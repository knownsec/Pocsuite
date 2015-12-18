#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite.lib.core.data import kb
from pocsuite.pocsuite_cli import pcsInit
from pocsuite.lib.core.common import banner
from pocsuite.lib.core.settings import PCS_OPTIONS
from pocsuite.lib.settings import HTTP_DEFAULT_HEADER


class Missile():
    def __init__(self, target, missile_info={}):
        if not missile_info["pocname"].endswith(".py"):
            missile_info["pocname"] += ".py"
        PCS_OPTIONS.update(missile_info)

    def run(self):
        pcsInit(PCS_OPTIONS)
        return kb.results
