#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite.pocsuite_cli import pcsInit
from pocsuite.lib.core.settings import PCS_OPTIONS
from pocsuite.lib.core.common import banner
from pocsuite.lib.core.data import kb


class Missile():
    def __init__(self, target, missile_info={}):
        if not missile_info["pocname"].endswith(".py"):
            missile_info["pocname"] += ".py"
        PCS_OPTIONS.update({
            "url": target,
            "pocFile": missile_info["pocstring"],
            "isPocString": True,
            "pocname": missile_info["pocname"],
            "headers": "",
            "extra_params": "",
            "mode": missile_info["mode"],
        })

    def run(self):
        pcsInit(PCS_OPTIONS)
        return kb.results
