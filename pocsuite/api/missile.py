#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import time
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.common import filepathParser
from pocsuite.lib.core.common import multipleReplace
from pocsuite.lib.core.common import StringImporter
from pocsuite.lib.core.settings import POC_IMPORTDICT
from pocsuite.lib.core.settings import HTTP_DEFAULT_HEADER


class Missile():

    def __init__(self, target, missile_info={}):
        self.target = target
        self.pocString = missile_info["pocstring"]
        self.pocName = missile_info["pocname"]
        self.mode = "verify"
        self.params = {}
        conf.isPycFile = False
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
            pass  # TODO

    def run(self):
        poc = kb.registeredPocs[self.moduleName]
        result = poc.execute(self.target, mode=self.mode)
        output = (self.target, self.pocName, result.vulID, result.appName, result.appVersion, "success" if result.is_success() else "failed", time.strftime("%Y-%m-%d %X", time.localtime()), str(result.result))

        return output
