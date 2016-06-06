#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import re
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.settings import POC_ATTRS
from pocsuite.lib.core.settings import POC_REQUIRES_REGEX
from pocsuite.lib.core.settings import OLD_VERSION_CHARACTER


def requiresCheck():
    if not conf.requires:
        return

    requires_regex = re.compile(POC_REQUIRES_REGEX)
    install_requires = []
    for _, poc in kb.pocs.items():
        try:
            requires = requires_regex.search(poc).group(1)
            install_requires += [require[1:-1] for require in requires.split(",")]
        except:
            pass

    infoMsg = "install_requires:\n" + "\n".join(install_requires)
    logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)


def pocViolation():
    violation = False
    if conf.requiresFreeze:
        install_requires = []
        for pocName, pocInstance in kb.registeredPocs.items():
            if isinstance(pocInstance, dict):
                continue
            requires = getRequires(pocName, pocInstance)
            if not requires:
                continue
            install_requires += list(requires)
        infoMsg = "install_requires:\n" + "\n".join(install_requires)
        logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
        return

    for pocName, pocInstance in kb.registeredPocs.items():
        if isinstance(pocInstance, dict):
            violation = checkJsonInfo(pocName, pocInstance)
        else:
            violation = checkPocInfo(pocName, pocInstance)
    return violation


def checkJsonInfo(pocName, pocInstance):
    infos = []
    infoMsg = "checking %s" % pocName
    logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
    if 'pocInfo' in pocInstance:
        for attr in POC_ATTRS:
            if attr in pocInstance['pocInfo'] and pocInstance['pocInfo'].get(attr):
                continue
            infos.append(attr)
        if infos:
            warnMsg = "missing %s in %s" % (infos, pocName)
            logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
            return False
        return True


def checkPocInfo(pocName, pocInstance):
    infos = []
    infoMsg = "checking %s" % pocName
    logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
    for attr in POC_ATTRS:
        if hasattr(pocInstance, attr) and getattr(pocInstance, attr):
            continue
        infos.append(attr)
    if infos:
        warnMsg = "missing %s in %s" % (infos, pocName)
        logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
        return False
    return True


def isOldVersionPoc(poc):
    for _ in OLD_VERSION_CHARACTER:
        if _ not in poc:
            return False
    return True


def getRequires(pocName, pocInstance):
    if hasattr(pocInstance, "install_requires"):
        return getattr(pocInstance, "install_requires")
