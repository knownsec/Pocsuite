#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.settings import POC_ATTRS
from lib.core.settings import OLD_VERSION_CHARACTER
from lib.core.common import readFile
from lib.core.data import kb


def pocViolation():
    violation = False
    #infoMsg = "checking PoCs.."
    #logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
    for pocname, pocInstance in kb.registeredPocs.items():
        if isinstance(pocInstance, dict):
            violation = checkJsonInfo(pocname, pocInstance)
        else:
            violation = checkPocInfo(pocname, pocInstance)
    #logger.log(CUSTOM_LOGGING.SUCCESS, infoMsg)
    return violation


def checkJsonInfo(pocname, pocInstance):
    infos = []
    infoMsg = "checking %s" % pocname
    logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
    if pocInstance.has_key('pocInfo'):
        for attr in POC_ATTRS:
            if pocInstance['pocInfo'].has_key(attr) and pocInstance['pocInfo'].get(attr):
                continue
            infos.append(attr)
        if infos:
            warnMsg = "missing %s in %s" % (infos, pocname)
            logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
            return False
        return True


def checkPocInfo(pocname, pocInstance):
    infos = []
    infoMsg = "checking %s" % pocname
    logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
    for attr in POC_ATTRS:
        if hasattr(pocInstance, attr) and getattr(pocInstance, attr):
            continue
        infos.append(attr)
    if infos:
        warnMsg = "missing %s in %s" % (infos, pocname)
        logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
        return False
    return True


def isOldVersionPoc(filename):
    poc = readFile(filename)
    for _ in OLD_VERSION_CHARACTER:
        if _ not in poc:
            return False
    return True
