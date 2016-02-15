#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import os
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.data import paths
from pocsuite.lib.core.common import banner
from pocsuite.lib.core.settings import IS_WIN
from pocsuite.lib.core.common import filepathParser
from pocsuite.lib.core.option import initializeKb
from pocsuite.lib.core.option import registerPocFromDict
from pocsuite.lib.core.option import setMultipleTarget
from pocsuite.lib.core.option import _setHTTPUserAgent
from pocsuite.lib.core.option import _setHTTPReferer
from pocsuite.lib.core.option import _setHTTPCookies
from pocsuite.lib.core.option import _setHTTPProxy
from pocsuite.lib.core.option import _setHTTPTimeout
from pocsuite.lib.core.settings import HTTP_DEFAULT_HEADER
from pocsuite.lib.controller.check import pocViolation
from pocsuite.lib.controller.setpoc import setPoc
from pocsuite.lib.controller.controller import start
from pocsuite.thirdparty.cmd2.cmd2 import Cmd
from pocsuite.thirdparty.oset.pyoset import oset
from pocsuite.thirdparty.prettytable.prettytable import PrettyTable
from pocsuite.thirdparty.colorama.initialise import init as coloramainit

try:
    import readline
    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except:
    pass


def initializePoc(folders):
    # 加载文件夹下的poc时默认只加载modules目录下的, modules目录下可以新建文件夹, 如wordpress
    # 默认情况不加载wordpress文件夹内的poc
    # Usage: pcs-console.py modules/wordpress tests
    # 调用方式如上时可以将modules/wordpress 和 tests两个文件夹下的poc导入
    pocNumber = 0
    if not os.path.isdir(paths.POCSUITE_MODULES_PATH):
        os.makedirs(paths.POCSUITE_MODULES_PATH)
    folders.append(paths.POCSUITE_MODULES_PATH)
    for folder in folders:
        files = os.listdir(folder)
        for file in files:
            if file.endswith(".py") or file.endswith('.json') and "__init__" not in file:
                pocNumber += 1
                kb.unloadedList.update({pocNumber: os.path.join(folder, file)})


def avaliable():
    graph = PrettyTable(["pocId", "avaliablePocName", "Folder"])
    graph.align["PocsName"] = "m"
    graph.padding_width = 1

    for k, v in kb.unloadedList.iteritems():
        path, name = filepathParser(v)
        graph.add_row([k, name, os.path.relpath(path, paths.POCSUITE_ROOT_PATH)])

    print graph
    print


class baseConsole(Cmd):

    def __init__(self):
        if IS_WIN:
            coloramainit()
        Cmd.__init__(self)
        os.system("clear")
        banner()
        self.case_insensitive = False
        self.prompt = "Pcs> "

        conf.url = None
        conf.proxy = None
        conf.params = None
        conf.urlFile = None
        conf.agent = None
        conf.referer = None
        conf.cookie = None
        conf.proxy = None
        conf.randomAgent = False

        conf.threads = 1
        conf.timeout = 5
        conf.httpHeaders = HTTP_DEFAULT_HEADER

    def do_verify(self, args):
        conf.mode = 'verify'
        self._execute()

    def do_attack(self, args):
        conf.mode = 'attack'
        self._execute()

    def _execute(self):
        kb.results = oset()

        _setHTTPUserAgent()
        _setHTTPReferer()
        _setHTTPCookies()
        _setHTTPTimeout()

        registerPocFromDict()
        pocViolation()

        setMultipleTarget()
        _setHTTPProxy()

        start()

    def do_config(self, args):
        subConsole = configConsole()
        subConsole.cmdloop()

    def do_poc(self, args):
        subConsole = pocConsole()
        subConsole.cmdloop()

    def do_ls(self, args):
        if not args:
            print
            print "[Command]"
            print "   config       : register global configs. "
            print "   poc          : enter pocConsole, basic poc operation. "
            print
            print "[Mode]"
            print "   verify       : conducting verification. "
            print "   attack       : conduncting attack. "
            print
        else:
            self.do_help(args)

    def do_help(self, args):
        self.do_ls(args)

    pass


