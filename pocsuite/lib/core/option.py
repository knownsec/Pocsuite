#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

import re
import os
import copy
import random
import Queue
import urlparse
import socket
from lib.core.data import logger
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import paths
from lib.core.datatype import AttribDict
from lib.core.settings import IS_WIN
from lib.core.enums import CUSTOM_LOGGING
from lib.core.enums import PROXY_TYPE
from lib.core.enums import HTTP_HEADER
from lib.core.settings import HTTP_DEFAULT_HEADER
from lib.core.common import getFileItems
from lib.core.common import safeExpandUser
from lib.core.common import getPublicTypeMembers
from lib.core.register import registerJsonPoc
from lib.core.register import registerPyPoc
from lib.core.exception import PocsuiteFilePathException
from lib.core.exception import PocsuiteSyntaxException
from lib.controller.check import pocViolation
from lib.controller.check import isOldVersionPoc
from lib.controller.setpoc import setPocFile
from thirdparty.socks import socks
from thirdparty.oset.pyoset import oset
from thirdparty.colorama.initialise import init as coloramainit



def initOptions(inputOptions=AttribDict()):
    if IS_WIN:
        coloramainit()

    # TODO
    conf.url = inputOptions.url
    conf.urlFile = inputOptions.urlFile
    conf.mode = inputOptions.Mode
    conf.pocFile = inputOptions.pocFile
    conf.randomAgent = inputOptions.randomAgent
    conf.agent = inputOptions.agent
    conf.cookie = inputOptions.cookie
    conf.headers = inputOptions.headers
    conf.referer = inputOptions.referer
    conf.threads = inputOptions.threads
    conf.report = inputOptions.report
    conf.proxy = inputOptions.proxy
    conf.proxyCred = inputOptions.proxyCred
    conf.timeout = inputOptions.timeout
    conf.params = None
    conf.httpHeaders = HTTP_DEFAULT_HEADER

    initializeKb()


def initializeKb():
    kb.targets = Queue.Queue()
    kb.pocFiles = set()
    kb.results = oset()
    kb.registeredPocs = {}


def registerPocFromFile():
    """
    @function import方式导入Poc文件, import Poc的时候自动rigister了
    """
    for path in kb.pocFiles:
        if path.endswith(".py"):
            if not isOldVersionPoc(path):
                registerPyPoc(path)
            else:
                warnMsg = "%s is old version poc" % path
                logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
        elif path.endswith(".json"):
            registerJsonPoc(path)


def init():
    _setHTTPUserAgent()
    _setHTTPReferer()
    _setHTTPCookies()
    _setHTTPTimeout()
    _setHTTPExtraHeaders()

    setPocFile()
    registerPocFromFile()
    pocViolation()

    setMultipleTarget()
    _setHTTPProxy()

# TODO
def _setHTTPUserAgent():
    """
    @function Set the HTTP User-Agent header.
    """
    if conf.agent:
        debugMsg = "setting the HTTP User-Agent header"
        logger.debug(debugMsg)

        conf.httpHeaders[HTTP_HEADER.USER_AGENT] = conf.agent

    if conf.randomAgent:
        infoMsg = "loading random HTTP User-Agent header(s) from "
        infoMsg += "file '%s'" % paths.USER_AGENTS
        logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
        try:
            userAgents = getFileItems(paths.USER_AGENTS)
        except IOError:
            warnMsg = "unable to read HTTP User-Agent header "
            warnMsg += "file '%s'" % paths.USER_AGENTS
            logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
            return

        userAgent = random.sample(userAgents, 1)
        infoMsg = "fetched random HTTP User-Agent header from "
        infoMsg += "file '%s': '%s'" % (paths.USER_AGENTS, userAgent)
        logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)

        conf.httpHeaders[HTTP_HEADER.USER_AGENT] = userAgent


def _setHTTPCookies():
    """
    Set the HTTP Cookie header
    """

    if conf.cookie:
        debugMsg = "setting the HTTP Cookie header"
        logger.debug(debugMsg)

        conf.httpHeaders[HTTP_HEADER.COOKIE] = conf.cookie


