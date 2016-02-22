#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite import pocsuite_cli
from pocsuite import pocsuite_verify
from pocsuite import pocsuite_attack
from pocsuite import pocsuite_console

from pocsuite.pocsuite_cli import modulePath
from pocsuite.lib.core.common import setPaths
from pocsuite.lib.core.data import paths

from nose.tools import assert_true


class TestPocsuiteBase(object):

    def test_pocsuite_setpath(self):
        paths.POCSUITE_ROOT_PATH = modulePath()
        setPaths()
        assert_true(paths.POCSUITE_ROOT_PATH.endswith("pocsuite"))
        assert_true(paths.POCSUITE_OUTPUT_PATH.endswith("output"))