class configConsole(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = "Pcs.config> "
        self.case_insensitive = False

    def do_url(self, args):
        if not args:
            conf.url = raw_input('Pcs.config.url> ')
        else:
            conf.url = str(args)

    def do_thread(self, args):
        if not args:
            conf.threads = input('Pcs.config.threads> ')
        else:
            conf.threads = int(args)

    def do_urlfile(self, args):
        if not args:
            conf.urlFile = raw_input('Pcs.config.urlFile> ')
        else:
            conf.urlFile = str(args)

    def do_header(self, args):
        subConsole = headerConsole()
        subConsole.cmdloop()
        pass

    def do_proxy(self, args):
        if not args:
            conf.proxy = raw_input('Pcs.config.proxy> ')
        else:
            conf.proxy = str(args)
        pass

    def do_timeout(self, args):
        if not args:
            conf.timeout = raw_input('Pcs.config.timeout> ')
        else:
            conf.timeout = args
        conf.timeout = int(conf.timeout)
        pass

    def do_show(self, args):

        graph = PrettyTable(["config", "value"])
        graph.align["config"] = "l"

        for k, v in conf.iteritems():
            if v and k != 'httpHeaders':
                graph.add_row([k, v])
        print graph

    def do_ls(self, args):
        if not args:
            print
            print "[Command]"
            print "   thread       : set multiple threads. (Default 1) "
            print "   url          : set target url from stdin. "
            print "   urlFile      : set target url from urlFile. "
            print "   q            : return upper level. "
            print
            print "[Option]"
            print "   header       : set http headers for follow requests."
            print "   proxy        : set proxy. format: '(http|https|socks4|socks5)://address:port'."
            print "   timeout      : set max requests time. (Default 5s)"
            print "   show         : show config."
            print

    def do_help(self, args):
        self.do_ls(args)


class headerConsole(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = "Pcs.config.header> "
        self.case_insensitive = False

    def do_ls(self, args):
        if not args:
            print
            print "[Command]"
            print "   cookie       : set cookie for requests. "
            print "   referer      : set referer for requests. "
            print "   ua           : set ua for requests. "
            print "   q            : return upper level. "
            print
        pass

    def do_cookie(self, args):
        if not args:
            conf.cookie = raw_input('Pcs.config.header.cookie> ')
        else:
            conf.cookie = str(args)

    def do_referer(self, args):
        if not args:
            conf.referer = raw_input('Pcs.config.header.referer> ')
        else:
            conf.referer = str(args)

    def do_ua(self, args):
        if not args:
            conf.agent = raw_input('Pcs.config.header.user-agent> ')
        else:
            conf.agent = str(args)

    def do_help(self, args):
        self.do_ls(args)


class pocConsole(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = "Pcs.poc> "
        self.case_insensitive = False

    def do_ls(self, args):
        if not args:
            print
            print "[Command]"
            print "   avaliable    : list avaliable poc file(s)"
            print "   search       : search from avaliable poc file(s). "
            print "   load         : load specific poc file(s). "
            print "   loaded       : list all loaded poc file(s). "
            print "   unload       : list all unload poc files(s)."
            print "   clear        : unload all loaded poc file(s)."
            print "   q            : return upper level. "
            print

            pass
        else:
            do_help()

    def do_avaliable(self, args):
        avaliable()

    def do_load(self, args):
        if args.isdigit():
            conf.pocFile = kb.unloadedList[int(args)]
            del kb.unloadedList[int(args)]
            pass
        else:
            conf.pocFile = args

        setPoc()

        print '[*] load poc file(s) success!'
        print
        pass

    def do_loaded(self, args):
        registerPocFromDict()

        graph = PrettyTable(["pocId", "loadedPocsName"])
        graph.align["LoadedPocsName"] = "m"
        graph.padding_width = 1
        count = 0

        if hasattr(kb, 'registeredPocs') and getattr(kb, 'registeredPocs'):
            for poc in sorted(kb.registeredPocs.keys()):
                count += 1
                graph.add_row([count, poc])
        else:
            graph.add_row(["0", "None"])
        print graph
        print

    def do_unload(self, args):
        # TODO 补全
        graph = PrettyTable(["pocId", "unloadPocsName"])
        graph.align["unloadPocsName"] = "m"
        graph.padding_width = 1
        count = 0

        if hasattr(kb, 'unloadedList') and getattr(kb, 'unloadedList'):
            for no in sorted(kb.unloadedList.keys()):
                from ntpath import split
                graph.add_row([no, split(kb.unloadedList[no])[1]])
        else:
            graph.add_row(["0", "None"])
        print graph
        print

    def do_clear(self, args):
        initializeKb()
        pass

    def do_help(self, args):
        self.do_ls(args)

    def do_search(self, args):
        graph = PrettyTable(["pocId", "PocName"])
        graph.align["PocName"] = "m"
        graph.padding_width = 1

        for k, v in kb.unloadedList.iteritems():
            if str(args) in v:
                graph.add_row([k, filepathParser(v)[1]])
        print graph
        pass

    pass
