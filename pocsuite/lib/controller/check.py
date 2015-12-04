#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.settings import POC_ATTRS
from pocsuite.lib.core.settings import OLD_VERSION_CHARACTER
from pocsuite.lib.core.data import kb


def pocViolation():
    violation = False
    for pocname, pocInstance in kb.registeredPocs.items():
        if isinstance(pocInstance, dict):
            violation = checkJsonInfo(pocname, pocInstance)
        else:
            violation = checkPocInfo(pocname, pocInstance)
    return violation


def checkJsonInfo(pocname, pocInstance):
    infos = []
    infoMsg = "checking %s" % pocname
    logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
    if 'pocInfo' in pocInstance:
        for attr in POC_ATTRS:
            if attr in pocInstance['pocInfo'] and pocInstance['pocInfo'].get(attr):
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


def isOldVersionPoc(poc):
    for _ in OLD_VERSION_CHARACTER:
        if _ not in poc:
            return False
    return True
