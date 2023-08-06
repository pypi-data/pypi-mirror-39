# 天智信达的库

## 用法
1. 此库作为git项目管理，凡是修改完后应及时通知到开发团队
2. 需要使用库中的方法，使用pip install,这时候就可以在项目中引用库中的方法
3. 引用的方法举例：

----------------------------------------------------------

#### generation - 更新库

Make sure you installed setuptools and wheel.

Important: You must modify the version of the package in setup.py and delete folders (build, dist, egg-info)
- python setup.py sdist bdist_wheel

#### upload - 上传代码

Install twine before doing this
- twine upload dist/*

------------------------------------------------------------

#### install - 安装
- pip install wisdoms

#### find the latest package of wisdoms - 发现最新版本
- pip list --outdated

#### upgrade - 升级到最新包
- pip install wisdoms --upgrade


## packets usage:

#### auth.py:

``` python

    from wisdoms.auth import permit

    host ={'AMQP_URI': "amqp://guest:guest@localhost"}

    auth = permit(host)

    class A:
        @auth
        def func():
            pass
```

#### config.py

``` python

    from wisdoms.config import c

    # gains item of YML config
    print(c.get('name'))

    # transforms class into dict
    d = c.to_dict()
    print(d['name'])

```

#### commons package

``` python

    from wisdoms.commons import revert, codes, success

    def func():
        # do something

        # revert(codes.code) or revert(number)
        # return revert(1)
        return revert(codes.ERROR)

    def foo():
        # return revert(code, data, desc)
        return revert(codes.SUCCESS, {'data':'data'},'返回成功描述信息')

    def done():
        # simplified revert where success execute
        # return success(data) or success()
        return success()
```

#### util.py
``` python

    # 多个字符串连接成路径
    from wisdoms.utils import joint4path

    print(joint4path('abc','dac','ccc'))

    # $: abc/dac/ccc

    # 对象转字典
    from wisdoms.utils import o2d

    o2d(obj)

    # 捕获异常装饰器
    from wisdoms.utils import exception

    @exception()
    def func():
        pass

```

#### ms.py
``` python

    from wisdoms.ms import ms_base

    MsBase = ms_base(config)

    class A(MsBase):
        pass
```


## 如何设计包
- 顶级包：wisdom，代表天智，智慧
- 现阶段的约定：采用一级包的方式
- 不同的功能放在不同的文件（模块）即可做好方法的分类