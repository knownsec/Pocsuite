#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING

from pocsuite.lib.utils.password import getLargeWeakPassword
from pocsuite.lib.utils.password import getWeakPassword

from pocsuite.lib.utils.funs import url2ip
from pocsuite.lib.utils.funs import getExtPar
from pocsuite.lib.utils.funs import strToDict
from pocsuite.lib.utils.funs import randomStr

from pocsuite.lib.utils.funs import writeText
from pocsuite.lib.utils.funs import writeBinary
from pocsuite.lib.utils.funs import loadText
from pocsuite.lib.utils.funs import resolve_js_redirects
