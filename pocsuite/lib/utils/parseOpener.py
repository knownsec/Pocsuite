#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

import urllib2

def openerHeaders(op):
    headers = {}
    _ = op.addheaders
    for pair in _:
        pair_copy = [part for part in pair]
        headers.update({pair[0]: pair[1]})
    return headers                
