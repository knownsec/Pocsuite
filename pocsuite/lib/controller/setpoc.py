#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

import os
import glob
import json
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.data import paths
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.common import multipleReplace
from pocsuite.lib.core.common import readFile, writeFile
from pocsuite.lib.core.settings import POC_IMPORTDICT


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
    retVal = multipleReplace(poc, POC_IMPORTDICT)
    # TODO 直接写入tmp文件夹 没有考虑是否存在文件 或者使用后删除文件
    writeFile(pocname, retVal)
    return pocname
