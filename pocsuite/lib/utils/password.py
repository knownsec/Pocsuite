#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite.lib.core.common import getFileItems
from pocsuite.lib.core.data import paths


def getWeakPassword():
    return getFileItems(paths.WEAK_PASS)


def getLargeWeakPassword():
    return getFileItems(paths.LARGE_WEAK_PASS)
