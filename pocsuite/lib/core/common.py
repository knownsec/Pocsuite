#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import os
import re
import sys
import imp
import ntpath
import locale
import inspect
import posixpath
import marshal
import unicodedata
import time
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.convert import stdoutencode
from pocsuite.lib.core.log import LOGGER_HANDLER
from pocsuite.lib.core.data import paths
from pocsuite.lib.core.exception import PocsuiteGenericException
from pocsuite.thirdparty.odict.odict import OrderedDict
from pocsuite.lib.core.settings import (BANNER, GIT_PAGE, ISSUES_PAGE, PLATFORM, PYVERSION, VERSION_STRING)
from pocsuite.lib.core.settings import UNICODE_ENCODING, INVALID_UNICODE_CHAR_FORMAT
from pocsuite.lib.core.exception import PocsuiteSystemException
from pocsuite.thirdparty.termcolor.termcolor import colored


class StringImporter(object):

    """
    Use custom meta hook to import modules available as strings.
    Cp. PEP 302 http://www.python.org/dev/peps/pep-0302/#specification-part-2-registering-hooks
    """

    def __init__(self, fullname, contents):
        self.fullname = fullname
        self.contents = contents

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__file__ = "<%s>" % fullname
        mod.__loader__ = self
        if conf.isPycFile:
            code = marshal.loads(self.contents[8:])
        else:
            code = compile(self.contents, mod.__file__, "exec")
        exec code in mod.__dict__
        return mod


def delModule(modname, paranoid=None):
    from sys import modules
    try:
        thismod = modules[modname]
    except KeyError:
        raise ValueError(modname)
    these_symbols = dir(thismod)
    if paranoid:
        try:
            paranoid[:]  # sequence support
        except:
            raise ValueError('must supply a finite list for paranoid')
        else:
            these_symbols = paranoid[:]
    del modules[modname]
    for mod in modules.values():
        try:
            delattr(mod, modname)
        except AttributeError:
            pass
        if paranoid:
            for symbol in these_symbols:
                if symbol[:2] == '__':  # ignore special symbols
                    continue
                try:
                    delattr(mod, symbol)
                except AttributeError:
                    pass


def banner():
    """
    Function prints pocsuite banner with its version
    """
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = re.sub("\033.+?m", "", _)
    dataToStdout(_)


def dataToStdout(data, bold=False):
    """
    Writes text to the stdout (console) stream
    """
    if 'quiet' not in conf or not conf.quiet:
        message = ""

        if isinstance(data, unicode):
            message = stdoutencode(data)
        else:
            message = data

        sys.stdout.write(setColor(message, bold))

        try:
            sys.stdout.flush()
        except IOError:
            pass
    return


def setColor(message, bold=False):
    retVal = message

    if message and getattr(LOGGER_HANDLER, "is_tty", False):  # colorizing handler
        if bold:
            retVal = colored(message, color=None, on_color=None, attrs=("bold",))

    return retVal


def unhandledExceptionMessage():
    """
    Returns detailed message about occurred unhandled exception
    """

    errMsg = "unhandled exception occurred in %s. It is recommended to retry your " % VERSION_STRING
    errMsg += "run with the latest development version from official Gitlab "
    errMsg += "repository at '%s'. If the exception persists, please open a new issue " % GIT_PAGE
    errMsg += "at '%s' " % ISSUES_PAGE
    errMsg += "with the following text and any other information required to "
    errMsg += "reproduce the bug. The "
    errMsg += "developers will try to reproduce the bug, fix it accordingly "
    errMsg += "and get back to you\n"
    errMsg += "pocsuite version: %s\n" % VERSION_STRING[VERSION_STRING.find('/') + 1:]
    errMsg += "Python version: %s\n" % PYVERSION
    errMsg += "Operating system: %s\n" % PLATFORM
    errMsg += "Command line: %s\n" % re.sub(r".+?\bpocsuite.py\b", "pocsuite.py", " ".join(sys.argv))

    return errMsg


def filepathParser(path):
    return ntpath.split(ntpath.splitext(path)[0])


def changeToPyImportType(path):
    """
    >>> changeToPyImportType('/path/to/module.py')
    'path.to.module'
    >>> changeToPyImportType('path/to/module.py')
    'path.to.module'
    >>> changeToPyImportType('path/to')
    'path.to'
    """

    return ntpath.splitext(path)[0].strip("/").replace("/", ".")


def multipleReplace(text, adict):
    rx = re.compile("|".join(map(re.escape, adict)))

    def oneXlat(match):
        return adict[match.group(0)]
    return rx.sub(oneXlat, text)


def getUnicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if noneToNull and value is None:
        return u'NULL'

    if isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, UNICODE_ENCODING)
                except:
                    value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances


def isListLike(value):
    """
    Returns True if the given value is a list-like instance

    >>> isListLike([1, 2, 3])
    True
    >>> isListLike(u'2')
    False
    """

    return isinstance(value, (list, tuple, set))


def readFile(filename):
    try:
        with open(filename) as f:
            retVal = f.read()
    except IOError, ex:
        errMsg = "something went wrong while trying to read "
        errMsg += "the input file ('%s')" % ex
        raise PocsuiteGenericException(errMsg)
    return retVal


def writeFile(filename, data):
    try:
        with open(filename, "w") as f:
            f.write(data)
    except IOError, ex:
        errMsg = "something went wrong while trying to write "
        errMsg += "to the output file ('%s')" % ex
        raise PocsuiteGenericException(errMsg)


