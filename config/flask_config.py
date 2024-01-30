# import os
# import socket
# from flask import Flask
# from flask import request
# from config import logging_config
from flask import request



class Config:
    '''
    os.environ是用来读取系统的环境变量的 环境变量通过键值对的形式存储 通过get的形式获取
    '''
    # APP_ID = os.environ.get("PM_APP_ID")  # 接口用
    # APP_SECRET = os.environ.get("PM_APP_SECRET")  # 接口用
    # SECRET_KEY = "3bfab48fc27316dd59f4b963e9087ea57b0a27c9d19b7dd7"  # Flask用
    # TASK_FILE_FOLDER = "./logs/history"
    # ACCESS_TOKEN_URL = os.environ.get("PM_ACCESS_TOKEN_URL")
    # SAVE_INFO_URL = os.environ.get("PM_SAVE_INFO_URL")
    # MAX_CONVERSION_TIME = os.environ.get("PM_MAX_CONVERSION_TIME")
    # PORT = os.environ.get("FLASK_RUN_PORT")
    # ipv4s = socket.gethostbyname_ex(socket.gethostname())[2]
    # iii=socket.gethostbyname(socket.gethostname())
    # print(iii)
    # print(ipv4s)
    HOST = "0.0.0.0"
    JSON_AS_ASCII = False
    PORT=28081
    # LOGGER = logging_config.logging_self_define().log(level='WARNING', name="app.py")
    BACK_END_URL="127.0.0.1"
    BACK_END_PORT=28081
    HOST_IP="127.0.0.1"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 设置请求大小限制为16MB




if Config.PORT is None:
    Config.PORT=28081



'''
logger：日志器，提供程序可使用的接口

handler：处理器，用于写入日志文件并输出到指定位置，如文件、控制台或网络等

filter：过滤器，用于输出符合指定条件的日志记录

formatter：格式器，决定日志记录的输出格式
'''

class ProductionConfig(Config):
    # LOGGING_LEVEL = logging.DEBUG  #设定日志等级
    DEBUG=False
    pass

class TestingConfig(Config):
    DEBUG=False
    pass
'''
http://115.200.3.77:8081
当前执行的ip地址是属于宽带厂商的固定端口号 可以通过公网访问 这就是为什么10.4 凌晨接收到了其他主机对我的访问

当前IP地址有三个 最多可以有四个
['172.18.144.1', '172.22.32.86', '192.168.43.6']
前两个是以太网的分别是   以太网适配器 vEthernet (WSL):     以太网适配器 以太网 2:
第一个是我的linux的 第二个是我的宽带 第三个是无线网或者ppp适配器
ppp适配器可以将域名映射到公网 无线局域网也可以满足在在局域网范围内得到请求

当前设置的 host是0.0.0.0表示flask监听本机所有的IP地址 flask就会使用这所有的ip地址 

str = request.remote_addr
print("localhost_ip:",str)  -->获得服务器ip地址
user_str=request.environ['REMOTE_ADDR']
print("user_ip:",user_str)   -->获得客户端ip地址
'''