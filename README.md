
```
                              ,--. ,--.
 ,---. ,---. ,---.,---.,--.,--`--,-'  '-.,---.
| .-. | .-. | .--(  .-'|  ||  ,--'-.  .-| .-. :
| '-' ' '-' \ `--.-'  `'  ''  |  | |  | \   --.
|  |-' `---' `---`----' `----'`--' `--'  `----'
`--'                        http://pocsuite.org
```

[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/knownsec/Pocsuite/master/docs/COPYING) [![Twitter](https://img.shields.io/badge/twitter-@seebug-blue.svg)](https://twitter.com/sebug)

简介
----
Pocsuite 是由知道创宇安全研究团队打造的一款远程漏洞验证框架。它是知道创宇安全研究团队发展的基石，是团队发展至今一直维护的一个项目，保障了我们的 Web 安全研究能力的领先。
你可以直接使用 Pocsuite 进行漏洞的验证与利用；你也可以基于 Pocsuite 进行 PoC/Exp 的开发，因为它也是一个 PoC 开发框架；同时，你还可以在你的漏洞测试工具里直接集成 Pocsuite，它也提供标准的调用类。


功能介绍
---------

#### 漏洞测试框架
Pocsuite 采用 Pyhton 编写，支持验证与利用两种插件模式，你可以指定单个目标或者从文件导入多个目标，使用单个 PoC 或者 PoC 集合进行漏洞的验证或利用。可以使用命令行模式进行调用，也支持类似 Metaspolit 的交互模式进行处理，除此之外，还包含了一些基本的如输出结果报告等功能。（[使用方法参考《Pocsuite 使用方法》](./docs/USAGE.md)）

#### PoC/Exp 开发包
Pocsuite 也是一个 PoC/Exp 的 SDK，也就是开发包，我们封装了基础的 PoC 类,以及一些常用的方法，比如 Webshell 的相关方法，基于Pocsuite 进行 PoC/Exp 的开发，你可以只要编写最核心的漏洞验证部分代码，而不用去关心整体的结果输出等其他一些处理。基于 Pocsuite 编写的 PoC/Exp 可以直接被 Pocsuite 使用，现在有几百人基于 Pocsuite 编写 PoC/Exp。

#### 可被集成模块
Pocsuite 除了本身具有直接就是一个安全工具除外，也可以成为一个可被集成的漏洞测试模块。你还可以基于Pocsuite开发你自己的应用，我们在 Pocsuite 里封装了可以被其他程序 import 的 PoC 调用类，你可以基于 Pocsuite 进行二次开发，调用 Pocsuite 开发您自己的漏洞验证工具。

#### 集成 ZoomEye 与 Seebug API
Pocsuite 还集成了 Seebug 与 ZoomEye API，通过该功能，你可以通过 ZoomEye API 批量获取指定条件的测试目标（通过 ZoomEye 的 Dork 进行搜索），同时通过 Seebug API 读取指定组件或者类型的漏洞的 PoC 或者本地 PoC，进行自动化的批量测试。

安装
-----
Pocsuite 可以运行在 Python 2.6.x 和 2.7.x 版本的任何平台上。

你可以通过用 Git 来克隆代码仓库中的最新源代码

``` bash
$ git clone git@github.com:knownsec/Pocsuite.git
```
或者你可以点击 [这里](https://github.com/knownsec/Pocsuite/archive/master.zip) 下载最新的源代码 zip 包,并解压

``` bash
$ wget https://github.com/knownsec/Pocsuite/archive/master.zip
$ unzip master.zip
```

``` bash
$ cd Pocsuite
$ python pocsuite.py --version
```

或者直接使用

``` bash
$ pip install pocsuite
$ pocsuite --version
```

使用
------
* [如何直接使用 Pocsuite 测试漏洞](./docs/USAGE.md)
* [如何基于 Pocsuite 开发 PoC/Exp](./docs/CODING.md)
* [如何在应用里集成 Pocsuite](./docs/INTEGRATE.md)

相关链接
---------
* [感谢列表](./docs/THANKS.md)
* [Change Log](./docs/CHANGELOG.md)
* [问题/BUG反馈](https://github.com/knownsec/Pocsuite/issues)
* [版权声明](./docs/COPYING)
* [Pocsuite 官网 http://pocsuite.org](http://pocsuite.org)
* [Seebug 官网 https://www.seebug.org](https://www.seebug.org)
* [ZoomEye 官网 https://www.zoomeye.org](https://www.zoomeye.org)

多语言
-------
* [English](./docs/translations/README-en.md)
