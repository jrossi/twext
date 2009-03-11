##
# Copyright (c) 2008-2009 Apple Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

from twisted.internet import protocol
from twisted.python import log
from twisted.web2.channel.http import HTTPFactory

__all__ = [
    "HTTP503LoggingFactory",
]

class OverloadedLoggingServerProtocol (protocol.Protocol):
    def __init__(self, retryAfter, outstandingRequests):
        self.retryAfter = retryAfter
        self.outstandingRequests = outstandingRequests

    def connectionMade(self):
        log.msg(overloaded=self)

        self.transport.write(
            "HTTP/1.0 503 Service Unavailable\r\n"
            "Content-Type: text/html\r\n"
        )

        if self.retryAfter:
            self.transport.write(
                "Retry-After: %s\r\n" % (self.retryAfter,)
            )

        self.transport.write(
            "Connection: close\r\n\r\n"
            "<html><head><title>Service Unavailable</title></head>"
            "<body><h1>Service Unavailable</h1>"
            "The server is currently overloaded, "
            "please try again later.</body></html>"
        )
        self.transport.loseConnection()

class HTTP503LoggingFactory (HTTPFactory):
    """
    Factory for HTTP server which emits a 503 response when overloaded.
    """
    def __init__(self, requestFactory, maxRequests=600, retryAfter=0, **kwargs):
        self.retryAfter = retryAfter
        HTTPFactory.__init__(self, requestFactory, maxRequests, **kwargs)

    def buildProtocol(self, addr):
        if self.outstandingRequests >= self.maxRequests:
            return OverloadedLoggingServerProtocol(self.retryAfter, self.outstandingRequests)
        
        p = protocol.ServerFactory.buildProtocol(self, addr)
        
        for arg,value in self.protocolArgs.iteritems():
            setattr(p, arg, value)

        return p
