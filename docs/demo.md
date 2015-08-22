PoC 开发文档
---
---
 
## 关于 Pocsuite

Pocsuite 是知道创宇安全研究团队打造的一款基于漏洞与 POC 的漏洞验证框架。Pocsuite 是知道创宇安全研究团队发展的基石，是团队发展至今持续维护的一个重要项目，保障了我们的 Web 安全研究能力的领先。

在获取到相关漏洞详情后，任何有一定 Python 开发基础的人都可以基于 Pocsuite 开发出对应漏洞的 POC 或者 Exp ，轻而易举的就可以直接使用 Pocsuite 进行相关的验证和调用，而无需考虑底层代码架构等。

在 Sebug 重新改版上线之际，知道创宇安全研究团队正式对外开放 Pocsuite 框架，任何安全研究人员都可以基于 Pocsuite 进行 POC 或者 Exp 的开发，同时也可以加入 Sebug 漏洞社区，为 Pocsuite 提供贡献或者贡献相关的 PoC。具体的开发文档可以参考下文。

## 文档目录
* 简介
* 框架
    * 获取
    * 安装
    * 使用
* 编写 PoC
 * PoC 编写规范
 * PoC 命名规范
 * 漏洞类型规范
 * PoC 编写注意事项
* 演示视频

## 简介

此文档将详细描述如何使用 Pocsuite 框架。基于 Pocsuite 这个框架，你可以编写出属于你自己的 POC。

## 框架

项目地址：https://github.com/knownsec/pocsuite

### 获取pocsuite：

* Clone 代码

    ```bash
$ git clone git@github.com:knownsec/pocsuite.git
    ```

* 或者直接下载并解压

    ```bash
$ wget https://github.com/knownsec/pocsuite/archive/master.zip
$ unzip master.zip
    ```

目录结构：

```
pocsuite-sebug
├── docs #说明文档
├── POCAPI.md #POC编写规范及相关API
├── pocsuite #pocsuite主程序
│   ├── data #基础数据
│   ├── lib        
│   │   ├── controller		
│   │   ├── core #核心组件
│   │   ├── parse #参数处理封装
│   │   ├── request #网络请求封装
│   │   └── utils #常用工具包
│   ├── modules
│   │   └── tmp #临时目录
│   ├── pcs-attack.py #攻击程序
│   ├── pcs-console.py #控制台程序
│   ├── pcs-verify.py #验证程序
│   ├── pocsuite.py #pocsuite主入口程序
│   ├── tests #测试poc目录
│   └── thirdparty #第三方库
└── README.md
```

### 安装框架

解压缩 pocsuite-sebug 后，无需安装，切换至 pocsuite 目录即可使用。在命令行输入

```bash
$ python pocsuite.py --version

                              ,--. ,--.         
 ,---. ,---. ,---.,---.,--.,--`--,-'  '-.,---.  {0.3-sebug-b30225e}
