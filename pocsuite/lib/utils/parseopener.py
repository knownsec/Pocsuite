#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import urllib2
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING


def openerHeaders(op):
    headers = {}
    try:
        assert isinstance(op, urllib2.OpenerDirector)
        _ = op.addheaders
        for pair in _:
            # pair_copy = [part for part in pair]
            headers.update({pair[0]: pair[1]})
    except:
        errMsg = 'unable to fetch headers from given opener'
        logger.log(CUSTOM_LOGGING.ERROR, errMsg)
    return headers

if __name__ == '__main__':
    op = urllib2.build_opener()
    openerHeaders(op)
