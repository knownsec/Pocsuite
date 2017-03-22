#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import os
from pocsuite.lib.core.data import defaults
from pocsuite.lib.core.settings import INDENT, USAGE, VERSION
from pocsuite.thirdparty.argparse import argparse


def parseCmdOptions():
    """
    @function parses the command line parameters and arguments
    """

    parser = argparse.ArgumentParser(usage=USAGE, formatter_class=argparse.RawTextHelpFormatter, add_help=False)

    parser.add_argument("-h", "--help", action="help",
                        help="Show help message and exit")

    parser.add_argument("--version", action="version",
                        version=VERSION, help="Show program's version number and exit")

    parser.add_argument("--update", dest="update", action="store_true",
                        help="Update Pocsuite")

    target = parser.add_argument_group('target')

    target.add_argument("-u", "--url", dest="url",
                        help="Target URL (e.g. \"http://www.targetsite.com/\")")

    target.add_argument("-f", "--file", action="store", dest="urlFile",
                        help="Scan multiple targets given in a textual file")

    target.add_argument("-r", dest="pocFile",
                        help="Load POC from a file (e.g. \"_0001_cms_sql_inj.py\") or directory (e.g. \"modules/\")")

    mode = parser.add_argument_group('mode')

    mode.add_argument("--verify", dest="Mode", default='verify', action="store_const", const='verify',
                      help="Run poc with verify mode")

    mode.add_argument("--attack", dest="Mode", action="store_const", const='attack',
                      help="Run poc with attack mode")

    request = parser.add_argument_group('request')

    request.add_argument("--cookie", dest="cookie",
                         help="HTTP Cookie header value")

    request.add_argument("--referer", dest="referer",
                         help="HTTP Referer header value")

    request.add_argument("--user-agent", dest="agent",
                         help="HTTP User-Agent header value")

    request.add_argument("--random-agent", dest="randomAgent", action="store_true", default=False,
                         help="Use randomly selected HTTP User-Agent header value")

    request.add_argument("--proxy", dest="proxy",
                         help="Use a proxy to connect to the target URL")

    request.add_argument("--proxy-cred", dest="proxyCred",
                         help="Proxy authentication credentials (name:password)")

    request.add_argument("--timeout", dest="timeout",
                         help="Seconds to wait before timeout connection (default 30)")

    request.add_argument("--retry", dest="retry", default=False,
                         help="Time out retrials times.")

    request.add_argument("--delay", dest="delay",
                         help="Delay between two request of one thread")

    request.add_argument("--headers", dest="headers",
                         help="Extra headers (e.g. \"key1: value1\\nkey2: value2\")")

    request.add_argument("--host", dest="host",
                         help="Host in HTTP headers.")

    params = parser.add_argument_group("params")

    params.add_argument("--extra-params", dest="extra_params",
                        help="Extra params (e.g. \"{username: \'***\', password: \'***\'}\")")

    optimization = parser.add_argument_group("optimization")

    optimization.add_argument("--threads", dest="threads", type=int, default=1,
                              help="Max number of concurrent HTTP(s) requests (default %d)" % defaults.threads)

    optimization.add_argument("--report", dest="report",
                              help="Save a html report to file (e.g. \"./report.html\")")

    optimization.add_argument("--batch", dest="batch",
                              help="Automatically choose defaut choice without asking.")

    optimization.add_argument("--requires", dest="requires", action="store_true", default=False,
                              help="Check install_requires")
    optimization.add_argument("--quiet", dest="quiet", action="store_true", default=False,
                              help="Activate quiet mode, working without logger.")

    optimization.add_argument("--requires-freeze", dest="requiresFreeze", action="store_true", default=False,
                              help="Check install_requires after register.")

    X = parser.add_argument_group("Zoomeye or Seebug")
    X.add_argument("--dork", dest="dork", action="store", default=None,
                   help="Zoomeye dork used for search.")
    X.add_argument("--max-page", dest="max_page", type=int, default=1,
                   help="Max page used in ZoomEye API(10 targets/Page).")
    X.add_argument("--search-type", dest="search_type", action="store", default='web,host',
                   help="search type used in ZoomEye API, web or host")
    X.add_argument("--vul-keyword", dest="vulKeyword", action="store", default=None,
                   help="Seebug keyword used for search.")
    X.add_argument("--ssv-id", dest="ssvid", action="store", default=None,
                   help="Seebug SSVID number for target PoC.")

    args = parser.parse_args()
    return args.__dict__
