#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import os
from cmd import Cmd

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
    pocNumber = 0
    if not os.path.isdir(paths.POCSUITE_MODULES_PATH):
        os.makedirs(paths.POCSUITE_MODULES_PATH)
    folders.append(paths.POCSUITE_MODULES_PATH)
    folders = [_ for _ in folders if os.path.isdir(_)]

    for folder in folders:
        for fname in os.listdir(folder):
            fname_lower = fname.lower()

            if fname_lower in ("__init__.py"):
                next
            elif fname_lower.endswith(".py") or fname_lower.endswith('.json'):
                pocNumber += 1
                kb.unloadedList.update({
                    pocNumber: os.path.join(folder, fname)
                })


class BaseInterpreter(Cmd):
    ruler = '='
    lastcmd = ''
    intro = None
    doc_leader = ''
    doc_header = 'Core Commands Menu (help <command> for details)'
    misc_header = 'Miscellaneous help topics:'
    undoc_header = 'No help on following command(s)'

    def __init__(self):
        Cmd.__init__(self)
        self.do_help.__func__.__doc__ = "Show help menu"

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt."""
        if self.lastcmd:
            return self.onecmd(self.lastcmd)

    def default(self, line):
        """Called on an input line when the cmd prefix is not recognized."""
        pass
        # return line

    def precmd(self, line):
        """Hook method executed just before the command line is interpreted,
        but after the input prompt is generated and issued"""
        return line

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        return stop

    def preloop(self):
        """Hook method executed once when the cmdloop() method is called."""
        pass

    def postloop(self):
        """Hook method executed once when the cmdloop() method is
        about to return"""
        pass

    def shell_will_go(self):
        try:
            self.cmdloop()
        except KeyboardInterrupt:
            print

    def print_topics(self, header, cmds, cmdlen, maxcol):
        """make help menu more readable"""
        if cmds:
            self.stdout.write(header)
            self.stdout.write("\n")
            if self.ruler:
                self.stdout.write(self.ruler * len(header))
                self.stdout.write("\n")

            for cmd in cmds:
                help_msg = getattr(self, "do_{}".format(cmd)).__doc__
                self.stdout.write("{:<16}".format(cmd))
                self.stdout.write(help_msg)
                self.stdout.write("\n")
            self.stdout.write("\n")


class PocsuiteInterpreter(BaseInterpreter):
    def __init__(self):
        if IS_WIN:
            coloramainit()
        BaseInterpreter.__init__(self)

        conf.report = False
        conf.retry = False
        conf.delay = 0
        conf.quiet = False
        conf.isPocString = False
        conf.isPycFile = False
        conf.requires = False
        conf.requiresFreeze = False

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

        self.prompt = "Pocsuite> "
        banner()
        self.case_insensitive = False
        self.showcommands = [_ for _ in dir(self) if _.startswith('show_')]

    def exploit(self):
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

    def do_verify(self, args):
        """Verify Mode, checks if a vuln exists or not"""
        conf.mode = 'verify'
        self.exploit()

    def do_attack(self, args):
        """Attack mode, sends exploit payload"""
        conf.mode = 'attack'
        self.exploit()

    def do_back(self, line):
        """Move back from the current Interpreter"""
        return True

    def do_banner(self, line):
        """Display an awesome framework banner"""
        banner()

    def do_exit(self, line):
        """Exit the current interpre"""
        return True

    def do_load(self, line):
        """Load specific poc file(s)."""
        if line.isdigit():
            conf.pocFile = kb.unloadedList[int(line)]
            del kb.unloadedList[int(line)]
        else:
            conf.pocFile = line

        conf.pocname = os.path.split(conf.pocFile)[1]
        setPoc()
        print '[*] load poc file(s) success!'

    def do_set(self, line):
        """Set key equal to value"""
        key, value, pairs = self.parseline(line)

        if (not key) or (not value):
            self.help_set()
            return False

        if key in conf:
            conf[key] = value

    def do_show(self, line):
        """Show available options / modules"""
        key, value, pairs = self.parseline(line)

        if (not key):
            self.help_show()
            return False

        method = 'show_{}'.format(key)
        # commands = [_ for _ in dir(self) if _.startswith('show_')]
        if method in self.showcommands and hasattr(self, method):
            func = getattr(self, method)
            func()

    def complete_set(self, line, text, *ignored):
        """Tab complete set"""
        keys = []
        if line:
            keys = [_ for _ in conf.keys() if _.startswith(line)]
        else:
            keys = conf.keys()
        return keys

    def available_show_completion(self, text):
        """Match all possible show commands"""
        return filter(lambda x: x.startswith(text), self.showcommands)

    def complete_show(self, line, text, *ignored):
        """Tab complete show"""
        if line:
            line = "show_{}".format(line)
            methods = self.available_show_completion(line)
        else:
            methods = self.showcommands

        return map(lambda x: x.replace('show_', ''), methods)

    def show_options(self):
        """Show options"""
        msg_format = "  {:>12} {:<32} "
        print
        print(msg_format.format('OPTION-KEY', 'OPTION-VALUE'))
        print(msg_format.format('==========', '============'))
        for i in conf.items():
            print(msg_format.format(*i))
        print

    def show_pocs(self):
        """Show all available pocs"""
        msg_format = "  {:>12} {:<32} "
        print
        print(msg_format.format('POC-ID', 'POC-PATH'))
        print(msg_format.format('======', '========'))
        for i in kb.unloadedList.items():
            print(msg_format.format(*i))
        print

    def help_back(self):
        print
        print('  Usage : back')
        print('  Desp  : {}'.format(getattr(self, 'do_back').__doc__))
        print('  Demo  : back')
        print

    def help_set(self):
        print
        print('  Usage :  set <key> <value>')
        print('  Desp  :  {}'.format(getattr(self, 'do_set').__doc__))
        print('  Demo  :  set threads 1')
        print

    def help_show(self):
        """Show available options / pocs"""
        print
        print('  Usage : show | show <options | pocs>')
        print('  Desp  : {}'.format(getattr(self, 'do_show').__doc__))
        print('  Demo  : show options')
        print
