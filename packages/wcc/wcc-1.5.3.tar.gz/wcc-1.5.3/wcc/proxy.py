"""
获取代理
"""
import os
import time
import json
import random
import requests
from ml3 import tools

def get_proxy(proxy_source):
    """
    从IP池中获取一个ip，IP池：  http://api.hannm.com/fc10009
    从虎头代理获取一个代理ip和端口
    :return:一个元组(ip, port), 其中ip是个字符串，port是个整型数字
    """
    if proxy_source is None:
        proxy_source = "all"
    if proxy_source == "":
        proxy_source = "all"

    url = 'http://api.hannm.com/fc10009/'+str(proxy_source)
    while True:
        response = requests.get(url).json()
        try:
            iport = response['result']['iport']
        except Exception as err:
            continue
        if verify_proxy(iport):
            ip, port = iport.split(":")
            return ip, port
        else:
            continue

def verify_proxy(iport, https=True):
    """
    验证代理是否可用
    """
    if https:
        proxies = {"https":iport}
        url = 'https://www.baidu.com/'
    else:
        url = 'http://www.sohu.com/'
        proxies = {"http":iport}
    try:
        resp = requests.get(url, proxies=proxies, timeout=15)
        return True
    except:
        return False

def main():
    ip, port = get_proxy("xdaili")
    print ("ip:" + ip + ", port:" + str(port))

if __name__ == "__main__":
    main()

