#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite.pocsuite_cli import modulePath
from pocsuite.lib.core.consoles import PocsuiteInterpreter
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import paths
from pocsuite.lib.core.common import setPaths
from pocsuite.lib.core.option import initializeKb


def main():
    paths.POCSUITE_ROOT_PATH = modulePath()
    setPaths()
    kb.unloadedList = {}

    initializeKb()

    pcs = PocsuiteInterpreter()
    pcs.shell_will_go()

if __name__ == "__main__":
    main()
