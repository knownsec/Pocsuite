#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

import re
import os
import glob
import json
from lib.core.data import kb
from lib.core.data import conf
from lib.core.data import paths
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.common import multipleReplace
from lib.core.common import readFile, writeFile
from lib.core.settings import POC_IMPORTDICT
from lib.core.settings import POC_REGISTER_REGEX
from lib.core.settings import POC_CLASSNAME_REGEX
from lib.core.settings import POC_REGISTER_STRING


def setPocFile():
    """
    @function 重新设置conf.pocFile
    """
    if len(conf.pocFile.split(",")) > 1:
        for pocFile in conf.pocFile.split(","):
            pocFile = os.path.abspath(pocFile)
            retVal = setTemporaryPoc(pocFile)
            kb.pocFiles.add(retVal)
    else:
        conf.pocFile = os.path.abspath(conf.pocFile)
        if os.path.isfile(conf.pocFile):
            retVal = setTemporaryPoc(conf.pocFile)
            kb.pocFiles.add(retVal)
        elif os.path.isdir(conf.pocFile):
            pyFiles = glob.glob(os.path.join(conf.pocFile, "*.py"))
            jsonFiles = glob.glob(os.path.join(conf.pocFile, "*.json"))
            pocFiles = pyFiles + jsonFiles
            for pocFile in pocFiles:
                retVal = setTemporaryPoc(pocFile)
                kb.pocFiles.add(retVal)
        else:
            errMsg = "can't find any valid PoCs"
            logger.log(CUSTOM_LOGGING.ERROR, errMsg)


def setTemporaryPoc(pocFile):
    pocFilename = "_" + os.path.split(pocFile)[1]
    if not os.path.isdir(paths.POCSUITE_TMP_PATH):
        os.makedirs(paths.POCSUITE_TMP_PATH)
    pocname = os.path.join(paths.POCSUITE_TMP_PATH, pocFilename)
    poc = readFile(pocFile)

    if not re.search(POC_REGISTER_REGEX, poc):
        warnMsg = "poc: %s register is missing" % pocFilename
        logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
        className = getPocClassName(poc)
        poc += POC_REGISTER_STRING.format(className)

    retVal = multipleReplace(poc, POC_IMPORTDICT)
    writeFile(pocname, retVal)
    return pocname


def getPocClassName(poc):
    try:
        className = re.search(POC_CLASSNAME_REGEX, poc).group(1)
    except:
        className = ""
    return className
