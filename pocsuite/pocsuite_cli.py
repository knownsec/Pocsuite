#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import os
import sys
import time
import traceback
from pocsuite.api.x import Seebug
from pocsuite.api.x import ZoomEye
from pocsuite.lib.utils import versioncheck
from pocsuite.lib.core.common import unhandledExceptionMessage
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.common import banner
from pocsuite.lib.core.exception import PocsuiteUserQuitException
from pocsuite.lib.core.common import dataToStdout
from pocsuite.lib.core.common import setPaths
from pocsuite.lib.core.settings import LEGAL_DISCLAIMER
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.data import paths
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.data import cmdLineOptions
from pocsuite.lib.parse.parser import parseCmdOptions
from pocsuite.lib.core.option import initOptions
from pocsuite.lib.controller.controller import start
from pocsuite.lib.core.option import init
from pocsuite.lib.core.common import delModule
from pocsuite.lib.core.common import getUnicode
from pocsuite.lib.core.update import update


def main():
    """
    @function Main function of pocsuite when running from command line.
    """
    pcsInit()


def modulePath():
    """
    @function the function will get us the program's directory
    """
    return getUnicode(os.path.dirname(os.path.realpath(__file__)), sys.getfilesystemencoding())


def pcsInit(PCS_OPTIONS=None):
    try:
        paths.POCSUITE_ROOT_PATH = modulePath()
        setPaths()
        if not os.path.exists(paths.POCSUITE_HOME_PATH + '/.pocsuite'):
            os.mkdir(paths.POCSUITE_HOME_PATH + '/.pocsuite')
        if not os.path.exists(paths.POCSUITE_OUTPUT_PATH):
            os.mkdir(paths.POCSUITE_OUTPUT_PATH)

        argsDict = PCS_OPTIONS or parseCmdOptions()

        cmdLineOptions.update(argsDict)
        initOptions(cmdLineOptions)

        def doNothin(*args, **kw):
            return

        if conf.quiet:
            logger.log = doNothin

        banner()
        conf.showTime = True

        dataToStdout("[!] legal disclaimer: %s\n\n" % LEGAL_DISCLAIMER)
        dataToStdout("[*] starting at %s\n\n" % time.strftime("%X"))

        if argsDict['update']:
            update()
            return

        if argsDict['dork']:
            z = ZoomEye(paths.POCSUITE_RC_PATH)
            if z.newToken():
                logger.log(CUSTOM_LOGGING.SUCCESS, 'ZoomEye API authorization success.')
                z.resourceInfo()
            else:
                logger.log(CUSTOM_LOGGING.SUCCESS, 'ZoomEye API authorization failed,Please input Telnet404 Email account and Password for use ZoomEye API!')
                z.write_conf()
                if z.newToken():
                    logger.log(CUSTOM_LOGGING.SUCCESS, 'ZoomEye API authorization success.')
                    z.resourceInfo()
                else:
                    sys.exit(logger.log(CUSTOM_LOGGING.ERROR, 'ZoomEye API authorization failed, make sure correct credentials provided in "~/.pocsuiterc".'))

            info = z.resources
            logger.log(
                CUSTOM_LOGGING.SYSINFO,
                'Available ZoomEye web search limit count: {}, host search limit count: {}'.format(info['web-search'], info['host-search'])
            )

            tmpIpFile = paths.POCSUITE_OUTPUT_PATH + '/zoomeye_%s.txt' % time.strftime('%Y_%m_%d_%H_%M_%S')
            with open(tmpIpFile, 'w') as fp:
                search_types = argsDict.get('search_type', 'web')
                if 'host' not in search_types and 'web' not in search_types:
                    search_types = 'web'
                for page in range(argsDict.get('max_page', 1)):
                    for search_type in search_types.split(','):
                        if search_type in ['web', 'host']:
                            for ip in z.search(argsDict['dork'], page, search_type):
                                if type(ip) == list:
                                    fp.write('%s\n' % ip[0])
                                else:
                                    fp.write('%s\n' % ip)
            conf.urlFile = argsDict['urlFile'] = tmpIpFile

        if not any((argsDict['url'] or argsDict['urlFile'], conf.requires, conf.requiresFreeze)):
            errMsg = 'No "url" or "urlFile" or "dork" assigned.'
            sys.exit(logger.log(CUSTOM_LOGGING.ERROR, errMsg))

        if not any((argsDict['pocFile'], argsDict['vulKeyword'], argsDict['ssvid'])):
            errMsg = 'No "--url" or "--file" or "--vul-keyword" or "--ssv-id" assigned.'
            sys.exit(logger.log(CUSTOM_LOGGING.ERROR, errMsg))

        if argsDict['ssvid']:
            if not os.path.exists(paths.POCSUITE_MODULES_PATH):
                os.mkdir(paths.POCSUITE_MODULES_PATH)
            if not argsDict['ssvid'].isdigit():
                warnMsg = "Paramenter SSV ID must be integer number"
                logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
            else:
                s = Seebug(paths.POCSUITE_RC_PATH)
                if not s.newToken():
                    logger.log(CUSTOM_LOGGING.ERROR,
                               'Seebug API authorization failed, Please input Telnet404 Email account for use Seebug API，you can get it in [https://www.seebug.org/accounts/detail].')
                    s.write_conf()
                    if not s.static():
                        sys.exit(logger.log(CUSTOM_LOGGING.ERROR,
                                            'Seebug API authorization failed, make sure correct credentials provided in "~/.pocsuiterc".'))
                logger.log(CUSTOM_LOGGING.SUCCESS, 'Seebug API authorization succeed.')
                p = s.retrieve(argsDict['ssvid'])
                if 'code' in p:
                    tmp = '%s/%s.py' % (paths.POCSUITE_MODULES_PATH, argsDict['ssvid'])
                    with open(tmp, 'w') as fp:
                        fp.write(p['code'])
                    conf.pocFile = tmp
                else:
                    warnMsg = "Fetch SSV-ID '%s' PoC failed! Check your Telnet404 account API permission." % argsDict['ssvid']
                    logger.log(CUSTOM_LOGGING.WARNING, warnMsg)

        if argsDict['vulKeyword']:
            if not os.path.exists(paths.POCSUITE_MODULES_PATH):
                os.mkdir(paths.POCSUITE_MODULES_PATH)
            folderPath = '%s/%s' % (paths.POCSUITE_MODULES_PATH, argsDict['vulKeyword'])
            if not os.path.exists(folderPath):
                os.mkdir(folderPath)
            s = Seebug(paths.POCSUITE_RC_PATH)
            if not s.newToken():
                    logger.log(CUSTOM_LOGGING.ERROR, 'Seebug API authorization failed, Please input Telnet404 Email account for use Seebug API，you can get it in [https://www.seebug.org/accounts/detail].')
                    s.write_conf()
                    if not s.static():
                        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, 'Seebug API authorization failed, make sure correct credentials provided in "~/.pocsuiterc".'))
            logger.log(CUSTOM_LOGGING.SUCCESS, 'Seebug API authorization succeed.')
            logger.log(CUSTOM_LOGGING.SYSINFO, s.seek(argsDict['vulKeyword']))

            if len(s.pocs) == 0:
                infoMsg = "No available PoC for your Telnet404 account, Try exchange PoC on Seebug website!\n(https://www.seebug.org)"
                logger.log(CUSTOM_LOGGING.WARNING, infoMsg)

            for poc in s.pocs:
                p = s.retrieve(poc['id'])
                tmp = '%s/%s.py' % (folderPath, poc['id'])

                with open(tmp, 'w') as fp:
                    fp.write(p['code'])

        init()
        start()

    except PocsuiteUserQuitException:
        errMsg = "user quit"
        logger.log(CUSTOM_LOGGING.ERROR, errMsg)

    except KeyboardInterrupt:
        print
        errMsg = "user aborted"
        logger.log(CUSTOM_LOGGING.ERROR, errMsg)

    except EOFError:
        print
        errMsg = "exit"
        logger.log(CUSTOM_LOGGING.ERROR, errMsg)

    except SystemExit:
        pass

    except Exception, ex:
        print
        print ex
        # errMsg = unhandledExceptionMessage()
        # logger.log(CUSTOM_LOGGING.WARNING, errMsg)
        excMsg = traceback.format_exc()
        dataToStdout(excMsg)

    if 'pCollect' in kb:
        for p in kb.pCollect:
            delModule(p)

        if conf.get("showTime"):
            dataToStdout("\n[*] shutting down at %s\n\n" % time.strftime("%X"))

        kb.threadContinue = False
        kb.threadException = True

        if conf.get("threads", 0) > 1:
            os._exit(0)


if __name__ == "__main__":
    main()
