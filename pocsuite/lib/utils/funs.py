#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

from socket import gethostbyname
from urlparse import urlsplit


def url2ip(url):
    """
    works like turning 'http://baidu.com' => '180.149.132.47'
    """
    iport = urlsplit(url)[1].split(':')
    if len(iport) > 1:
        return gethostbyname(iport[0]), iport[1]
    return gethostbyname(iport[0])
