## 简介
本部分代码用于构建sdk

## 打包上传
首先在`https://pypi.org/`上创建账号，接下来在本地本目录下创建~/.pypirc，这样以后就不用输入用户名和密码了
```shell
[distutils]
index-servers=pypi

[pypi]
repository = https://pypi.python.org/pypi
username = <username>
password = <password>
```
执行如下命令打包和上传
```shell
python setup sdist
dwine upload dist/*
```

## 使用方法
可以在本地执行`pip install baidu-acu-asr`安装sdk，创建新的python文件，示例代码如下(也可见client_demo.py)
```python
# -*-coding:utf-8-*-
from baidu_acu_asr.AsrClient import AsrClient
import threading
# ip和端口可根据需要修改，sdk接口文档见http://agroup.baidu.com/abc_voice/md/article/1425870
client = AsrClient("172.18.53.17", "31051", enable_flush_data=False)


def run():
    response = client.get_result("/Users/xiashuai01/Downloads/300s.wav")
    for res in response:
        print("start_time\tend_time\tresult")
        print(res.start_time + "\t" + res.end_time + "\t" + res.result)


if __name__ == '__main__':
    run()
    # 多线程运行
    # for i in range(100):
    #     print(i)
    #     t = threading.Thread(target=run, args=[])
    #     t.start()
```