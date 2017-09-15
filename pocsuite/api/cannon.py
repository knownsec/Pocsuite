#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import time
import socket
import imp
from os import path
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.common import delModule
from pocsuite.lib.core.settings import HTTP_DEFAULT_HEADER


class Cannon():

    def __init__(self, target, info={}, mode='veirfy', params={}, headers={}, timeout=30):
        self.target = target
        self.pocString = info["pocstring"]
        self.pocName = info["pocname"].replace('.', '')
        self.pocFile = info["pocname"]
        self.mode = mode if mode in ('verify', 'attack') else 'verify'
        self.delmodule = False
        self.params = params
        conf.isPycFile = info.get('ispycfile', False)
        conf.httpHeaders = HTTP_DEFAULT_HEADER
        # fix issue #112
        conf.retry = 0
        if headers:
            conf.httpHeaders.update(headers)

        try:
            kb.registeredPocs
        except Exception:
            kb.registeredPocs = {}

        self._setHTTPTimeout(timeout)

    def _setHTTPTimeout(self, timeout):
        """
        Set the HTTP timeout
        """
        timeout = float(timeout)
        socket.setdefaulttimeout(timeout)

    def loadPoc(self):
        class_name = 'POCBase'
        filepath = path.dirname(self.pocFile)
        try:
            file_name = path.split(self.pocFile)[-1].split('.')[0]
            fp,pathname,description = imp.find_module(file_name,[filepath])
        except ImportError as e:
            logger.exception(e)
            raise
        try:
            _module = imp.load_module(class_name,fp,pathname,description)
            _pocbase = getattr(_module,class_name)
            for v in _module.__dict__.values():
                if isinstance(v,type) and _pocbase in v.__bases__:
                    return v()
        except Exception as e:
            logger.exception(e)
            raise
        finally:
            if fp:
                fp.close()

    def run(self):
        try:
            poc = self.loadPoc()
            result = poc.execute(self.target, headers=conf.httpHeaders, mode=self.mode, params=self.params)
            output = (self.target, self.pocName, result.vulID, result.appName, result.appVersion, (1, "success") if result.is_success() else result.error, time.strftime("%Y-%m-%d %X", time.localtime()), str(result.result))

            if self.delmodule:
                delModule(self.moduleName)
            return output
        except Exception, ex:
            logger.log(CUSTOM_LOGGING.ERROR, ex)
