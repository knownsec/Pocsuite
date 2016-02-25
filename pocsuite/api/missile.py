#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite.lib.core.data import kb
from pocsuite.pocsuite_cli import pcsInit
from pocsuite.lib.core.settings import PCS_OPTIONS



class Missile():

    def __init__(self, target, missile_info={}):
        if not missile_info["pocname"].endswith(".py"):
            missile_info["pocname"] += ".py"
        PCS_OPTIONS.update({
            "url": target,
            "host": "",
            "pocFile": missile_info["pocstring"],
            "isPocString": True,
            "pocname": missile_info["pocname"],
            "headers": "",
            "extra_params": "",
            "mode": missile_info["mode"],
            "retry": False,
            "delay": 0,
            "requires": False,
            "requiresFreeze": False
            "quiet": True
        })

    def run(self):
        pcsInit(PCS_OPTIONS)
        return kb.results
