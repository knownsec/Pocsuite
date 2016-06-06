使用方法
--------

Pocsuite 支持命令行模式(cli)和交互式控制台模式(console), 如果使用 pip 安装, 直接使用`pocsuite`代替`python pocsuite.py`


### 获取命令帮助列表

``` bash
    $ python pocsuite.py -h
```

```
使用方法: python pocsuite.py [选项]

基础帮助:
  -h, --help            显示帮助信息
  --version             显示当前程序版本号

目标设置:
  -u URL, --url URL     目标 URL (如："http://www.targetsite.com/")
  -f URLFILE, --file URLFILE
                        加载一个文档中的所有 URL，一行一个
  -r POCFILE            加载一个 PoC 或者一个目录下的所有 PoC(如： "_0001_cms_sql_inj.py" 或者 "modules/")

模式设置:
  --verify              Verify 模式
  --attack              Attack 模式

请求设置:
  --cookie COOKIE       自定义 HTTP 请求头中 Cookie 信息
  --referer REFERER     自定义 HTTP 请求头中 Referer 信息
  --user-agent AGENT    自定义 HTTP 请求头中 User-Agent 信息
  --random-agent        使用随机 User-Agent
  --proxy PROXY         使用代理来连接目标
  --proxy-cred PROXYCRED
                        设置代理用户名和密码 (如 name:password)
  --timeout TIMEOUT     设置超时时间(默认30秒)
  --retry RETRY			设置超时重试的次数
  --delay DELAY			设置超时重试之间的时间间隔
  --headers HEADERS		设置额外的 HTTP 请求头
  --host HOST			设置 HTTP 请求时的 HOST 字段

参数设置:
  --extra-params		用来自定义额外的参数, 传入类似字典的字符串"{'username': '***', 'password': '***'}", 调用 Pocsuite 来取它时会自动转化成字典格式.

其他设置:
  --threads THREADS     最大线程数(默认为1)
  --report REPORT       生成 HTML 格式报告(如："./report.html")
  --batch BATCH			所有参数都选择使用默认情况
  --requires			检查 install_requires 是否都符合
  --quite				安静模式, 不输出 Pocsuite 的日志
  --require-freeze		在 Poc 注册后进行 install_requires 检查

Zoomeye 和 Seebug:
  --dork DORK           ZoomEye Dork，用于在 ZoomEye 搜索目标
  --max-page MAX_PAGE   ZoomEye API 的请求翻页数(10 目标/页)
  --search-type SEARCH_TYPE
                        ZoomEye API 搜索类型，web 或者 host
  --vul-keyword VULKEYWORD
                        Seebug 搜索关键词，用于在 Seebug 搜索漏洞
```

### 命令行模式

命令行模式可以对目标发起 Verify 和 Attack 模式的测试,

进入 pocsuite 目录,执行 pocsuite.py


假定你已经有一个 PoC(poc_example.py),并且将其保存在 tests 目录(**任意目录, 以下如无说明默认为 ./tests**)下面:

PoC 目前支持.py 文件和 .json 文件两种，两者用法一样,具体参考下方说明

Verify 模式，验证目标是否存在漏洞:

``` bash
    $ python pocsuite.py -r tests/poc_example.py -u http://www.example.com/ --verify
```

Attack 模式:

``` bash
    $ python pocsuite.py -r tests/poc_example.py -u http://www.example.com/ --attack
```

如果你有一个 URL 文件(url.txt),要批量验证,你可以:

``` bash
    $ python pocsuite.py -r tests/poc_example.py -f url.txt --verify
```

> Attack 模式的批量处理，只需要替换 ```--verify``` 参数为 ```--attack``` 即可.



加载 任意目录(如: tests)下的所有 PoC 对目标测试:

``` bash
    $ python pocsuite.py -r tests/ -u http://www.example.com --verify
```

使用多线程,默认线程数为 1:

``` bash
    $ python pocsuite.py -r tests/ -f url.txt --verify --threads 10
```

### 控制台交互式视图模式

进入控制台交互式视图:

``` bash
    $ python pcs-console.py
```

通用命令：

```
    ls, help        展示出当前可用的命令
    q, exit         退出/返回父视图
```

在 **Pcs 视图**(Pcs>)下,常用的命令:

```
    config          进入目标配置子视图
    poc             进入 PoC 配置子视图
    verify          开始验证
    attack          开始
    shell [command] 执行系统shell命令
    hi, history     历史命令
    show            显示当前系统设置
    set             修改系统设置
    shortcuts       查看短命令
```

在 **Config 视图**(Pcs.Config>)下,常用的命令:

```
[Command]
   thread       : 设置最大线程数(默认为1)
   url          : 设置目标 URL
   urlFile      : 载入文件中的 URL
```

在 **Poc 视图**(Pcs.poc>)下,常用的命令:

```
    avaliable   查看所有可用的 PoC
    search      从可用的 PoC 列表中检索
    load <Id>   加载指定 Id 的 PoC
    loaded      查看已经加载的 PoC
    unload      查看未加载的 PoC
    clear       移出所有已加载的 PoC
```

**注意：控制台视图下只能加载 pocsuite/modules/ 目录下的 PoC**

#### 使用 pcs-console 测试步骤:

1. 进入 Config 子视图,设置目标

   ```
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

2. 进入 PoC 子视图，加载指定 PoC

   ```
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

3. Verify/Attack

   ```
   Pcs>verify
   [15:13:26] [*] starting 1 threads
   [15:13:26] [*] poc:'_poc_example1' target:'www.example.com'
   ```

### 使用 ZoomEye 和 Seebug API

如：

```
    pocsuite --dork 'port:6379' --vul-keyword 'redis' --max-page 2
```

搜索 Redis 服务器目标，指定两页，即20个目标，进行自动化的批量测试

```
--dork DORK                 ZoomEye Dork，用于在 ZoomEye 搜索目标
--max-page MAX_PAGE         ZoomEye API 的请求翻页数(10 目标/页)
--search-type SEARCH_TYPE   ZoomEye API 搜索类型，web 或者 host
--vul-keyword VULKEYWORD    Seebug 搜索关键词，用于在 Seebug 搜索漏洞
```

### Pocsuite 报告自动生成

Pocsuite 默认只会将执行结果输出显示在屏幕上，如需将结果自动生成报告并保存，在扫描参数后加 `--report [report_file]` 即可生成 HTML 格式报告。

``` bash
    $ python pocsuite.py -r tests/poc_example2.py -u example.com --verify --report /tmp/report.html
```
