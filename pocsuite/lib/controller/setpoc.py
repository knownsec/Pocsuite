#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import re
import os
import glob
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.common import multipleReplace
from pocsuite.lib.core.common import readFile
from pocsuite.lib.core.settings import POC_IMPORTDICT
from pocsuite.lib.core.settings import POC_REGISTER_REGEX
from pocsuite.lib.core.settings import POC_CLASSNAME_REGEX
from pocsuite.lib.core.settings import POC_REGISTER_STRING


def setPoc():
    """
    @function 重新设置conf.pocFile
    """
    if conf.isPocString:
        retVal = loadPoc(conf.pocFile)
        kb.pocs.update(retVal)
    elif len(conf.pocFile.split(",")) > 1:
        for pocFile in conf.pocFile.split(","):
            pocFile = os.path.abspath(pocFile)
            retVal = loadPoc(pocFile)
            kb.pocs.update(retVal)
    else:
        conf.pocFile = os.path.abspath(conf.pocFile)
        if os.path.isfile(conf.pocFile):
            retVal = loadPoc(conf.pocFile)
            kb.pocs.update(retVal)
        elif os.path.isdir(conf.pocFile):
            pyFiles = glob.glob(os.path.join(conf.pocFile, "*.py"))
            jsonFiles = glob.glob(os.path.join(conf.pocFile, "*.json"))
            pocFiles = pyFiles + jsonFiles
            for pocFile in pocFiles:
                retVal = loadPoc(pocFile)
                kb.pocs.update(retVal)
        else:
            errMsg = "can't find any valid PoCs"
            logger.log(CUSTOM_LOGGING.ERROR, errMsg)

    conf.pocFile = None


def loadPoc(pocFile):
    if pocFile.endswith(".pyc"):
        conf.isPycFile = True

    if conf.isPocString:
        poc = conf.pocFile
        if not conf.pocname:
            if conf.pocFile:
                conf.pocname = os.path.split(conf.pocFile)[1]
            else:
                errMsg = "Use pocString must provide pocname"
                logger.log(CUSTOM_LOGGING.ERROR, errMsg)
        pocname = conf.pocname
    else:
        pocname = os.path.split(pocFile)[1]
        poc = readFile(pocFile)

    if not conf.isPycFile:
        if not re.search(POC_REGISTER_REGEX, poc):
            warnMsg = "poc: %s register is missing" % pocname
            logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
            className = getPocClassName(poc)
            poc += POC_REGISTER_STRING.format(className)

        retVal = multipleReplace(poc, POC_IMPORTDICT)
    else:
        retVal = poc
    return {pocname: retVal}


def getPocClassName(poc):
    try:
        className = re.search(POC_CLASSNAME_REGEX, poc).group(1)
    except:
        className = ""
    return className
