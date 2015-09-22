#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

from lib.request.basic import req
from lib.controller.setplugin import activatePlugin


class pluginBase():


    def execute(self):
        print 123


activatePlugin(pluginBase)
