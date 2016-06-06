#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite.lib.core.datatype import AttribDict
from pocsuite.lib.core.log import LOGGER
from pocsuite.lib.core.defaults import defaults

# logger
logger = LOGGER

# object to share within function and classes command
# line options and settings
conf = AttribDict()

# Dictionary storing
# (1)targets, (2)registeredPocs, (3) bruteMode
# (4)results, (5)pocFiles
# (6)multiThreadMode \ threadContinue \ threadException
kb = AttribDict()

cmdLineOptions = AttribDict()

registeredPocs = {}

# pocsuite paths
paths = AttribDict()

defaults = AttribDict(defaults)

pocJson = AttribDict()

resultJson = AttribDict()

savedReq = AttribDict()
