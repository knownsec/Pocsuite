#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING


def require_header(field):
    def _require_header(function):
        def check_header(self, *args):
            name = getattr(self, "name")
            headers = getattr(self, "headers")
            if field in map(str.lower, headers.keys()):
                return function(self, *args)
            else:
                errMsg = "poc: %s need HTTP Header \"%s\"" % (name, field)
                logger.log(CUSTOM_LOGGING.ERROR, errMsg)
                return
        return check_header
    return _require_header
