#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import string
from random import choice
from pocsuite.lib.core.common import getFileItems
from pocsuite.lib.core.data import paths


def getWeakPassword():
    return getFileItems(paths.WEAK_PASS)


def getLargeWeakPassword():
    return getFileItems(paths.LARGE_WEAK_PASS)


def genPassword(length=8, chars=string.letters + string.digits):
    return "".join([choice(chars) for _ in range(length)])
