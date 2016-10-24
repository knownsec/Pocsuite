
version 2.0
---------------
* Integrate Seebug and ZoomEye APIs（doing）
* Add English document（doing）
* Update webshell class


version 2.0.3
---------------
* Add method:resolve_js_redirects
* Class pocsuite.api.cannon.Cannon returns details of  error and failure of a PoC
* Fix ImportError in class Cannon
* Fix wrong md5 func used in PhpShell
* Change PoC success & fail return format from string to tuple  in Cannon API
* Catch more exceptions when processing HTTP request in POCBase
* Fix error 'importing from source results in parent module not found while handling absolute import' when '.' in fullname in Cannon API


version 2.0.4
---------------
* Fix bug in lib/core/common.py: not import locale and used it
* Fix bug in lib/core/common.py: there is not Variable or constant name NULL,bug it is used
* Fix bug in lib/core/consoles.py:PocsuiteInterpreter:do_ls:endless loop when command ls something
* Add file .travis.yml and integrate travis-ci
* PEP8 and fix some error Variable
* Update cannon API, you can custom mode/Http Headers/Http Timeout and params


version 2.0.4.1
---------------
* Add api method output.error and modify output.fail
* Optimization results show
* Fix bug in lib/core/poc.py: output.error is not tuple type
* Update ZoomEye API address


version 2.0.4.2
---------------
* Add seebug api support
* Add zoomeye api support
* Add random functions
* Add a new console feature
* Update cannon doc
* Fix AttributeErrir bug in pocsuite/api/x.py
* Fix OSError bug in pocsuite/lib/core/consoles.py
* Fix pep8 syntax check
* Fix output bug in pocsuite/lib/core/poc.py
* Fix timeout retry bug in pocsuite/lib/core/option.py


version 3.0
---------------

todo:
* Compact structure and code
* Update thread to coroutine
* update Interactive mode
* Add PoC search function
* Add some PoC to module directory
