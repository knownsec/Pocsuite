#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

import os
from lib.core.data import conf
from lib.core.common import changeToPyImportType


def setPlugin():
    """ enable plugin function """

    if not conf.plugin:
        return

    else:
        with open('plugins/enabled_plugins.txt') as fp:
            for plugin in fp.readlines():
                try:
                    __import__(changeToPyImportType(plugin), fromlist=["*"])
                except ImportError:
                    errMsg = "%s register failed \"%s\"" % (plugin, str(ex))


def activatePlugin(pluginClz):
    """ activate plugin """
    pluginClz().execute()