| .-. | .-. | .--(  .-'|  ||  ,--'-.  .-| .-. : 
| '-' ' '-' \ `--.-'  `'  ''  |  | |  | \   --. 
|  |-' `---' `---`----' `----'`--' `--'  `----'  
`--'                                            http://sebug.net
```

### 使用

pocsuite支持命令行模式(cli)和交互式控制台模式(console)

#### 命令行模式

命令行模式可以对目标发起快速检测和攻击,

进入pocsuite目录,执行pocsuite.py

获取命令帮助列表

```bash
python pocsuite.py -h
```


假定你已经有一个poc(poc_example.py),并且将基保存在test目录下面:
<font color=red>POC目前支持.py和.json两种，两者使用方法完全一样</font>

* 验证目标是否存在漏洞:

    ```bash
python pocsuite.py -r test/poc_example.py -u http://www.example.com/ --verify
    ```

* 加载poc直接get shell:

    ```bash
python pocsuite.py -r test/poc_example.py -u http://www.example.com/ --attack
    ```

* 如果你有一个url文件(url.txt),要批量验证,你可以:

    ```bash
python pocsuite.py -r test/poc_example.py -f url.txt --verify
    ```
    > 批量get shell 只需要替换 **--verify** 参数为 **--attack** 即可.

* 加载test目录下的所有poc对目标测试:

    ```bash
python pocsuite.py -r test/ -u http://www.example.com --verify
    ```

* 使用多线程,默认线程数为1:

    ```bash
python pocsuite.py -r test/ -f url.txt --verify --threads 10
    ```

#### 控制台交互式视图

进入控制台交互式视图:

    ```bash
python pcs-console.py
    ```

在**Pcs视图**(Pcs>)下,常用的命令:

```bash
ls, help        展示出当前可用的命令
config          进入目标配置子视图
poc             进入poc配置子视图
verify          开始验证
attack          开始攻击
shell [command] 执行系统shell命令
hi, history     历史命令
q, exit , eof   退出
show            显示当前系统设置
set             修改系统设置
shortcuts       查看短命令
  
```

在config视图(Pcs.Config>)下,常用的命令:

```bash
[Command]
   thread       : 设置最大线程数(默认为1) 
   url          : 设置目标URL
   urlFile      : 载入文件中的URL 
   q            : 返回父视图 
[Option]
   header       : 设置 http 请求头.
   proxy        : 设置代理. 格式: '(http|https|socks4|socks5)://address:port'.
   timeout      : 设置超时时间. (默认 5s)
   show         : 显示当前配置.

```

在poc视图(Pcs.poc>)下,常用的命令:

```bash
avaliable   查看所有可用的POC
search      从可用的POC列表中检索
load <Id>   加载指定Id的POC
loaded      查看已经加载的POC   
unload      查看未加载的POC 
clear       移出所有已加载的POC
```


#### 使用pcs-console验证/攻击步骤:

1. 进入Config子视图,设置目标：

    ```bash
Pcs.Config>url
Pcs.config.url>www.example.com
Pcs.Config>show
+---------+-----------------+
|  config |      value      |
+---------+-----------------+
|   url   | www.example.com |
| threads |        1        |
+---------+-----------------+
 或
Pcs.Config>url example.com
Pcs.Config>show
+---------+-------------+
|  config |    value    |
+---------+-------------+
|   url   | example.com |
| threads |      1      |
+---------+-------------+
    ```
 
2. 进入 poc子视图，加载指定POC

    ```bash
Pcs>poc
Pcs.poc>avaliable
+-------+------------------+
| pocId | avaliablePocName |
+-------+------------------+
|   1   | _poc_example1.py |
|   2   | poc_example1.py  |
+-------+------------------+
Pcs.poc>load 1
[*] load poc file(s) success!
Pcs.poc>q
    ```

3. 验证/攻击

    ```bash
Pcs>verify
[15:13:26] [*] starting 1 threads
[15:13:26] [*] poc:'_poc_example1' target:'www.example.com'
    ```

#### POC报告自动生成

pocsuite 默认只会将执行结果输出显示在屏幕上，如需将结果自动生成报告并保存，在扫描参数后加 --report [report_file] 即可生成 html格式报告。

```bash
python pocsuite.py -r tests/poc_example2.py -u example.com --verify --report /tmp/report.html
```

上述命令执行后，会调用poc_example2.py并将结果保存到/tmp/report.html中。


### 编写 POC

Pocsuite 是一个 Python 开发的 PoC 框架, 支持python和json两种poc编写方式．

#### PyPOC编写规范

**本小节介绍**
pypoc即使用python语言来编写POC

> 特别注意：编写的代码要尽可能符合 PEP8 规范，严格规范 4 个空格为缩进！相关规范可以参考 [PythonCodingRule](http://blog.knownsec.com/Knownsec_RD_Checklist/PythonCodingRule.pdf)。

1. 新建 .py 文件，导入相关模块，新建继承框架的基础类 TestPOC(POCBase)

    ```python
    #!/usr/bin/env python
    # coding: utf-8

    from pocsuite.net import req
    from pocsuite.poc import POCBase, Output
    from pocsuite.utils import register
    
    
    class TestPOC(POCBase):
        ...
    ```

2. 填写POC信息字段,**<font color=red>所有信息都要认真填写不然不会过审核的</font>**

    ```python
    vulID = '1571'  # vul ID
    version = '1' #默认为1
    author = 'zhengdt' # POC作者的大名
    vulDate = '2014-10-16' #漏洞公开的时间,不清楚可以与编写POC日期相同
    createDate = '2014-10-16'# 编写POC的日期
    updateDate = '2014-10-16'#POC更新的时间,默认和编写时间一样
    references = ['https://www.sektioneins.de/en/blog/14-10-15-drupal-sql-injection-vulnerability.html']# 漏洞地址来源,0day不用写
    name = 'Drupal 7.x /includes/database/database.inc SQL注入漏洞 POC'# POC 名称
    appPowerLink = 'https://www.drupal.org/'# 漏洞厂商主页地址
    appName = 'Drupal'# 漏洞应用名称
    appVersion = '7.x'# 漏洞影响版本
    vulType = 'SQL Injection'#漏洞类型,类型参考见 漏洞类型规范表
    desc = '''
        Drupal 在处理 IN 语句时，展开数组时 key 带入 SQL 语句导致 SQL 注入，
        可以添加管理员、造成信息泄露。
    ''' # 漏洞简要描述
    samples = []# 测试样列,就是用POC测试成功的网站
    ```

3. 编写检测模式： 检测模式即为单纯的验证目标网站是否有漏洞，不对目标进行任何修改，删除等有危害的行为。在 PoCsuite 中用户需要定义 verify 函数作为检测模式，定义方式如下：

    ```python
    def _verify(self):
        output = Output(self)
        result = {} #result是返回结果
        # 验证代码
    ```

	验证成功后需要把验证结果赋值给 result 变量。result 里的 key 必须按照下面规范填写

    ```python
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

    Example:

    ```python
  if keywords:
      result['VerifyInfo'] = {}
      result['VerifyInfo']['URL'] = self.url + payload
    ```

	result 每个 key 值相对应的意义：

    ```python
    correspond：[

    {  name: 'DBInfo',        value：'数据库内容' },
    {  name: 'Username',      value: '管理员用户名'},
    {  name: 'Password',      value：'管理员密码' },
    {  name: 'Salt',          value: '加密盐值'},
    {  name: 'Uid',           value: '用户ID'},
    {  name: 'Groupid',       value: '用户组ID'},

    {  name: 'ShellInfo',     value: 'Webshell信息'},
    {  name: 'URL',           value: 'Webshell地址'},
    {  name: 'Content',       value: 'Webshell内容'},

    {  name: 'FileInfo',      value: '文件信息'},
    {  name: 'Filename',      value: '文件名称'},
    {  name: 'Content',       value: '文件内容'},

    {  name: 'XSSInfo',       value: '跨站脚本信息'},
    {  name: 'URL',           value: '验证URL'},
    {  name: 'Payload',       value: '验证Payload'},

    {  name: 'AdminInfo',     value: '管理员信息'},
    {  name: 'Uid',           value: '管理员ID'},
    {  name: 'Username',      value: '管理员用户名'},
    {  name: 'Password',      value: '管理员密码'},

    {  name: 'Database',      value：'数据库信息' },
    {  name: 'Hostname',      value: '数据库主机名'},
    {  name: 'Username',      value：'数据库用户名' },
    {  name: 'Password',      value: '数据库密码'},
    {  name: 'DBname',        value: '数据库名'},

    {  name: 'VerifyInfo',    value: '验证信息'},
    {  name: 'URL',           value: '验证URL'},
    {  name: 'Postdata',      value: '验证POST数据'},
    {  name: 'Path',          value: '网站绝对路径'},

    {  name: 'SiteAttr',      value: '网站服务器信息'},
    {  name: 'Process',       value: '服务器进程'}

    ]
    ```

4. 编写攻击模式： 攻击模式可以对目标进行 getshell ，查询管理员帐号密码等操作.定义它的方法与检测模式类似

    ```python
    def _attack(self):
        output = Output(self)
        result = {}
        # 攻击代码
    ```

    和验证模式一样，攻击成功后需要把攻击得到结果赋值给 result 变量。

    **注意：如果该 PoC 没有攻击模式，可以在 _attack() 函数下加入一句 return self._verify() 这样你就无需再写 _attack() 函数了。**

5. 注册POC实现类

    在类的外部调用register()方法注册poc类

    ```python
    Class TestPOC(POCBase):
        #POC内部代码
    
    #注册TestPOC类
    register(TestPOC)
    ```

#### JsonPOC编写 

1. 首先新建一个.json文件,文件名应当符合 **poc命名规范** 

2. poc json有两个key，pocInfo和pocExecute，分别代表poc信息部分执行体。

    ```json
{
    "pocInfo":{},
    "pocExecute":{}
}
    ```

3. 填写pocInfo部分：

    ```json
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
    
    ```json
{
    "pocInfo":{},
    "pocExecute":{
        "verify":[],
        "attack":[]
    }
}
    ```

    **填写verify部分:**

    ```json
{
    "pocInfo":{},
    "pocExecute":{
        "verify":[
            {
                "step": "1",
                "method": "get",
                "vulPath": "/api.php",
                "params": "test=123&sebug=1234",
                "necessary": "",
                "headers": {"cookie": "123"},
                "res": {
                    "raw": ["baidu","google"],
                    "time": "time"
                }
            },
            {
                "step": "2",
                "method": "get",
                "vulPath": "/api.php",
                "params": "test=sebug",
                "necessary": "",
                "headers": "",
                "res":{
                    "raw": [],
                    "time": "0.01"
                }
            }
        ],
        "attack":[]
    }
}
    ```
 
    > 说明：
    
    > step: 按照上下顺序执行，值可以取0和非0两种。如果step的值为0,那么验证成功后就会返回成功，如果step的值不为0,那么需要全部满足后才返回成功。
    
    > method：请求方式
    
    >  vulPath：请求路径
    
    > params：请求参数
    
    > necessary：请求中必须存在的数据，例如cookie
    
    > headers：自定义请求头部
    
    > res：返回体，其中：
    
    > > raw：表示字符串匹配，为数组类型，当且仅当raw中所有的元素都匹配成功的情况下，返回True，否则返回False.
    
    > > time：为时间差
    
    > > 当raw和time同时存在时，取raw，time失效。
    
    **verify中每个元素代表一个请求。**
        
    **填写attack部分:**
attack部分和verify部分类似，不再缀述。



### PoC 命名规范
 PoC 命名分成 3 个部分组成漏洞应用名_版本号_漏洞类型名称 然后把文件名中的所有字母改写为小写，所有的符号改成_。文件名不能有特殊字符和大写字母。 规范的文件名示例
 
 ```
	_1847_seeyon_3_1_login_info_disclosure.py
 ```

### 漏洞类型规范

参考[漏洞分类](http://sebug.net/category)


### PoC 编写注意事项

1. 检测模式为了防止误报的产生,我们一般使用的让页面输出一个自定义的字符串。

    比如:

    检测 SQL 注入时, ```select md5(0x2333333)```
    
    ```
    if '5e2e9b556d77c86ab48075a94740b6f7' in content:
	    result['VerifyInfo'] = {}
        result['VerifyInfo']['URL'] = self.url+payload
    ```
 
    检测 XSS 漏洞时```alert('<0x2333333>')```
    
    ```
    if '<0x2333333>' in content:
	    result['VerifyInfo'] = {}
        result['VerifyInfo']['URL'] = self.url+payload
    ```
 
    检测 PHP 文件上传是否成功。```<?php echo md5(0x2333333);unlink(__FILE__);?>```
     
    ```
    if '5e2e9b556d77c86ab48075a94740b6f7' in content:
        result['VerifyInfo'] = {}
        result['VerifyInfo']['URL'] = self.url+payload
    ```    
 
2. 任意文件如果需要知道网站路径才能读取文件的话,可以读取系统文件进行验证,要写 Windows 版和 Linux 版两个版本。

3. 检测模式下,上传的文件一定要删掉

4. 程序可以通过某些方法获取表前缀，just do it；若不行，保持默认表前缀

5. PoC 编写好后，务必进行测试，测试规则为：5个不受漏洞的网站，确保 PoC 攻击不成功；5个受漏洞影响的网站，确保 PoC 攻击成功。

## 演示视频

如果浏览器不支持播放，请直接访问[这里](http://sebug.net/static/images/pocsuite_demo.mp4)