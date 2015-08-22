#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pocsuite.net import req
from pocsuite.poc import Output, POCBase
from pocsuite.utils import register


class TestPOC(POCBase):
    vulID = 'example2'  # vul ID
    version = '1'
    author = 'test'
    vulDate = '2014-04-08'
    createDate = '2014-04-08'
    updateDate = '2014-04-08'
    references = ['http://drops.wooyun.org/papers/1381']
    name = 'test xxx'
    appPowerLink = 'www.test.org'
    appName = 'testkd'
    appVersion = '1.0'
    vulType = 'Information Disclosure'
    desc = '''
        安全人员表示：无需任何特权信息或身份验证，
        我们就可以从我们自己的（测试机上）偷来X.509证书的私钥、
        用户名与密码、聊天工具的消息、电子邮件以及重要的商业文档和通信等数据。
    '''
    # the sample sites for examine
    samples = ['http://www.baidu.com', 'http://www.qq.com']
  
    def _attack(self):
        response = req.get(self.url, timeout=10, headers={'123': '23'})
        return self.parse_attack(response)

    def _verify(self):
        return self._attack()

    def parse_attack(self, response):
        output = Output(self)
        result = {}
        if response:
            result['FileInfo'] = {}
            result['FileInfo']['Filename'] = response
            result['FileInfo']['Filecontent'] = 'test123' * 10
            output.success(result)
        else:
            output.fail('Internet Nothing returned')
        return output


register(TestPOC)
