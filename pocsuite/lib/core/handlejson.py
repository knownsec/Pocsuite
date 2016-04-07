#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import re
import json
import time
from string import atof
from pocsuite.lib.core.common import parseTargetUrl
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.data import resultJson
from pocsuite.lib.core.data import savedReq
from pocsuite.lib.request.basic import req


def initilizeJson(devilJson):
    _ = ("step", "method", "vulPath", "params", "headers")
    return [devilJson[i] for i in _] + [resSelect(devilJson["match"]), int(devilJson["status"])]


def resSelect(res):
    return res['regex'] or atof(res['time'])


def showResult(tag):
    for key1, value1 in resultJson[tag].iteritems():
        for key2, value2 in value1.iteritems():
            if key1 != 'verifyInfo':
                logger.log(CUSTOM_LOGGING.SUCCESS, key2 + " : " + resultJson[tag][key1][key2])

    pass


def execReq(poc, mode, targetUrl):
    pocInfo, devilJson = poc['pocInfo'], poc["pocExecute"]
    result = False

    infoMsg = "poc-%s '%s' has already been detected against '%s'." % (pocInfo["vulID"], pocInfo["name"], targetUrl)
    logger.log(CUSTOM_LOGGING.SUCCESS, infoMsg)

    for targetJson in devilJson[mode]:

        if mode == 'verify':
            result = _executeVerify(pocInfo, targetJson, targetUrl, 'verify')
            if targetJson['step'] == '0' and result:
                return True
            elif targetJson['step'] != '0' and not result:
                return False

        else:
            result = _executeAttack(pocInfo, targetJson, targetUrl)
            if targetJson['step'] == '0' and result:
                showResult(targetUrl + pocInfo['vulID'])
                return True
            elif targetJson['step'] != '0' and not result:
                return False

    if result:
        showResult(targetUrl + pocInfo['vulID'])

    return result


def _executeVerify(pocInfo, targetJson, targetUrl, mode):
    url, startTime = parseTargetUrl(targetUrl), time.time()
    step, method, path, params, headers, match, status_code = initilizeJson(targetJson)

    if (targetUrl + pocInfo['vulID']) not in resultJson:
        resultJson[targetUrl + pocInfo['vulID']] = {}
        resultJson[targetUrl + pocInfo['vulID']]['verifyInfo'] = {'URL': url, 'Postdata': params, 'Path': path}

    try:
        if method == 'get':
            r = req.get('%s/%s' % (url, path), params=params, headers=headers)
        else:
            r = req.post('%s/%s' % (url, path), data=params, headers=headers)

    except Exception, ex:
        logger.log(CUSTOM_LOGGING.ERROR, str(ex))
        return False

    if r.status_code != status_code:
        return False

    if isinstance(match, float) and (time.time() - startTime > match):
        savedReq.update({targetUrl + pocInfo['vulID']: r.req})

        if mode == 'verify':
            logger.log(CUSTOM_LOGGING.SUCCESS, "URL : " + targetUrl + path)
            if params:
                logger.log(CUSTOM_LOGGING.SUCCESS, "Postdata : " + params)
        return True

    else:
        for mat in match:
            # TODO
            if not re.search(mat.encode(), r.content):
                return False

        savedReq.update({targetUrl + pocInfo['vulID']: r.content})

        if mode == 'verify':
            logger.log(CUSTOM_LOGGING.SUCCESS, "URL : " + targetUrl + path)
            if params:
                logger.log(CUSTOM_LOGGING.SUCCESS, "Postdata : " + params)

        return True

    return False


def _executeAttack(pocInfo, targetJson, targetUrl):
    if not _executeVerify(pocInfo, targetJson, targetUrl, 'attack'):
        return False

    _filterColumn(targetJson['result'], targetUrl, pocInfo['vulID'])
    return True


def _filterColumn(Json, targetUrl, vulID):

    for k, v in Json.iteritems():
        if k not in resultJson[targetUrl + vulID]:
            resultJson[targetUrl + vulID][k] = {}
        resultJson[targetUrl + vulID][k].update(v)

    for key1, value1 in resultJson[targetUrl + vulID].iteritems():
        for key2, value2 in value1.iteritems():
            if value2.startswith("<regex>"):
                valuePattern = re.compile(value2[value2.index('>') + 1:])
                match = valuePattern.search(savedReq[targetUrl + vulID])
                if match:
                    resultJson[targetUrl + vulID][key1][key2] = match.group()
