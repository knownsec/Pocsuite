#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import os
import sys
import json
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.common import filepathParser
from pocsuite.lib.core.common import changeToPyImportType
from pocsuite.lib.core.common import StringImporter


def registerPoc(pocClass):
    module = pocClass.__module__.split('.')[-1]
    if module in kb.registeredPocs:
        return

    kb.registeredPocs[module] = pocClass()


def registerJsonPoc(pocDict):
    pocname = pocDict.keys()[0]
    if pocname in kb.registeredPocs:
        return

    jsonPoc = json.load(pocDict[pocname])
    kb.registeredPocs[pocname] = jsonPoc


def registerPyPoc(pocDict):
    pocname = pocDict.keys()[0]
    _, moduleName = filepathParser(pocname)
    try:
        importer = StringImporter(moduleName, pocDict[pocname])
        importer.load_module(moduleName)
    except ImportError, ex:
        errMsg = "%s register failed \"%s\"" % (moduleName, str(ex))
        logger.log(CUSTOM_LOGGING.ERROR, errMsg)


def addSysPath(*paths):
    for path in paths:
        if not path.startswith('/'):
            path = os.path.join(os.getcwd(), path)
        sys.path.append(path)
