#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

import sys
from pocsuite import pcsInit
from lib.core.common import banner
from lib.core.common import dataToStdout
from lib.core.settings import PCS_OPTIONS


if __name__ == "__main__":

    try:
        pocFile, targetUrl = sys.argv[1: 3]
    except ValueError:
        banner()

        excMsg = "usage: python pcs-attack.py [pocfile] [url]\n"
        excMsg += "pocsuite: error: too few arguments"
        dataToStdout(excMsg)
        sys.exit(1)

    PCS_OPTIONS.update({'url': targetUrl, 'pocFile': pocFile, 'Mode': 'attack'})
    pcsInit(PCS_OPTIONS)
