#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import collections
from pocsuite.lib.core.data import conf
from pocsuite.thirdparty import requests
from pocsuite.thirdparty.requests.hooks import default_hooks
from pocsuite.thirdparty.requests.models import DEFAULT_REDIRECT_LIMIT
from pocsuite.thirdparty.requests.models import REDIRECT_STATI
from pocsuite.thirdparty.requests.cookies import cookiejar_from_dict
from pocsuite.thirdparty.requests.compat import OrderedDict
from pocsuite.thirdparty.requests.adapters import HTTPAdapter
from pocsuite.thirdparty.requests.structures import CaseInsensitiveDict
from pocsuite.thirdparty.requests.utils import default_headers
from pocsuite.thirdparty.requests.packages.urllib3._collections import RecentlyUsedContainer


def requestsPatch():
    if hasattr(requests.packages.urllib3.util, '_Default'):
        requests.packages.urllib3.util._Default = None
    else:
        requests.packages.urllib3.util.timeout._Default = None

    def setVerifyToFalse():
        # 重写requests的cert_verify,禁用ssl verify
        def cert_verify(self, conn, url, verify, cert):
            conn.cert_reqs = 'CERT_NONE'
            conn.ca_certs = None
        requests.adapters.HTTPAdapter.cert_verify = cert_verify

    def setDefaultHeaders():
        def session_init(self):
            self.headers = CaseInsensitiveDict(conf.httpHeaders) if 'httpHeaders' in conf else default_headers()
            self.auth = None
            self.proxies = {}
            self.hooks = default_hooks()
            self.params = {}
            self.stream = False
            self.verify = True
            self.cert = None
            self.max_redirects = DEFAULT_REDIRECT_LIMIT
            self.trust_env = True
            self.cookies = cookiejar_from_dict({})
            self.adapters = OrderedDict()
            self.mount('https://', HTTPAdapter())
            self.mount('http://', HTTPAdapter())
            self.redirect_cache = RecentlyUsedContainer(1000)
        requests.sessions.Session.__init__ = session_init

    setVerifyToFalse()
    setDefaultHeaders()
    requests.packages.urllib3.disable_warnings()
