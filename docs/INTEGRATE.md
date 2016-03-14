集成 Pocsuite
----------

pocsuite/api/cannon.py 定义了 Cannon 类, 可以通过传递一个包含「待检测目标」,「 PoC 字符串」, 「检测模式」等内容的字典来获得 Cannon 类实例取名为 cannon, 之后通过 cannon.run 可以启动 Pocsuite 来进行检测, 此时 Pocsuite 将切换到静默模式不输出任何内容, 结束时返回一个记录此次运行结果的字典, 具体代码如下:

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