def _setHTTPReferer():
    """
    Set the HTTP Referer
    """

    if conf.referer:
        debugMsg = "setting the HTTP Referer header"
        logger.debug(debugMsg)

        conf.httpHeaders[HTTP_HEADER.REFERER] = conf.referer


def _setHTTPExtraHeaders():
    if conf.headers:
        infoMsg = "setting extra HTTP headers"
        logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)

        conf.headers = conf.headers.split("\n") if "\n" in conf.headers else conf.headers.split("\\n")

        for headerValue in conf.headers:
            if not headerValue.strip():
                continue

            if headerValue.count(':') >= 1:
                header, value = (_.lstrip() for _ in headerValue.split(":", 1))

                if header and value:
                    conf.httpHeaders[header] = value
            else:
                errMsg = "invalid header value: %s. Valid header format is 'name:value'" % repr(headerValue).lstrip('u')
                raise PocsuiteSyntaxException(errMsg)

def setMultipleTarget():

    if not conf.urlFile:
        for pocname, pocInstance in kb.registeredPocs.items():
            kb.targets.put((conf.url, pocInstance, pocname))
        return

    conf.urlFile = safeExpandUser(conf.urlFile)
    infoMsg = "parsing multiple targets list from '%s'" % conf.urlFile
    logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)

    if not os.path.isfile(conf.urlFile):
        errMsg = "the specified file does not exist"
        raise PocsuiteFilePathException(errMsg)

    for line in getFileItems(conf.urlFile):
        for pocname, poc in kb.registeredPocs.items():
            if not isinstance(poc, dict):
                kb.targets.put((line.strip(), copy.copy(poc), pocname))
            else:
                kb.targets.put((line.strip(), poc, pocname))


def _setHTTPProxy():
    """
    Check and set the HTTP/SOCKS proxy for all HTTP requests.
    """

    if not conf.proxy:
        return

    infoMsg = "setting the HTTP/SOCKS proxy for all HTTP requests"
    logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)

    try:
        _ = urlparse.urlsplit(conf.proxy)
    except Exception, ex:
        errMsg = "invalid proxy address '%s' ('%s')" % (conf.proxy, ex)
        raise PocsuiteSyntaxException(errMsg)

    hostnamePort = _.netloc.split(":")
    scheme = _.scheme.upper()
    hostname = hostnamePort[0]
    port = None
    username = None
    password = None

    if len(hostnamePort) == 2:
        try:
            port = int(hostnamePort[1])
        except:
            pass  # drops into the next check block

    if not all((scheme, hasattr(PROXY_TYPE, scheme), hostname, port)):
        errMsg = "proxy value must be in format '(%s)://address:port'" % "|".join(_[0].lower() for _ in getPublicTypeMembers(PROXY_TYPE))
        raise PocsuiteSyntaxException(errMsg)

    if conf.proxyCred:
        _ = re.search("^(.*?):(.*?)$", conf.proxyCred)
        if not _:
            errMsg = "Proxy authentication credentials "
            errMsg += "value must be in format username:password"
            raise PocsuiteSyntaxException(errMsg)
        else:
            username = _.group(1)
            password = _.group(2)

    if scheme == PROXY_TYPE.SOCKS4:
        proxyMode = socks.PROXY_TYPE_SOCKS4
    elif scheme == PROXY_TYPE.SOCKS5:
        proxyMode = socks.PROXY_TYPE_SOCKS5
    else:
        proxyMode = socks.PROXY_TYPE_HTTP

    socks.setdefaultproxy(proxyMode, hostname, port, username=username, password=password)
    socket.socket = socks.socksocket


def _setHTTPTimeout():
    """
    Set the HTTP timeout
    """

    if conf.timeout:
        infoMsg = "setting the HTTP timeout"
        logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)

        conf.timeout = float(conf.timeout)

        if conf.timeout < 3.0:
            warnMsg = "the minimum HTTP timeout is 3 seconds, pocsuite will going to reset it"
            logger.log(CUSTOM_LOGGING.WARNING, warnMsg)

            conf.timeout = 3.0
    else:
        conf.timeout = 30.0

    socket.setdefaulttimeout(conf.timeout)
