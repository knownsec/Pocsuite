
集成 Pocsuite
----------

pocsuite/api/cannon.py 定义了 Cannon 类, 可以通过传递一个包含「待检测目标」,「 PoC 字符串」, 「检测模式」等内容的字典来获得 Cannon 类实例取名为 cannon, 之后通过 cannon.run 可以启动 Pocsuite 来进行检测, 此时会进行单线程检测, 并支持在上层对Cannon进行多线程/多进程调用. 

另外将切换到静默模式不输出任何内容, 结束时返回一个记录此次运行结果的字典, 具体代码如下:

``` python
from pocsuite.api.cannon import Cannon

info = {"pocname": "PoC的名字",
        "pocstring": "PoC的字符串",
        "mode": "verify( or attack)"
        }

target = "test.site"
invoker = Cannon(target, info) # 生成用来引用 Pocsuite 的实例
result = invoker.run()			# 调用 Pocsuite, result 保存了 Pocsuite 执行的返回结果
```

返回结果如下:

```
(
	'test.site', # 测试站点
	'PoC Name', # poc名字
	'SeebugID', # seebug id
	'applications', # poc针对应用
	'version', 	# 目标应用版本
	'failedMessage/success/(errorID, error)', # poc执行后返回的成功失败信息,成功则显示 success,失败则显示 PoC 里通过 output.fail(msg) 保存的 msg 字符串,异常则显示程序捕获到的异常和该异常的编号
	'Date', 	# 时间
	{result}	# poc返回的result字典, 格式参照docs/CODING.md#poc-结果返回规范
)
```