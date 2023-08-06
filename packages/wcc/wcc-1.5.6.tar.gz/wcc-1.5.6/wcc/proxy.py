"""
获取代理
"""
import os
import time
import json
import random
import requests
from ml3 import tools
import pymongo
from  pymongo import MongoClient
import traceback
import threading
import numpy as np

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
    if proxy_source == True:
        proxy_source = "all"
    url = 'http://api.hannm.com/fc10009/'+str(proxy_source)
    response = requests.get(url).json()
    try:
        iport = response['result']['iport']
        ip,port = iport.split(":")
    except Exception as err:
        ip = None
        port = None
    return ip,port

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
        time0 = int(time.time()*1000)
        resp = requests.get(url, proxies=proxies, timeout=10)
        time1 = int(time.time()*1000)
        return time1 - time0
    except:
        return -1

def verify_proxy_thread_main(thread_tid,thread_jobs,mongo_proxy_col):
    #print("thread "+str(thread_tid)+" start")
    for k in range(len(thread_jobs)):
        tjob = thread_jobs[k]
        iport = tjob["iport"]
        src = tjob["src"]
        delay = verify_proxy(iport)
        thread_jobs[k]["delay"] = delay
        proxy_delay = delay
        if proxy_delay < 0:
            mongo_proxy_col.update_one({"iport":iport},{"$set":{"active":0,"delay":-1,"vtime":int(time.time())}})
        else:
            mongo_proxy_col.update_one({"iport":iport},{"$set":{"active":1,"delay":delay,"vtime":int(time.time())}})
        #print(src+"/"+iport+" "+str(delay))
    #print("thread "+str(thread_tid)+" finish")
 
    


#本函数将访问wccdb下的proxy表,然后循环运行,来验证proxy里的各个proxy的有效性,延迟等..
def verify_proxydb(https=True):
    #为了尽快赶上数据库add_proxy自己清理的速度,我们要快速对库里的代理进行验证.
    MAX_THREAD_N = 2
    PROXY_PER_THREAD = 10
    try:
        time0 = int(time.time())
        env_dict = os.environ
        mongo_dat_uri       = env_dict["MONGO_DAT_URI"]
        mongo_dat_client    = pymongo.MongoClient(mongo_dat_uri)
        mongo_dat_db        = mongo_dat_client["wccdb"]
        mongo_dat_col       = mongo_dat_db["proxy"]
        mongo_dat_col_proxy_eva       = mongo_dat_db["proxy_eva"]
        mongo_proxy_col     = mongo_dat_db["proxy"]
        cur_ctime = 0
        dblist = mongo_dat_client.wccdb.proxy.find({"active":1}).limit(MAX_THREAD_N*PROXY_PER_THREAD).sort([("ctime",pymongo.DESCENDING)])
        proxy_list = []
        for dbitem in dblist:
            proxy_list.append({"iport":dbitem["iport"],"src":dbitem["src"]})
        
        local_time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        if len(proxy_list) == 0:
            print(local_time_str + " no proxy found")
            return True
        job_list = []
        for k in range(MAX_THREAD_N):
            job_list.append({"tid":k%MAX_THREAD_N+1000,"jobs":[]})

        cur_K= 0
        for proxy in proxy_list:
            job_list[cur_K%MAX_THREAD_N]["jobs"].append(proxy)
            cur_K +=1

        threads = []
        for job in job_list:
            if len(job["jobs"]) == 0:
                continue
            thread = threading.Thread(target=verify_proxy_thread_main,args=(job["tid"],job["jobs"],mongo_proxy_col))    
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()           #主线程等待 ta线程结束才继续执行
       
        proxy_born_count = mongo_dat_client.wccdb.proxy.count_documents({"active":1})
        dblist = mongo_dat_client.wccdb.proxy.find({"active":1,"delay":{"$gt":0}}).limit(10000).sort([("ctime",pymongo.DESCENDING)])
        proxy_list = []
        proxy_delay_list = []
        for dbitem in dblist:
            proxy_delay = 0
            if "delay" in dbitem:
                proxy_delay = dbitem["delay"]
            proxy_list.append({"iport":dbitem["iport"],"src":dbitem["src"],"delay":proxy_delay})
            proxy_delay_list.append(proxy_delay)
        if len(proxy_list) == 0:
            return
        
        np_proxy_delay_list = np.array(proxy_delay_list)
        proxy_cnt = len(proxy_delay_list)
        proxy_std = np.std(proxy_delay_list,ddof=1)
        proxy_avg = np.mean(proxy_delay_list)
        proxy_max = np.max(proxy_delay_list)
        proxy_min = np.min(proxy_delay_list)
        #代理良率
        good_proxy_count = 0
        for a in proxy_delay_list: 
            if a > 0: good_proxy_count +=1
        proxy_yield = float(good_proxy_count)/float(len(proxy_delay_list))
        time1 = int(time.time())
        local_time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        proxy_eva_doc = {
            "incr":int(time.time()*1000*1000),
            "cthr":local_time_str,
            "cost":time1 - time0, #这个记录的验证时间代价
            "yield":proxy_yield,
            "born":int(proxy_born_count),
            "cnt":int(proxy_cnt),
            "std":int(proxy_std),
            "avg":int(proxy_avg),
            "max":int(proxy_max),
            "min":int(proxy_min)
        }
        print(proxy_eva_doc)
        mongo_dat_col_proxy_eva.insert_one(proxy_eva_doc)
    except Exception as err:
        print(traceback.format_exc())

def main():
    iport = get_proxy("all")
    print(iport)
    verify_proxydb()


if __name__ == "__main__":
    main()

