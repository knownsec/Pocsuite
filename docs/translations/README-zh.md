
# Pocsuite

[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/knownsec/Pocsuite/master/docs/COPYING) [![Twitter](https://img.shields.io/badge/twitter-@seebug-blue.svg)](https://twitter.com/sebug)

## 简介

Pocsuite 是由[知道创宇安全研究团队](http://www.knownsec.com/)打造的一款远程漏洞验证框架。它是知道创宇安全研究团队发展的基石，是团队发展至今一直维护的一个项目。该框架拥有强大的漏洞引擎，可供渗透测试/安全研究人员使用, 进行漏洞的验证与利用。


## 准备条件

- Python 2.6+
- Works on Linux, Windows, Mac OSX, BSD

## 安装

安装只需一条命令:

```
$ pip install pocsuite
```

或者点击[链接](https://github.com/knownsec/Pocsuite/archive/master.zip) 下载最新版的zip源码包，并解压安装:

```
$ wget https://github.com/knownsec/Pocsuite/archive/master.zip
$ unzip master.zip
```


最新版的软件也可以在这里找到: http://pocsuite.org

## 文档

Pocsuite相关的**帮助/开发文档**, 请查阅目录 [```docs```](../../docs) .

## 功能


**漏洞测试框架**

Pocsuite 采用 Python 编写，支持验证与利用两种插件模式，你可以指定单个目标或者从文件导入多个目标，使用单个 PoC 或者 PoC 集合进行漏洞的验证或利用。可以使用命令行模式进行调用，也支持类似 Metaspolit 的交互模式进行处理，除此之外，还包含了一些基本的如输出结果报告等功能。（[使用方法参考《Pocsuite 使用方法》](./USAGE-zh.md)）

**PoC/Exp 开发包**

Pocsuite 也是一个 PoC/Exp 的 SDK，也就是开发包，我们封装了基础的 PoC 类,以及一些常用的方法，比如 Webshell 的相关方法，基于 Pocsuite 进行 PoC/Exp 的开发，你可以只要编写最核心的漏洞验证部分代码，而不用去关心整体的结果输出等其他一些处理。基于 Pocsuite 编写的 PoC/Exp 可以直接被 Pocsuite 使用，现在有几百人基于 Pocsuite 编写 PoC/Exp。

**可被集成模块**

Pocsuite 除了本身具有直接就是一个安全工具除外，也可以成为一个可被集成的漏洞测试模块。你还可以基于Pocsuite开发你自己的应用，我们在 Pocsuite 里封装了可以被其他程序 import 的 PoC 调用类，你可以基于 Pocsuite 进行二次开发，调用 Pocsuite 开发您自己的漏洞验证工具。

**集成 ZoomEye 与 Seebug API**

Pocsuite 还集成了 Seebug 与 ZoomEye API，通过该功能，你可以通过 ZoomEye API 批量获取指定条件的测试目标（通过 ZoomEye 的 Dork 进行搜索），同时通过 Seebug API 读取指定组件或者类型的漏洞的 PoC 或者本地 PoC，进行自动化的批量测试。


## 如何贡献

1. 如果有好的点子或问题，可以在 [issues](https://github.com/knownsec/Pocsuite/issues) 板块提出来。
2. 创建 [Pocsuite](https://github.com/knownsec/Pocsuite) 分支，开始维护自己的代码.
3. 需要解决的问题，请附上详细的错误信息，以便开发/测试人员复现。已经解决的问题，请提交测试结果信息，确保所有功能按照预期正确运行。
4. 请确认提交的请求已经被处理，并获得感谢。(添加相关人员到[感谢名单列表](https://github.com/knownsec/Pocsuite/blob/dev/docs/THANKS.md).


## 友情链接

* [感谢名单列表](../../docs/THANKS.md)
* [历史修订](../../docs/CHANGELOG.md)
* [问题跟踪](https://github.com/knownsec/Pocsuite/issues)
* [版权](./docs/COPYING)
* [Pocsuite](http://pocsuite.org)
* [Seebug](https://www.seebug.org)
* [ZoomEye](https://www.zoomeye.org)
