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
                Msg = 'Enter HTTP Header "%s" for "%s"' % (field, self.url)
                logger.log(CUSTOM_LOGGING.SYSINFO, Msg)
                self.headers[field] = raw_input()
            return function(self, *args)
        return check_header
    return _require_header
