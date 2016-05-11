# Installation

Pocsuite supports command line mode and interactive console mode, if you use pip install directly `pocsuite`.


## Usage

``` bash
$ python pocsuite.py -h
```

```
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

## Command-line

Command-line mode can be initiated on the target Verify/Attack test. Enter `pocsuite` directory, execute `pocsuite.py`.

If you already have a PoC (e.g. poc_example.py), and save it in the `tests` directory (**you can specify any directory**).

PoC script for `.py` and` .json` file formats, both of which use the same.

#### Verify mode

``` bash
$ python pocsuite.py -r tests/poc_example.py -u http://www.example.com/ --verify
```

#### Attack mode

``` bash
$ python pocsuite.py -r tests/poc_example.py -u http://www.example.com/ --attack
```

#### By URL list file (url.txt) bulk verification

``` bash
$ python pocsuite.py -r tests/poc_example.py -f url.txt --verify
```

> Attack batch processing mode only need to replace the ```--verify``` as ``` --attack```.


#### Loading `tests` directory on the target all PoC test

``` bash
$ python pocsuite.py -r tests/ -u http://www.example.com --verify
```

#### Using multiple threads, the default number of threads is 1

``` bash
$ python pocsuite.py -r tests/ -f url.txt --verify --threads 10
```

## Console interaction

#### Interactive view into the console

``` bash
$ python pcs-console.py
```

#### Common Command

```
  ls, help        show currently available commands
  q, exit         quit/returns the parent view
```

#### In view `Pcs` under the commonly used commands

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

#### In view `config` under the commonly used commands

```
Pcs.config> help

[Command]
   thread       : set multiple threads. (Default 1)
   url          : set target url from stdin.
   urlFile      : set target url from urlFile.
```

#### In view `poc` under the commonly used commands:

```
Pcs.poc> help

    avaliable   list avaliable poc file(s)
    search      search from avaliable poc file(s).
    load <Id>   load specific poc file(s).
    loaded      list all loaded poc file(s).
    unload      list all unload poc files(s).
    clear       unload all loaded poc file(s).
```

** Note: The console view can only loading PoC  `pocsuite/modules/` directory. **

## pcs-console Test Procedure:

#### Set the target to enter the Config view

```
    Pcs.Config> url
    Pcs.config.url> www.example.com
    Pcs.Config> show
    +---------+-----------------+
    |  config |      value      |
    +---------+-----------------+
    |   url   | www.example.com |
    | threads |        1        |
    +---------+-----------------+
    
    or
    
    Pcs.Config> url example.com
    Pcs.Config> show
    +---------+-------------+
    |  config |    value    |
    +---------+-------------+
    |   url   | example.com |
    | threads |      1      |
    +---------+-------------+
```

#### Enter PoC view loads the specified PoC

```
    Pcs> poc
    Pcs.poc> avaliable
    +-------+------------------+
    | pocId | avaliablePocName |
    +-------+------------------+
    |   1   | _poc_example1.py |
    |   2   | poc_example1.py  |
    +-------+------------------+

    Pcs.poc> load 1
    [*] load poc file(s) success!

    Pcs.poc> q
```

#### Verify/Attack

```
   Pcs>verify
   [15:13:26] [*] starting 1 threads
   [15:13:26] [*] poc:'_poc_example1' target:'www.example.com'
```

## ZoomEye or Seebug API

```
--dork DORK                 Zoomeye dork used for search
--max-page MAX_PAGE         Max page used in ZoomEye API(10 targets/Page)
--search-type SEARCH_TYPE   search type used in ZoomEye API, web or host
--vul-keyword VULKEYWORD    Seebug keyword used for search
```

Search redis server, maximum two page (ie. 20 targets), automated batch testing

```
$ pocsuite --dork 'port:6379' --vul-keyword 'redis' --max-page 2
```

## Generate reports

Pocsuite default only the execution result is output to the screen, `--report [report_file]` parameter can generate reports in HTML format.

``` bash
$ python pocsuite.py -r tests/poc_example2.py -u example.com --verify --report /tmp/report.html
```
