```
                              ,--. ,--.
 ,---. ,---. ,---.,---.,--.,--`--,-'  '-.,---.
| .-. | .-. | .--(  .-'|  ||  ,--'-.  .-| .-. :
| '-' ' '-' \ `--.-'  `'  ''  |  | |  | \   --.
|  |-' `---' `---`----' `----'`--' `--'  `----'
`--'                            http://sebug.net

```
Pocsuite
---
---
Pocsuite 是知道创宇安全研究团队打造的一款基于漏洞与 PoC 的漏洞验证框架。Pocsuite 是知道创宇安全研究团队发展的基石，是团队发展至今一直维护的一个项目，保障了我们的 Web 安全研究能力的领先。

在获取到相关漏洞详情后，任何有一定 Python 开发基础的人都可以基于 Pocsuite 开发出对应漏洞的 PoC 或者 Exp ，轻而易举的就可以直接使用 Pocsuite 进行相关的验证和调用，而无需考虑底层代码架构等。

在 Sebug 重新改版上线之际，知道创宇安全研究团队正式对外开放 Pocsuite 框架，任何安全研究人员都可以基于 Pocsuite 进行 PoC 后者 Exp 的开发，同时也可以加入 Sebug 漏洞社区，为 Pocsuite 提供贡献或者贡献相关的 PoC。


安装
---
---

你可以通过用 Git 来克隆代码仓库中的最新源代码

```bash
    git clone git@github.com:knownsec/pocsuite.git
```
或者你可以点击 [这里](https://github.com/knownsec/pocsuite/archive/master.zip) 下载最新的源代码 zip 包,并解压

```bash
    $ wget https://github.com/knownsec/pocsuite/archive/master.zip
    $ unzip master.zip
```

无需其它安装进入 pocsuite 目录,输入即可使用

```
    python pocsuite.py --version
```

使用
---
---

Pocsuite 支持命令行模式(cli)和交互式控制台模式(console)

#### 命令行模式

命令行模式可以对目标发起 Verify 和 Attack 模式的测试,

进入 pocsuite 目录,执行 pocsuite.py

获取命令帮助列表
```
    python pocsuite.py -h
```


假定你已经有一个 PoC(poc_example.py),并且将基保存在 test 目录下面:

PoC 目前支持.py 文件和 .json 文件两种，两者用法一样,具体参考下方说明

Verify 模式，验证目标是否存在漏洞:

```
    python pocsuite.py -r test/poc_example.py -u http://www.example.com/ --verify
```
Attack 模式:
```
    python pocsuite.py -r test/poc_example.py -u http://www.example.com/ --attack

```
如果你有一个 URL 文件(url.txt),要批量验证,你可以:

```
    python pocsuite.py -r test/poc_example.py -f url.txt --verify
```
> Attack 模式的批量处理，只需要替换 ```--verify``` 参数为 ```--attack``` 即可.


加载 test 目录下的所有 PoC 对目标测试:

```
    python pocsuite.py -r test/ -u http://www.example.com --verify
```

使用多线程,默认线程数为 1:
```
    python pocsuite.py -r test/ -f url.txt --verify --threads 10
```

#### 控制台交互式视图

进入控制台交互式视图:
```
    python pcs-console.py
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

PoC 报告自动生成
---
---
Pocsuite 默认只会将执行结果输出显示在屏幕上，如需将结果自动生成报告并保存，在扫描参数后加 ```--report [report_file]``` 即可生成 HTML 格式报告。

```
    python pocsuite.py -r tests/poc_example2.py -u example.com --verify --report /tmp/report.html
```
上述命令执行后，会调用 poc_example2.py 并将结果保存到 /tmp/report.html中。


PoC 编写规范及注意事项
---
---
PoC 支持 Python 和 JSON 两种格式，详情参见[PoC 编写规范](./docs/POCAPI.md)

Pocsuite 中文帮助
---
---

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

其他设置:
  --threads THREADS     最大线程数(默认为1)
  --report REPORT       生成 HTML 格式报告(如："./report.html")

```

感谢
---
---
* 感谢来自不同同学的建议和帮助
* 也欢迎更多同学参与 Pocsuite 的贡献
* [感谢列表](./docs/THANKS.md)

相关链接
---
---
* Sebug http://sebug.net
* 知道创宇 http://www.knownsec.com
