#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

import os
import re
import time
import tempfile
from textwrap import dedent
from lib.core.settings import REPORT_HTMLBASE
from lib.core.settings import REPORT_TABLEBASE
from lib.core.data import paths
from lib.core.exception import PocsuiteSystemException
from lib.core.exception import PocsuiteMissingPrivileges
from lib.core.common import getUnicode
from lib.core.common import reIndent
from lib.core.common import normalizeUnicode
from lib.core.data import logger
from lib.core.data import conf
from lib.core.data import kb
from lib.core.enums import CUSTOM_LOGGING
from lib.core.handlejson import execReq
from lib.core.threads import runThreads
from thirdparty.prettytable.prettytable import PrettyTable

from lib.core.poc import POCBase
from lib.core.poc import Output
from lib.core.register import addSysPath
from lib.core.common import parseTargetUrl


def start():
    if kb.targets and kb.targets.qsize() > 1:
        infoMsg = "pocsuite got a total of %d targets" % kb.targets.qsize()
        logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)

    runThreads(conf.threads, pocThreads)

    resultTable = PrettyTable(["target-url", "poc-name", "poc-id", "component", "version", "status"])
    resultTable.padding_width = 1

    if not kb.results:
        return

    for row in kb.results:
        resultTable.add_row(list(row)[:-1])

    print resultTable

    _createTargetDirs()
    _setRecordFiles()

    if conf.report:
        _setReport()

def pocThreads():
    """
    @function multiThread executing
    """
    while not kb.targets.empty() and kb.threadContinue:
        target, poc, pocname = kb.targets.get()


        infoMsg = "poc:'%s' target:'%s'" % (pocname, target)
        logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
        # TODO json
        if isinstance(poc, dict):
            pocInfo, pocDevil = poc['pocInfo'], poc["pocExecute"]
            result = execReq(poc, conf.mode, target)
            output = (target, pocname, pocInfo["vulID"], pocInfo["appName"], pocInfo["appVersion"], "success" if result else "failed", time.strftime("%Y-%m-%d %X", time.localtime()))
        elif isinstance(poc, POCBase):
            result = poc.execute(target, headers=conf.httpHeaders, mode=conf.mode, params=conf.params, verbose=True)
            output = (target, pocname, result.vulID, result.appName, result.appVersion, "success" if result.is_success() else "failed", time.strftime("%Y-%m-%d %X", time.localtime()))
            result.show_result()
        else:
            addSysPath(poc)
            try:
                module = __import__(pocname, fromlist=['*'])
            except ImportError, ex:
                errMsg = "%s register failed \"%s\"" % (poc, str(ex))
                logger.log(CUSTOM_LOGGING.ERROR, errMsg)

            module.io_info['URL'] = parseTargetUrl(target)
            module.main(module.io_info)

            result = Output()
            result.url, result.vulID, result.name = target, '', pocname

            if module.io_info['Status']:
                result.success(module.io_info['Result'])
            else:
                result.fail('Not vulnerable.')
            result.show_result()

            output = (target, pocname, 'N/A', 'N/A', 'N/A', 'success' if module.io_info['Status'] else 'failure', time.strftime("%Y-%m-%d %X", time.localtime()))

        kb.results.add(output)


def _createTargetDirs():
    """
    Create the output directory.
    """
    if not os.path.isdir(paths.POCSUITE_OUTPUT_PATH):
        try:
            if not os.path.isdir(paths.POCSUITE_OUTPUT_PATH):
                os.makedirs(paths.POCSUITE_OUTPUT_PATH, 0755)
            warnMsg = "using '%s' as the output directory" % paths.POCSUITE_OUTPUT_PATH
            logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
        except (OSError, IOError), ex:
            try:
                tempDir = tempfile.mkdtemp(prefix="pocsuiteoutput")
            except Exception, _:
                errMsg = "unable to write to the temporary directory ('%s'). " % _
                errMsg += "Please make sure that your disk is not full and "
                errMsg += "that you have sufficient write permissions to "
                errMsg += "create temporary files and/or directories"
                raise PocsuiteSystemException(errMsg)

            warnMsg = "unable to create regular output directory "
            warnMsg += "'%s' (%s). " % (paths.POCSUITE_OUTPUT_PATH, getUnicode(ex))
            warnMsg += "Using temporary directory '%s' instead" % getUnicode(tempDir)
            logger.log(CUSTOM_LOGGING.WARNING, warnMsg)

            paths.POCUSITE_OUTPUT_PATH = tempDir


def _setRecordFiles():
    for (target, pocname, pocid, component, version, status, time) in kb.results:
        outputPath = os.path.join(getUnicode(paths.POCSUITE_OUTPUT_PATH), normalizeUnicode(getUnicode(target)))

        if not os.path.isdir(outputPath):
            try:
                os.makedirs(outputPath, 0755)
            except (OSError, IOError), ex:
                try:
                    tempDir = tempfile.mkdtemp(prefix="pocsuitetoutput")
                except Exception, _:
                    errMsg = "unable to write to the temporary directory ('%s'). " % _
                    errMsg += "Please make sure that your disk is not full and "
                    errMsg += "that you have sufficient write permissions to "
                    errMsg += "create temporary files and/or directories"
                    raise PocsuiteSystemException(errMsg)

                warnMsg = "unable to create output directory "
                warnMsg += "'%s' (%s). " % (outputPath, getUnicode(ex))
                warnMsg += "Using temporary directory '%s' instead" % getUnicode(tempDir)
                logger.warn(warnMsg)

                outputPath = tempDir

        recordFile = os.path.join(outputPath, "record.txt")

        if not os.path.isfile(recordFile):
            try:
                with open(recordFile, "w") as f:
                    f.write("poc-name,poc-id,component,version,status,time")
            except IOError, ex:
                if "denied" in getUnicode(ex):
                    errMsg = "you don't have enough permissions "
                else:
                    errMsg = "something went wrong while trying "
                errMsg += "to write to the output directory '%s' (%s)" % (paths.POCSUITE_OUTPUT_PATH, ex)

                raise PocsuiteMissingPrivileges(errMsg)

        try:
            with open(recordFile, "a+") as f:
                f.write("\n" + ",".join([pocname, pocid, component, version, status, time]))
        except IOError, ex:
            if "denied" in getUnicode(ex):
                errMsg = "you don't have enough permissions "
            else:
                errMsg = "something went wrong while trying "
            errMsg += "to write to the output directory '%s' (%s)" % (paths.POCSUITE_OUTPUT_PATH, ex)

            raise PocsuiteMissingPrivileges(errMsg)


def _setReport():
    tdPiece = thStr = ""
    for _ in ("target-url", "poc-name", "poc-id", "component", "version", "status"):
        tdPiece += " <td>%s</td> "
        thStr += " <th>%s</td> " % _
    td = "<tr>%s</tr>" % tdPiece
    tables = ""
    reportTable = dedent(REPORT_TABLEBASE)
    reportHtml = dedent(REPORT_HTMLBASE)
    for _ in kb.results:
        tdStr = td % _[:-1]
        tables += reportTable % reIndent(tdStr, 4)
    html = reportHtml % (reIndent(thStr, 19), reIndent(tables, 16))

    with open(conf.report, 'w') as f:
        f.write(html)
