# Usage

- **pocsuite**: a cool and hackable command line program
- **pcs-console**: an interactive interface.

## pocsuite

Enter into `pocsuite` directory, execute `python pocsuite.py`. It supports double mode:

 - ```verify```
 - ```attack```

You can also use ```python pocsuite.py -h``` for more details.

```
$ python pocsuite.py -h

Usage: python pocsuite.py [options]

optional arguments:
  -h, --help            Show help message and exit
  --version             Show program's version number and exit

target:
  -u URL, --url URL     Target URL (e.g. "http://www.targetsite.com/")
  -f URLFILE, --file URLFILE
                        Scan multiple targets given in a textual file
  -r POCFILE            Load POC from a file (e.g. "_0001_cms_sql_inj.py") or directory (e.g. "modules/")

mode:
  --verify              Run poc with verify mode
  --attack              Run poc with attack mode

request:
  --cookie COOKIE       HTTP Cookie header value
  --referer REFERER     HTTP Referer header value
  --user-agent AGENT    HTTP User-Agent header value
  --random-agent        Use randomly selected HTTP User-Agent header value
  --proxy PROXY         Use a proxy to connect to the target URL
  --proxy-cred PROXYCRED
                        Proxy authentication credentials (name:password)
  --timeout TIMEOUT     Seconds to wait before timeout connection (default 30)
  --retry RETRY         Time out retrials times.
  --delay DELAY         Delay between two request of one thread
  --headers HEADERS     Extra headers (e.g. "key1: value1\nkey2: value2")
  --host HOST           Host in HTTP headers.

params:
  --extra-params        Extra params (e.g. "{username: '***', password: '***'}")

optimization:
  --threads THREADS     Max number of concurrent HTTP(s) requests (default 1)
  --report REPORT       Save a html report to file (e.g. "./report.html")
  --batch BATCH         Automatically choose defaut choice without asking
  --requires            Check install_requires
  --quiet               Activate quiet mode, working without logger
  --requires-freeze     Check install_requires after register

Zoomeye or Seebug:
  --dork DORK           Zoomeye dork used for search.
  --max-page MAX_PAGE   Max page used in ZoomEye API(10 targets/Page).
  --search-type SEARCH_TYPE
                        search type used in ZoomEye API, web or host
  --vul-keyword VULKEYWORD
                        Seebug keyword used for search.
```

**-f, --file URLFILE**

Scan multiple targets given in a textual file

```
$ python pocsuite.py -r tests/poc_example.py -f url.txt --verify
```

> Attack batch processing mode only need to replace the ```--verify``` as ``` --attack```.

**-r POCFILE**

POCFILE can be a file or a directory. If a file, it can be placed in it in the `tests` directory (or anywhere you prefer). If a directory, Pocsuite will load multiple PoCs from special destination.


```
$ python pocsuite.py -r tests/ -u http://www.example.com --verify
```

**--verify**

Run poc with verify mode. PoC(s) will be only used for a vulnerability scanning.

```
$ python pocsuite.py -r tests/poc_example.py -u http://www.example.com/ --verify
```

**--attack**

Run poc with attack mode, PoC(s) will be exploitable, and it may allow hackers/researchers break into labs.

```
$ python pocsuite.py -r tests/poc_example.py -u http://www.example.com/ --attack
```

**--threads THREADS**

Using multiple threads, the default number of threads is 1

```
$ python pocsuite.py -r tests/ -f url.txt --verify --threads 10
```

**--report REPORT**

Pocsuite default only the execution result is output to the screen, `--report [report_file]` parameter can generate reports in HTML format.

```
$ python pocsuite.py -r tests/poc_example2.py -u example.com --verify --report /tmp/report.html
```


**--dork DORK**

If you are a [**ZoomEye**](https://www.zoomeye.org/) user, The API is a cool and hackable interface. ex:

Search redis server with ```port:6379``` and ```redie``` keyword.


```
$ python pocsuite.py --dork 'port:6379' --vul-keyword 'redis' --max-page 2

                              ,--. ,--.
 ,---. ,---. ,---.,---.,--.,--`--,-'  '-.,---.  {2.0.2-58f6fe6}
| .-. | .-. | .--(  .-'|  ||  ,--'-.  .-| .-. :
| '-' ' '-' \ `--.-'  `'  ''  |  | |  | \   --.
|  |-' `---' `---`----' `----'`--' `--'  `----'
`--'                                            https://seebug.org

[!] legal disclaimer: Usage of pocsuite for attacking targets without prior mutual consent is illegal.

[*] starting at 19:26:19

[19:26:19] [+] ZoomEye API authorization failed,Please input ZoomEye Email and Password for use ZoomEye API!
ZoomEye Email:
ZoomEye Password:
[19:26:35] [-] ZoomEye API authorization failed, make sure correct credentials provided in "~/.pocsuiterc".
```


----

## pcs-console

The **pcs-console** is a interactive interface. It provides an “all-in-one” centralized console and allows you efficient access to virtually all of the options available.

**Benefits**

- Provides a console-based interface to the framework
- Contains the most features
- Full readline support, tabbing, and command completion


```
$ python pcs-console.py
```

```
Pcs> help
    config          register global configs
    poc             enter pocConsole, basic poc operation
    verify          conducting verification
    attack          conduncting attack
    shell [command] shell command execution system
    hi, history     command history
    show            displays the current system settings
    set             modify system settings
    shortcuts       view short command
```

**Note**: PoC(s) should be in ```pocsuite/modules/``` directory.

If you want to test against **www.example.com**, please try it step by step.

  - set a target (url, urlFile)
  - load avaliable PoC(s)


```
$ python pcs-console.py

                              ,--. ,--.
 ,---. ,---. ,---.,---.,--.,--`--,-'  '-.,---.  {2.0.2-58f6fe6}
| .-. | .-. | .--(  .-'|  ||  ,--'-.  .-| .-. :
| '-' ' '-' \ `--.-'  `'  ''  |  | |  | \   --.
|  |-' `---' `---`----' `----'`--' `--'  `----'
`--'                                            https://seebug.org

Pcs> help

[Command]
   config       : register global configs.
   poc          : enter pocConsole, basic poc operation.

[Mode]
   verify       : conducting verification.
   attack       : conduncting attack.

Pcs> config
Pcs.config> help

[Command]
   thread       : set multiple threads. (Default 1)
   url          : set target url from stdin.
   urlFile      : set target url from urlFile.
   q            : return upper level.

[Option]
   header       : set http headers for follow requests.
   proxy        : set proxy. format: '(http|https|socks4|socks5)://address:port'.
   timeout      : set max requests time. (Default 5s)
   show         : show config.

Pcs.Config> url
Pcs.config.url> www.example.com
Pcs.Config> show
+---------+-----------------+
|  config |      value      |
+---------+-----------------+
|   url   | www.example.com |
| threads |        1        |
+---------+-----------------+
Pcs.config> q
```


**avaliable** command will show all PoC(s), one PoC one id. If you want a special PoC, please enter ```load pocId``` in the console.

```
Pcs> poc
Pcs.poc> avaliable
+-------+-------------------------+
| pocId | avaliablePocName        |
+-------+-------------------------+
|   1   | struts2_dmi_rce.py      |
|   2   | ImageMagic_delegate.py  |
+-------+-------------------------+

Pcs.poc> load 1
[*] load poc file(s) success!
Pcs.config> q
Pcs>verify
[15:13:26] [*] starting 1 threads
[15:13:26] [*] poc:'struts2_dmi_rce' target:'www.example.com'
```

If you have good ideas, please show them on your way.