def setPaths():
    """
    Sets absolute paths for project directories and files
    """

    paths.POCSUITE_DATA_PATH = os.path.join(paths.POCSUITE_ROOT_PATH, "data")

    paths.USER_AGENTS = os.path.join(paths.POCSUITE_DATA_PATH, "user-agents.txt")
    paths.WEAK_PASS = os.path.join(paths.POCSUITE_DATA_PATH, "password-top100.txt")
    paths.LARGE_WEAK_PASS = os.path.join(paths.POCSUITE_DATA_PATH, "password-top1000.txt")

    _ = os.path.join(os.path.expanduser("~"), ".pocsuite")
    paths.POCSUITE_OUTPUT_PATH = getUnicode(paths.get("POCSUITE_OUTPUT_PATH", os.path.join(_, "output")), encoding=sys.getfilesystemencoding())

    paths.POCSUITE_MODULES_PATH = os.path.join(_, "modules")
    paths.POCSUITE_TMP_PATH = os.path.join(paths.POCSUITE_MODULES_PATH, "tmp")
    paths.POCSUITE_HOME_PATH = os.path.expanduser("~")
    paths.POCSUITE_RC_PATH = paths.POCSUITE_HOME_PATH + "/.pocsuiterc"


def getFileItems(filename, commentPrefix='#', unicode_=True, lowercase=False, unique=False):
    """
    @function returns newline delimited items contained inside file
    """

    retVal = list() if not unique else OrderedDict()

    checkFile(filename)

    try:
        with open(filename, 'r') as f:
            for line in (f.readlines() if unicode_ else f.xreadlines()):
                # xreadlines doesn't return unicode strings when codecs.open() is used
                if commentPrefix and line.find(commentPrefix) != -1:
                    line = line[:line.find(commentPrefix)]

                line = line.strip()

                if not unicode_:
                    try:
                        line = str.encode(line)
                    except UnicodeDecodeError:
                        continue

                if line:
                    if lowercase:
                        line = line.lower()

                    if unique and line in retVal:
                        continue

                    if unique:
                        retVal[line] = True

                    else:
                        retVal.append(line)

    except (IOError, OSError, MemoryError), ex:
        errMsg = "something went wrong while trying "
        errMsg += "to read the content of file '%s' ('%s')" % (filename, ex)
        raise PocsuiteSystemException(errMsg)

    return retVal if not unique else retVal.keys()


def checkFile(filename):
    """
    @function Checks for file existence and readability
    """

    valid = True

    if filename is None or not os.path.isfile(filename):
        valid = False

    if valid:
        try:
            with open(filename, "rb"):
                pass
        except:
            valid = False

    if not valid:
        raise PocsuiteSystemException("unable to read file '%s'" % filename)


def choosePocType(filepath):
    """
    @function choose '.py' or '.json' extension to load the poc file
    """
    return ntpath.splitext(filepath)[1][1:]


def safeExpandUser(filepath):
    """
    @function Patch for a Python Issue18171 (http://bugs.python.org/issue18171)
    """

    retVal = filepath

    try:
        retVal = os.path.expanduser(filepath)
    except UnicodeDecodeError:
        _ = locale.getdefaultlocale()
        retVal = getUnicode(os.path.expanduser(filepath.encode(_[1] if _ and len(_) > 1 else UNICODE_ENCODING)))

    return retVal


def parseTargetUrl(url):
    """
    Parse target URL
    """
    retVal = url

    if not re.search("^http[s]*://", retVal, re.I) and not re.search("^ws[s]*://", retVal, re.I):
        if re.search(":443[/]*$", retVal):
            retVal = "https://" + retVal
        else:
            retVal = "http://" + retVal

    return retVal


def normalizePath(filepath):
    """
    Returns normalized string representation of a given filepath

    >>> normalizePath('//var///log/apache.log')
    '//var/log/apache.log'
    """

    retVal = filepath

    if retVal:
        retVal = retVal.strip("\r\n")
        retVal = ntpath.normpath(retVal) if isWindowsDriveLetterPath(retVal) else posixpath.normpath(retVal)

    return retVal


def isWindowsDriveLetterPath(filepath):
    """
    Returns True if given filepath starts with a Windows drive letter

    >>> isWindowsDriveLetterPath('C:\\boot.ini')
    True
    >>> isWindowsDriveLetterPath('/var/log/apache.log')
    False
    """

    return re.search("\A[\w]\:", filepath) is not None


def normalizeUnicode(value):
    """
    Does an ASCII normalization of unicode strings
    Reference: http://www.peterbe.com/plog/unicode-to-ascii

    >>> normalizeUnicode(u'\u0161u\u0107uraj')
    'sucuraj'
    """

    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore') if isinstance(value, unicode) else value


def getPublicTypeMembers(type_, onlyValues=False):
    """
    Useful for getting members from types (e.g. in enums)

    >>> [_ for _ in getPublicTypeMembers(OS, True)]
    ['Linux', 'Windows']
    """

    for name, value in inspect.getmembers(type_):
        if not name.startswith('__'):
            if not onlyValues:
                yield (name, value)
            else:
                yield value


def reIndent(s, numSpace):
    leadingSpace = numSpace * ' '
    lines = [leadingSpace + line for line in s.splitlines()]
    return '\n'.join(lines)


def poll_process(process, suppress_errors=False):
    """
    Checks for process status (prints . if still running)
    """

    while True:
        dataToStdout(".")
        time.sleep(1)

        returncode = process.poll()

        if returncode is not None:
            if not suppress_errors:
                if returncode == 0:
                    dataToStdout(" done\n")
                elif returncode < 0:
                    dataToStdout(" process terminated by signal %d\n"
                                 % returncode)
                elif returncode > 0:
                    dataToStdout(" quit unexpectedly with return code %d\n"
                                 % returncode)
            break
