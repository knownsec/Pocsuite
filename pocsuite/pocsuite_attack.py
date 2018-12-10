#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import sys
from pocsuite.pocsuite_cli import pcsInit
from pocsuite.lib.core.common import banner
from pocsuite.lib.core.common import dataToStdout
from pocsuite.lib.core.settings import PCS_OPTIONS


def main():
    try:
        pocFile, targetUrl = sys.argv[1: 3]
    except ValueError:
        excMsg = "usage: pcs-attack [pocfile] [url]\n"
        excMsg += "pocsuite: error: too few arguments"
        dataToStdout(excMsg)
        sys.exit(1)

    PCS_OPTIONS.update(
        {
            'url': targetUrl, 'pocFile': pocFile, 'headers': None, 'extra_params': None,
            'host': None, 'Mode': 'attack', 'retry': None, 'delay': None, 'dork': None,
            'vulKeyword': None,
        }
    )
    pcsInit(PCS_OPTIONS)

if __name__ == "__main__":
    main()
