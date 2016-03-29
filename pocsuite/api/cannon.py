#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import time
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.common import filepathParser
from pocsuite.lib.core.common import multipleReplace
from pocsuite.lib.core.common import StringImporter
from pocsuite.lib.core.common import delModule
from pocsuite.lib.core.settings import POC_IMPORTDICT
from pocsuite.lib.core.settings import HTTP_DEFAULT_HEADER


class Cannon():

    def __init__(self, target, info={}):
        self.target = target
        self.pocString = info["pocstring"]
        self.pocName = info["pocname"]
        self.mode = "verify"
        self.delmodule = False
        self.params = {}
        conf.isPycFile = info.get('ispycfile', False)
        conf.httpHeaders = {}

        try:
            kb.registeredPocs
        except Exception:
            kb.registeredPocs = {}

        self.registerPoc()

    def registerPoc(self):
        pocString = multipleReplace(self.pocString, POC_IMPORTDICT)
        _, self.moduleName = filepathParser(self.pocName)
        try:
            importer = StringImporter(self.moduleName, pocString)
            importer.load_module(self.moduleName)
        except ImportError, ex:
            logger.log(CUSTOM_LOGGING.ERROR, ex)

    def run(self):
        try:
            poc = kb.registeredPocs[self.moduleName]
            result = poc.execute(self.target, mode=self.mode)
            output = (self.target, self.pocName, result.vulID, result.appName, result.appVersion, "success" if result.is_success() else "failed", time.strftime("%Y-%m-%d %X", time.localtime()), result.result)
            if self.delmodule:
                delModule(self.moduleName)
            return output
        except Exception, ex:
            logger.log(CUSTOM_LOGGING.ERROR, ex)
