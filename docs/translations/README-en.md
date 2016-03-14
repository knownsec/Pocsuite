
```
                              ,--. ,--.
 ,---. ,---. ,---.,---.,--.,--`--,-'  '-.,---.
| .-. | .-. | .--(  .-'|  ||  ,--'-.  .-| .-. :
| '-' ' '-' \ `--.-'  `'  ''  |  | |  | \   --.
|  |-' `---' `---`----' `----'`--' `--'  `----'
`--'                        http://pocsuite.org
```

[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/knownsec/Pocsuite/master/docs/COPYING) [![Twitter](https://img.shields.io/badge/twitter-@seebug-blue.svg)](https://twitter.com/sebug)

Introduction
----
Pocsuite is an open-sourced remote vulnerability testing framework developed by Knownsec Security Team.It is the cornerstone of the Knownsec Security Team.
You can use Pocsuite to verify and exploit vulnerabilities;You also can write PoC/Exp based on Pocsuite, because it is also a PoC development framework;You can also integrate Pocsuite in your vulnerability testing tool, which also provides a standard calling class.


Functions
---------
* ```Vulnerability Testing Framework```
Pocsuite is written in Python and supported both validation and exploitation two plugin-invoked modes, Pocsuite could import batch targets from files and test those targets-imported against multiple exploit-plugins in advance.（[View the documents《Pocsuite usage》](../USAGE.md)）

* ```PoC/Exp Development Kit```
Like Metasploit, it is a development kit for pentesters to develope their own exploits. Develope PoC/Exp based on Pocsuite , you can just write the most core code of PoC/Exp, and do not care about the results output or others.There are at least several hundred people  write PoC/Exp based on Pocsuite.

* ```Can Be Integrated Module```
Users could utilze some auxiliary modules packaged in pocsuite to extend their exploit functions or integrate pocsuite to develop other vulnerability assesment tools.

* ```Integrated ZoomEye And Seebug API```
Pocsuite is also an extremely useful tool to integrate Seebug and ZoomEye APIs in a collaborative way. Vulnerablity assessment can be done automately and effectively by searching targets through ZoomEye and acquiring PoC scripts from Seebug or locally.


Installation
-----
Pocsuite works out of the box with Python version 2.6.x and 2.7.x on any platform.

You can use Git to clone the latest source code repository

``` bash
$ git clone git@github.com:knownsec/Pocsuite.git
```
Or you can click [here](https://github.com/knownsec/Pocsuite/archive/master.zip) Download the latest source zip package, and extract

``` bash
$ wget https://github.com/knownsec/Pocsuite/archive/master.zip
$ unzip master.zip
```

``` bash
$ cd Pocsuite
$ python pocsuite.py --version
```

Or use pip

``` bash
$ pip install pocsuite
$ pocsuite --version
```

Usage
------
* [How to use the Pocsuite test vulnerability](./docs/USAGE.md)
* [How to develop PoC/Exp based on Pocsuite](./docs/CODING.md)
* [How to integrate Pocsuite in applications](./docs/INTEGRATE.md)

Links
---------
* [Thanks List](./docs/THANKS.md)
* [Change Log](./docs/CHANGELOG.md)
* [BUG Feedback](https://github.com/knownsec/Pocsuite/issues)
* [Copying](./docs/COPYING)
* [Pocsuite Website: http://pocsuite.org](http://pocsuite.org)
* [Seebug Website: https://www.seebug.org](https://www.seebug.org)
* [ZoomEye Website: https://www.zoomeye.org](https://www.zoomeye.org)
