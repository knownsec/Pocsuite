#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

import functools
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING


def require_header(field):
    def _require_header(function):
        @functools.wraps(function)
        def check_header(self, *args):
            name = getattr(self, "name")
            headers = getattr(self, "headers")
            if field.lower() not in map(str.lower, headers.keys()):
                errMsg = "poc: %s need HTTP Header \"%s\"" % (name, field)
                logger.log(CUSTOM_LOGGING.ERROR, errMsg)
                return
            return function(self, *args)
        return check_header
    return _require_header


def require_param(field):
    def _require_param(function):
        @functools.wraps(function)
        def check_param(self, *args):
            name = getattr(self, "name")
            params = getattr(self, "params")
            if field not in params:
                errMsg = "poc: %s need extra params \"%s\"" % (name, field)
                logger.log(CUSTOM_LOGGING.ERROR, errMsg)
                return
            return function(self, *args)
        return check_param
    return _require_param
