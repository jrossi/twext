#!/usr/bin/env python

##
# Copyright (c) 2006-2010 Apple Inc. All rights reserved.
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

import sys
import os
from distutils.core import Extension
from distutils.core import setup

extensions = [
    Extension("twext.python.sendmsg", sources=["twext/python/sendmsg.c"])
]
dist = setup(
    name             = "Calendar and Contacts Server",
    version          = "0.0.0",
    description      = "",
    long_description = "", 
    url              = None,
    author           = "Apple Inc.",
    author_email     = None,
    license          = None,
    platforms        = ["all"],
    packages         = [
        'twext',
        'twext.protocols', 
        'twext.python',
        'twext.internet'
    ],
    ext_modules      = extensions,
)
