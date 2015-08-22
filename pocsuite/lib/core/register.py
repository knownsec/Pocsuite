#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

import sys
import json
from lib.core.data import kb
from lib.core.common import filepathParser
from lib.core.common import changeToPyImportType


def registerPoc(pocClass):
    module = pocClass.__module__.split('.')[-1]
    if module in kb.registeredPocs:
        return

    kb.registeredPocs[module] = pocClass()


def registerJsonPoc(path):
    _, pocname = filepathParser(path)
    if pocname in kb.registeredPocs:
        return

    with open(path) as f:
        jsonPoc = json.load(f)
        kb.registeredPocs[pocname] = jsonPoc


def registerPyPoc(path):
    _, moduleName = filepathParser(path)
    module = changeToPyImportType(path)
    try:
        __import__(module, fromlist=["*"])
    except ImportError:
        # TODO 需要再搞一下
        addSysPath(_)
        __import__(moduleName, fromlist=["*"])


def addSysPath(*paths):
    for path in paths:
        if not path.startswith('/'):
            path = os.path.join(os.getcwd(), path)
        sys.path.append(path)
