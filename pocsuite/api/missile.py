#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite.lib.core.data import kb
from pocsuite.pocsuite_cli import pcsInit

class Missile():

    def __init__(self, target, missile_info={}):
        if not missile_info["pocname"].endswith(".py"):
            missile_info["pocname"] += ".py"
        self.PCS_OPTIONS = {
            "url": target,
            "host": "",
            "pocFile": missile_info["pocstring"],
            "isPocString": True,
            "pocname": missile_info["pocname"],
            "headers": "",
            "extra_params": "",
            "Mode": missile_info["mode"],
            "retry": False,
            "delay": 0,
            "requires": False,
            "requiresFreeze": False,
            "quiet": True,
            'threads': 1,
            'urlFile': None,
            'agent': None,
            'referer': None,
            'cookie': None,
            'randomAgent': False,
            'report': None,
            'proxy': None,
            'proxyCred': None,
            'timeout': 5
        }

    def run(self):
        pcsInit(self.PCS_OPTIONS)
        return kb.results
