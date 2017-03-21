#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import os


def initial():
    currentUserHomePath = os.path.expanduser('~')
    _ = """[Telnet404]\nAccount = Your Telnet404 Account\npassword = Your Telnet404 Password"""
    if not os.path.isfile(currentUserHomePath + '/.pocsuiterc'):
        with open(currentUserHomePath + '/.pocsuiterc', 'w') as fp:
            fp.write(_)

initial()
