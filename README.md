# esp8266\_wake\_on\_line
基于ESP8266的远程唤醒设备,使用OneNET物联网平台,micropython+mqtt协议


----------

# 帮助文档

[http://docs.micropython.org/en/latest/index.html](http://docs.micropython.org/en/latest/index.html "http://docs.micropython.org/en/latest/index.html")

# 使用方法


1. 在OneNET物联网平台添加产品和设备
2. 刷入bin目录下的固件(也可以从[官网](http://micropython.org/download#esp8266 "官网")下载)
3. 将产品ID,设备ID,鉴权信息,要唤醒设备的MAC地址写入main.py中
4. 将所有文件上传至设备
5. 连接到'ESP8666_'开头的wifi,打开[http://192.168.4.1](http://192.168.4.1 "http://192.168.4.1"),输入要连接的wifi和密码


