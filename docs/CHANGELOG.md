
version 2.0
---------------
* Integrate Seebug and ZoomEye APIs（doing）
* Add English document（doing）
* update webshell class



version 2.0.3.1
--------------
* add method:resolve_js_redirects
* class pocsuite.api.cannon.Cannon returns details of  error and failure of a PoC
* fix ImportError in class Cannon
* fix wrong md5 func used in PhpShell
* change PoC success & fail return format from string to tuple  in Cannon API
* catch more exceptions when processing HTTP request in POCBase
* fix error 'importing from source results in parent module not found while handling absolute import' when '.' in fullname in Cannon API

version 2.0.4
-----------
* fix bug in lib/core/common.py: not import locale and used it
* fix bug in lib/core/common.py: there is not Variable or constant name NULL,bug it is used
* fix bug in lib/core/consoles.py:baseConsole:do_ls:endless loop when command ls something
* add file .travis.yml and integrate travis-ci
* PEP8
