#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import ast
import codecs
from socket import gethostbyname
from urlparse import urlsplit

from pocsuite.lib.core.data import logger
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.enums import CUSTOM_LOGGING


def url2ip(url):
    """
    works like turning 'http://baidu.com' => '180.149.132.47'
    """
    iport = urlsplit(url)[1].split(':')
    if len(iport) > 1:
        return gethostbyname(iport[0]), iport[1]
    return gethostbyname(iport[0])


def writeText(fileName, content, encoding='utf8'):
    """
    write file with given fileName and encoding
    """
    try:
        fp = codecs.open(fileName, mode='w+', encoding=encoding)
        fp.write(content)
        fp.close()
        logger.log(CUSTOM_LOGGING.SYSINFO, '"%s" write to Text file "%s"' % (content, fileName))
    except Exception as e:
        logger.log(CUSTOM_LOGGING.WARNING, e)


def loadText(fileName, encoding='utf8'):
    """
    read file with given fileName and encoding
    """
    try:
        fp = codecs.open(fileName, mode='r', encoding=encoding)
        content = fp.readlines()
        fp.close()
        logger.log(CUSTOM_LOGGING.SYSINFO, 'return file "%s" content .' % fileName)
        return content
    except Exception as e:
        logger.log(CUSTOM_LOGGING.WARNING, e)


def writeBinary(fileName, content, encoding='utf8'):
    """
    write file with given fileName and encoding
    """
    try:
        fp = codecs.open(fileName, mode='wb+', encoding=encoding)
        fp.write(content)
        fp.close()
        logger.log(CUSTOM_LOGGING.SYSINFO, '"%s" write to Text file "%s"' % (content, fileName))
    except Exception as e:
        logger.log(CUSTOM_LOGGING.WARNING, e)


def getExtPar():
    return conf.params


def convExtPar():
    try:
        return ast.literal_eval(conf.params)
    except ValueError as e:
        logger.log(CUSTOM_LOGGING.ERROR, "conv extra-params failed : %s" % e)
        logger.log(CUSTOM_LOGGING.ERROR, "try to use getExtPar instead.")
