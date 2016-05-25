#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""


class CUSTOM_LOGGING:
    SYSINFO = 9
    SUCCESS = 8
    ERROR = 7
    WARNING = 6


class OUTPUT_STATUS:
    SUCCESS = 1
    FAILED = 0


class HTTP_HEADER:
    ACCEPT = "Accept"
    ACCEPT_CHARSET = "Accept-Charset"
    ACCEPT_ENCODING = "Accept-Encoding"
    ACCEPT_LANGUAGE = "Accept-Language"
    AUTHORIZATION = "Authorization"
    CACHE_CONTROL = "Cache-Control"
    CONNECTION = "Connection"
    CONTENT_ENCODING = "Content-Encoding"
    CONTENT_LENGTH = "Content-Length"
    CONTENT_RANGE = "Content-Range"
    CONTENT_TYPE = "Content-Type"
    COOKIE = "Cookie"
    SET_COOKIE = "Set-Cookie"
    HOST = "Host"
    LOCATION = "Location"
    PRAGMA = "Pragma"
    PROXY_AUTHORIZATION = "Proxy-Authorization"
    PROXY_CONNECTION = "Proxy-Connection"
    RANGE = "Range"
    REFERER = "Referer"
    SERVER = "Server"
    USER_AGENT = "User-Agent"
    TRANSFER_ENCODING = "Transfer-Encoding"
    URI = "URI"
    VIA = "Via"


class PROXY_TYPE:
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    SOCKS4 = "SOCKS4"
    SOCKS5 = "SOCKS5"


class ERROR_TYPE:
    NOTIMPLEMENTEDERROR = 0
    CONNECTIONERROR = 1.0
    HTTPERROR = 1.1
    CONNECTTIMEOUT = 1.2
    TOOMANYREDIRECTS = 1.3
    BASEHTTPERROR = 1.4
    CHUNKEDENCODINGERROR = 1.5
    CONTENTDECODINGERROR = 1.6
    INVALIDSCHEMA = 1.7
    INVALIDURL = 1.8
    PROXYERROR = 1.9
    READTIMEOUT = 1.10
    OTHER = 2
