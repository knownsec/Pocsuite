#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import os
import time
import shutil
import tempfile
from textwrap import dedent
from pocsuite.lib.core.settings import REPORT_HTMLBASE
from pocsuite.lib.core.settings import REPORT_TABLEBASE
from pocsuite.lib.core.data import paths
from pocsuite.lib.core.exception import PocsuiteSystemException
from pocsuite.lib.core.exception import PocsuiteMissingPrivileges
from pocsuite.lib.core.common import getUnicode
from pocsuite.lib.core.common import reIndent
from pocsuite.lib.core.common import normalizeUnicode
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.handlejson import execReq
from pocsuite.lib.core.threads import runThreads
from pocsuite.thirdparty.prettytable.prettytable import PrettyTable


def cleanTrash():
    nowTime = time.time()
    for _ in os.listdir(paths.POCSUITE_TMP_PATH):
        tempFile = '%s/%s' % (paths.POCSUITE_TMP_PATH, _)
        if tempFile != '.keep' and (nowTime - os.stat(tempFile).st_mtime) / 3600 / 24 > 3:
            if os.path.isfile(tempFile):
                os.remove(tempFile)
            else:
                shutil.rmtree(tempFile)


def start():
    if kb.targets and kb.targets.qsize() > 1:
        infoMsg = "pocsuite got a total of %d targets" % kb.targets.qsize()
        logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)

    runThreads(conf.threads, pocThreads)

    resultTable = PrettyTable(["target-url", "poc-name", "poc-id", "component", "version", "status"])
    resultTable.align["target-url"] = "l"
    resultTable.padding_width = 1

    if not kb.results:
        return

    toNum, sucNum = 0, 0
    for row in kb.results:
        resultTable.add_row(list(row)[:-2])
        toNum += 1
        if row[5] == 'success':
            sucNum += 1

    if not conf.quiet:
        print resultTable
        # infoMsg = "{} of {} success !".format(sucNum, toNum)
        # logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
        print "success : {} / {}".format(sucNum, toNum)

    _createTargetDirs()
    _setRecordFiles()

    if conf.report:
        _setReport()


def pocThreads():
    """
    @function multiThread executing
    """
    kb.pCollect = set()

    while not kb.targets.empty() and kb.threadContinue:
        target, poc, pocname = kb.targets.get()
        infoMsg = "poc:'%s' target:'%s'" % (poc.name, target)
        logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
        # TODO json
        if isinstance(poc, dict):
            pocInfo = poc['pocInfo']
            result = execReq(poc, conf.mode, target)
            output = (target, pocname, pocInfo["vulID"], pocInfo["appName"], pocInfo["appVersion"], "success" if result else "failed", time.strftime("%Y-%m-%d %X", time.localtime()), str(result.result))
        else:
            kb.pCollect.add(poc.__module__)
            result = poc.execute(target, headers=conf.httpHeaders, mode=conf.mode, params=conf.params, verbose=False)
            if not result:
                continue
            result_status = "success" if result.is_success() else "failed"
            output = (target, pocname, result.vulID, result.appName, result.appVersion, result_status, time.strftime("%Y-%m-%d %X", time.localtime()), str(result.result))
            result.show_result()

        kb.results.add(output)
        if isinstance(conf.delay, (int, float)) and conf.delay > 0:
            time.sleep(conf.delay / 1000)


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
    for (target, pocname, pocid, component, version, status, r_time, result) in kb.results:
        if type(status) != str:
            status = status[1]
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
                    f.write("poc-name,poc-id,component,version,status,time,result")
            except IOError, ex:
                if "denied" in getUnicode(ex):
                    errMsg = "you don't have enough permissions "
                else:
                    errMsg = "something went wrong while trying "
                errMsg += "to write to the output directory '%s' (%s)" % (paths.POCSUITE_OUTPUT_PATH, ex)

                raise PocsuiteMissingPrivileges(errMsg)

        try:
            with open(recordFile, "a+") as f:
                f.write("\n" + ",".join([pocname, pocid, component, version, status, r_time, result]))
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
    td = "<tr class='status' onclick='showDetail(this)'>%s</tr>" % tdPiece
    detail = "<tr class=\"result0\"><td colspan=\"6\">%s</td></tr>"
    tables = ""
    reportTable = dedent(REPORT_TABLEBASE)
    reportHtml = dedent(REPORT_HTMLBASE)
    for _ in kb.results:
        tdStr = td % _[:-2]
        detailStr = ""
        if _[-1]:
            result_obj = eval(_[-1])
            if result_obj:
                detailStr = "<dl>"
                for outkey in result_obj.keys():
                    items = "<dt>%s</dt>" % (outkey)
                    vals = result_obj.get(outkey)
                    for innerkey in vals.keys():
                        items += "<dd>%s: %s</dd>" % (innerkey, vals.get(innerkey))
                    detailStr += items
                detailStr += "</dl>"
        if detailStr:
            tdStr += detail % detailStr
        tables += reportTable % reIndent(tdStr, 4)
    html = reportHtml % (reIndent(thStr, 19), reIndent(tables, 16))

    with open(conf.report, 'w') as f:
        f.write(html)
