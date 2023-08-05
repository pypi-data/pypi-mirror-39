#Wikicivi Crawler Client SDK
import os,time
import threading
import datetime
import urllib
import oss2
import shelve
import socket
import requests
import traceback
from hashlib import md5
from datetime import date
import os,sys
import struct
import random
import json
#pip install Pillow
from PIL import Image
from io import BytesIO
#tinytag对有些mp3读不出duration,我备用eyed3试下,eyed3不行的话,用mutagen
from tinytag import TinyTag
#pip3 install eyeD3(注意大小写)
import eyed3
from mutagen.mp3 import MP3  
import mutagen.id3  
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3  
import re
import types
import traceback
import getopt
from tinytag import TinyTag
from .utils import *
from selenium import webdriver
import imageio


import traceback
import sys
import time
from aliyun.log.logitem import LogItem
from aliyun.log.logclient import LogClient
from aliyun.log.getlogsrequest import GetLogsRequest
from aliyun.log.putlogsrequest import PutLogsRequest
from aliyun.log.listlogstoresrequest import ListLogstoresRequest
from aliyun.log.gethistogramsrequest import GetHistogramsRequest



#https://boonedocks.net/blog/2008/03/10/Determining-Image-File-Types-in-Ruby.html
#def file_type(file)
#   case IO.read(file, 10)
#        when /^GIF8/: ‘gif’
#        when /^\x89PNG/: 'png’
#        when /^\xff\xd8\xff\xe0\x00\x10JFIF/: 'jpg’
#        when /^\xff\xd8\xff\xe1(.*){2}Exif/: 'jpg’
#        else 'unknown’
#        end
#    end
#
#最多尝试10次,判断这个远程文件的信息
#坑：程序总是运行到中途就会卡死，经定位发现是 res = requests.get(url,timeout=1)这句代码出了问题
#https://www.zhihu.com/question/35321993
#我估计是GC没有正确释放资源, 卡住了.
#像爬虫这种IO密集型的程序，本身就不适合利用多进程编程，所以题主用的应该是python的threading库而不是multiprocessing。题主可以将程序改为threading+Queue试试。
#若要更简单点，题主可以利用gevent等并发框架试试。
#因为使用requests.get()会卡主，这也说明了requests这种第三方库不是很厉害
#所以使用python的官方urllib,它是python自己维护的,应该不会卡主
#
#第二个问题:如果urlopen目标file_url中有中文的时候,urlopen就会出现如下错误
#http://t44.tingchina.com/yousheng/历史军事/国士无双/001_关外来的土匪.mp3?key=32bd82ce105b4741e0d7c4b08870d2c3_546431312
#'ascii' codec can't encode characters in position 14-17: ordinal not in range(128)
#下面这个帖子说，要对url中的中文进行parse,而且仅对中文
#http://www.cnblogs.com/LuckyBao/p/6223443.html
#下面这个帖子说，可以混合用
#https://www.zhihu.com/question/22899135
#第一方案
#socket.setdefaulttimeout(30)    
#urlreq = urllib.request.Request(file_url, headers=Wcc.wcc_headers)
#if k % 2 == 1 and k > 0:
#    #使用自定义的UA和代理IP
#    proxy = {'http':'61.48.134.245:53109'}
#    proxy_support = urllib.request.ProxyHandler(proxy)
#    opener = urllib.request.build_opener(proxy_support)
#    urllib.request.install_opener(opener)
#with urllib.request.urlopen(urlreq) as resp:
#    resp.read()
#    file_size = resp.headers['content-length']
#    mime_type = resp.headers['content-type']
#第二方案
#response = requests.get(file_url,stream=True,timeout=30,headers=HEAD)
#file_size = int(response.headers['content-length'])
#mime_type = response.headers['content-type']
#第三方案
#有些图片因为不存在,它们所在的server会返回一些文字

"""
获取网络上一个url文件的信息.在这个过程中要把url转移到oss上.
返回retinfo结构.
"""

"""
通过file_url获取file_url这个文件的 mime_type,file_ext,file_size
mime_type是"image/jpeg"这种
file_ext 是"jpg"/"png"/"mp4"这种
file_size是文件大小
"""

@staticmethod
def getFurlInfo(file_url,bucket,myheaders=None):
    try:
        if bucket == "xdua-files":
            oss_url_pfx = "http://xdua-files.oss-cn-beijing.aliyuncs.com/"
        elif bucket == "wikicivi-files":
            oss_url_pfx = "http://wikicivi-files.oss-cn-beijing.aliyuncs.com/"
        else:
            print("Error:错误的bucket名字")
        retinfo = {"url":file_url}
        fileurlmd5 = md5(file_url.encode(encoding='utf_8')).hexdigest()
        retinfo["urlmd5"] = fileurlmd5
        """
        如果数据库有fileurlmd5对应的这条记录,那么就返回这条数据.
        """
        info = None
        ##try:
        ##    #This method is a shortcut that calls Model.select() with the given query, but limits the result set to a single row. Additionally, if no model matches the given query, a DoesNotExist exception will be raised.
        ##    info = Furlinfo.get(Furlinfo.urlmd5 == fileurlmd5)
        ##except Exception as err:
        
        if info != None:
            retinfo["datmd5"] = info.datmd5
            retinfo["ossurl"] = info.ossurl
            retinfo["mime"] = info.mime
            retinfo["s"] = info.s
            retinfo["w"] = info.w
            retinfo["h"] = info.h
            retinfo["lot"] = info.lot
            retinfo["fps"] = info.lot
            retinfo["vdef"] = info.vdef
            retinfo["givurl"] = info.givurl
            retinfo["givsiz"] = info.givsiz
            retinfo["webpurl"] = info.webpurl
            return retinfo
        
        mime_type,file_ext,file_size = Wcc.getFileInfo(file_url)
        if mime_type == "null" or file_size ==0 or file_ext == "" :
            print("ErrbakUrl:"+file_url)
            return None
        mime_main = mime_type.split("/")[0]
        mime_sub = mime_type.split("/")[1]
        if mime_main == "image":
            bucket_dir = "Images"
        elif mime_main == "video":
            bucket_dir = "Videos"
        elif mime_main == "audio":
            bucket_dir = "Audios"
        elif mime_type == "application/pdf":
            bucket_dir = "Pdfs"
       
        fileurlmd5_localpath = bucket_dir+"/"+fileurlmd5+'.' +file_ext
        retinfo["s"] = file_size
        retinfo["ext"] = file_ext
        retinfo["mime"] = mime_type
        file_local_path=bucket_dir+"/"+fileurlmd5+"."+file_ext
        down_flag = Wcc.downloadFile(file_local_path,file_url,myheaders)
        if down_flag == False:
            print("Error: 下载文件失败 "+file_url)
            return None
        filedatmd5 = md5_file(file_local_path)
        if filedatmd5 == None:
            print("Error: 获取文件MD5失败 "+file_local_path)
            return None
        filedatmd5_localpath = bucket_dir+"/"+filedatmd5+"."+file_ext
        retinfo["datmd5"] = filedatmd5
        """
        如果数据库有filedatmd5对应的这条记录,那么就返回这条数据.
        """
        try:
            #This method is a shortcut that calls Model.select() with the given query, but limits the result set to a single row. Additionally, if no model matches the given query, a DoesNotExist exception will be raised.
            info = Furlinfo.get(Furlinfo.datmd5 == filedatmd5)
        except Exception as err:
            info = None
        
        if info != None:
            retinfo["datmd5"] = info.datmd5
            retinfo["ossurl"] = info.ossurl
            retinfo["mime"] = info.mime
            retinfo["s"] = info.s
            retinfo["w"] = info.w
            retinfo["h"] = info.h
            retinfo["lot"] = info.lot
            retinfo["fps"] = info.lot
            retinfo["vdef"] = info.vdef
            retinfo["givurl"] = info.givurl
            retinfo["webpurl"] = info.webpurl
            return retinfo
        
        file_oss_path = bucket_dir+"/"+filedatmd5+"."+file_ext
        file_oss_url = oss_url_pfx+file_oss_path
        
        if Wcc.existsFile(bucket,file_oss_path) == False:
            upload_flag = Wcc.uploadFile(file_local_path,file_oss_path,bucket)
            if upload_flag == False:
                print("Error:不能回避的错误,文件上传失败 "+file_oss_path)
                return None
        retinfo["ossurl"] = file_oss_url
        
        if mime_main == "image":
            success,image_width, image_height  = Wcc.get_image_info(file_url,fileurlmd5_localpath)
            if success == False:
                print("Error: 获取图片信息失败 "+file_url)
                return None
            retinfo["w"] = image_width
            retinfo["h"] = image_height
            if image_width == 0 or image_height == 0:
                print("Error: 获取图片信息错误 "+file_url)
                return None
        
        if mime_main == "video":
            okflag,width,height,lot,fps  = Wcc.get_video_info(file_url,fileurlmd5_localpath)
            if okflag == False:
                print("Error: 获取视频信息失败 "+file_url)
                return None
            if width == 0 or height == 0 or lot == 0:
                print("Error: 获取视频信息错误 "+file_url)
                return None
            retinfo["w"] = width
            retinfo["h"] = height
            retinfo["lot"] = lot
            retinfo["fps"] = fps
        if mime_main == "video":
            vdef = "other"
            vh = retinfo["h"]
            if vh >= 240:
                vdef = "240p"
            if vh >= 360:
                vdef = "360p"
            if vh >= 480:
                vdef = "480p"
            if vh >= 540:
                vdef = "540p"
            if vh >= 720:
                vdef = "720p"
            if vh >= 1080:
                vdef = "1080p"
            retinfo["vdef"] = vdef
        
        if mime_main == "audio":
            duration  = Wcc.get_avdio_duration(file_url,fileurlmd5_localpath)
            if duration == 0:
                print("Error: 获取音频时长失败 "+file_url)
                return None
            retinfo["lot"] = duration
        
        """
        获取文章的其它信息.如果是gif<我得生成一个mp4,然后上传.
        """
        #如果是动态gif图片,那么我要转换成mp4,添加到fitem的mp4项目中.
        #如果转换失败,也没关系,忽略
        if mime_type == "image/gif":
            if gif2mp4(fileurlmd5_localpath) == False:
                print("Error: 动图转MP4失败")
                return None
            file_gifmp4_localpath = fileurlmd5_localpath[:-4]+".mp4"
            file_gifmp4_osspath   = filedatmd5_localpath[:-4]+".mp4"
            if Wcc.existsFile(bucket,file_gifmp4_osspath) == False:
                if Wcc.uploadFile(file_gifmp4_localpath, file_gifmp4_osspath,bucket) == False:
                    print("Error:MP4动图上传失败 "+file_oss_path)
                    return None
            retinfo["givurl"] = oss_url_pfx+file_gifmp4_osspath
            try:
                tinytag_class = TinyTag.get(file_gifmp4_localpath)
                duration = tinytag_class.duration
                mp4lot = duration
            except Exception as err:
                print("Get mp4 Duration Fail:"+str(err))
                mp4lot = 0
        
            try:
                mp4size = os.path.getsize(file_gifmp4_localpath)
            except Exception as err:
                print("Get mp4 Size Fail:"+str(err))
                mp4size = 0
            retinfo["lot"] = mp4lot
            retinfo["givsiz"]  = mp4size
        
        """
        如果是图片是gif,要转换成webp,必须用google的gif2webp
        """
        if mime_main == "image":
            webp_flag = False
            webp_localpath = bucket_dir+"/"+fileurlmd5+".webp"
            #if os.path.exists(webp_localpath):
            #    os.remove(webp_localpath)
            if mime_sub == "gif":
                try:
                    if(gif2webp(fileurlmd5_localpath)==True):
                        webp_flag = True
                    else:
                        print("gif2webp "+fileurlmd5_localpath +" -> "+webp_localpath+" Fail ")
                except Exception as err:
                    print("gif2webp " + fileurlmd5_localpath +" -> "+webp_localpath+" Error: "+str(err))
            else:
                try:
                    Image.open(fileurlmd5_localpath).save(webp_localpath, "WEBP")
                    webp_flag = True
                    if not os.path.exists(webp_localpath):
                        print("img2webp "+fileurlmd5_localpath+" > "+webp_localpath+" fail due to lost")
                        return None
                except Exception as err:
                    #gif走到这里会发生: OSError: cannot write mode P as WEBP
                    #有些静态图如新浪的http://storage.slide.news.sina.com.cn/slidenews/77_ori/2017_40/74766_800832_676052.gif
                    #它的mime就写的是jpeg,其实是gif,这个时候我就会来着里.
                    print("image2webp "+fileurlmd5_localpath +" -> "+webp_localpath+" Error: "+str(err))

            if webp_flag == True and Wcc.existsFile(bucket,webp_localpath) == False:
                if Wcc.uploadFile(webp_localpath, webp_localpath,bucket) == False:
                    print("Error:WEBP动图上传失败 "+webp_localpath)
                    webp_flag = False
            if webp_flag == True:
                retinfo["webpurl"]  = oss_url_pfx+webp_localpath
            else:
                retinfo["webpurl"]  = ""
        info = Furlinfo()
        info.url = file_url
        info.urlmd5 = retinfo["urlmd5"]
        info.datmd5 = retinfo["datmd5"]
        info.ossurl = retinfo["ossurl"]
        info.mime = retinfo["mime"]
        info.s = retinfo["s"]
        if "w" in retinfo:
            info.w = retinfo["w"]
        else:
            info.w = 0
        if "h" in retinfo:
            info.h = retinfo["h"]
        else:
            info.h = 0
        if "lot" in retinfo:
            info.lot = retinfo["lot"]
        else:
            info.lot = 0
        if "fps" in retinfo:
            info.fps = retinfo["fps"]
        else:
            info.fps = 0
        
        if "vdef" in retinfo:
            info.vdef = retinfo["vdef"]
        else:
            info.vdef = ''
        
        
        if "givurl" in retinfo:
            info.givurl = retinfo["givurl"]
        else:
            info.givurl = ""
        if "givsiz" in retinfo:
            info.givsiz = retinfo["givsiz"]
        else:
            info.givsiz = 0
        
        if "webpurl" in retinfo:
            info.webpurl = retinfo["webpurl"]
        else:
            info.webpurl = ""
        info.ctime = time.time()
        try:
            info.save()
        except Exception as err:
            print(info)
            print(err)
    except Exception as err:
        print(traceback.print_exc())
        print(err)
        
    return retinfo


@staticmethod
def doGetFileInfo(file_url_original):
    #file_url = urllib.parse.quote(file_url_original,safe='/:?=&')
    file_url = file_url_original
    for k in range(1,6):
        file_size = 0
        mime_type = "null"
        file_text = ""
        resp = None
        try:
            resp = requests.get(file_url,timeout=300,headers=Wcc.wcc_headers)
            #http://img5.cache.netease.com/m/2015/6/3/20150603180813ca37a.jpg
            #上面这个图片就没有content-length
            #http://rmfygg.court.gov.cn/psca/lgnot/bulletin/download/6309888.pdf
            #上面的地址是就没有content-length
            #{'Content-Type': 'application/pdf', 'Server': 'Apache/2.2.15 (CentOS)', 'Transfer-Encoding': 'chunked', 'Date': 'Thu, 01 Feb 2018 12:27:51 GMT', 'Content-Disposition': 'attachment;filename=¹«¸æ2018-02-01.pdf', 'Connection': 'close'}
            #当content-length不存在的时候,file_size==1
            if 'content-length' not in resp.headers:
                file_size = 1
                print(file_url+" no content-length force to 1")
                #print(resp.headers)
            else:
                file_size = int(resp.headers['content-length'])
            if 'content-type' not in resp.headers:
                mime_type = ""
            else:
                mime_type = resp.headers['content-type']
            break
        except Exception as err:
            #print(traceback.print_exc())
            print(""+file_url+" info err("+str(k)+") "+str(err))
            file_size = 0
            mime_type = "null"
            time.sleep(1)
            if k == 5:
                print(""+file_url+" info Abort")
                if resp == None:
                    print("get resp as None")
                else:
                    print(resp.text)
                    print(traceback.print_exc())
        finally:
            pass
    
    file_url_ext = file_url.split('.')[-1]
    file_url_host= file_url.replace("http://","").split("/")[0]
    #有的图片获取的mime有额外的东西.
    #unkonw mime:image/png;charset=UTF-8 for http://cms-bucket.nosdn.127.net/30b3a22ed1ae458d96de6ccdddec7cd020170330025319.png
    mime_type = mime_type.split(";")[0]
    if "image/png" in mime_type:
        mime_type = "image/png"
    if mime_type == 'image/gif':
        extension = 'gif'
    elif mime_type == 'image/png':
        extension = 'png'
    elif mime_type == 'image/jpeg':
        extension = 'jpg'
    elif mime_type == 'image/webp':
        extension = 'webp'
    elif mime_type == 'audio/x-m4a':
        extension = 'm4a'
    elif mime_type == 'audio/mpeg':
        extension = 'mp3'
    elif mime_type == 'video/mp4':
        extension = 'mp4'
    elif mime_type == 'application/pdf':
        extension = 'pdf'
    elif mime_type == 'text/html; charset=utf-8' and file_url_ext in ["jpg"] and file_url_host in ["www.ting56.com"]:
        #在好多网站观察到图片和m4a都变成了这种content-type
        #http://www.ting56.com/pic/images/2016-11/201611211759927267.jpg
        #未知的mime:text/html; charset=utf-8 for http://www.ting56.com/pic/images/2016-11/201611211759927267.jpg
        mime_type = "image/jpeg"
        extension = "jpg"
    elif mime_type == 'text/html' and file_url_ext in ["m4a"] and file_url_host in ["audio.xmcdn.com"]:
        #未知的mime:text/html for http://audio.xmcdn.com/group15/M02/60/ED/wKgDaFXUZH3iNnE6AJX6ZBlEXF8394.m4a
        mime_type = "audio/x-m4a"
        extension = "m4a"
    elif mime_type == 'null' and file_url_ext in ["m4a"] and file_url_host in ["audio.xmcdn.com"]:
        #未知的mime:null for http://audio.xmcdn.com/group17/M0B/67/AB/wKgJKVf6Pe7wCOrTACU75dNaD5M039.m4a
        mime_type = "audio/x-m4a"
        extension = "m4a"
    else:
        print("unkonw mime:"+mime_type+" for "+file_url)
        mime_type = "null"
        file_size =0
        extension = ''
    if file_url_ext in ["gif"] and mime_type in ["image/jpeg","image/jpg"] and "storage.slide.news.sina.com.cn" in file_url:
        #http://storage.slide.news.sina.com.cn/slidenews/77_ori/2017_40/74766_800832_676052.gif
        #的content-type就是这样.其实是gif
        mime_type_old = mime_type
        mime_type = "image/gif"
        extension = "gif"
        print(file_url+" mime redirect to "+mime_type+" from "+mime_type_old)

    if file_url_ext in ["gif"] and mime_type in ["image/jpeg","image/jpg"] and ".sinaimg." in file_url:
        #http://wx3.sinaimg.cn/mw690/661eb95cgy1fmbm3p96kqg20dm0887wh.gif
        #的content-type就是这样.其实是gif
        mime_type_old = mime_type
        mime_type = "image/gif"
        extension = "gif"
        print(file_url+" mime redirect to "+mime_type+" from "+mime_type_old)

    return mime_type,extension,file_size

#为何要设置User Agent
#有一些网站不喜欢被爬虫程序访问，所以会检测连接对象，如果是爬虫程序，也就是非人点击访问，它就会不让你继续访问，所以为了要让程序可以正常运行，需要隐藏自己的爬虫程序的身份。此时，我们就可以通过设置User Agent的来达到隐藏身份的目的，User Agent的中文名为用户代理，简称UA。
#User Agent存放于Headers中，服务器就是通过查看Headers中的User Agent来判断是谁在访问。在Python中，如果不设置User Agent，程序将使用默认的参数，那么这个User Agent就会有Python的字样，如果服务器检查User Agent，那么没有设置User Agent的Python程序将无法正常访问网站。
#Python允许我们修改这个User Agent来模拟浏览器访问，它的强大毋庸置疑。
#为何使用IP代理
#User Agent已经设置好了，但是还应该考虑一个问题，程序的运行速度是很快的，如果我们利用一个爬虫程序在网站爬取东西，一个固定IP的访问频率就会很高，这不符合人为操作的标准，因为人操作不可能在几ms内，进行如此频繁的访问。所以一些网站会设置一个IP访问频率的阈值，如果一个IP访问频率超过这个阈值，说明这个不是人在访问，而是一个爬虫程序。

#下载网络上的一个文件,比一般的代码多了如下部分
#1:对url中的中文进行重编码
#2:使用UA
#3:使用代理IP
#4:检查content-type合content-size
@staticmethod
def downloadFile(local_path,file_url,params=None):
    if file_url == None:
        print("url must not be None(downloadFile)")
        print(file_url)
        return False
    
    param_headers = None
    if params != None and "headers" in params:
        param_headers = params["headers"]
        
    download_try_count = 5
    try:
        if os.path.exists(local_path):
            return True
        dirname = os.path.dirname(local_path)
        isExists = os.path.exists(dirname)
        if not isExists:
            os.makedirs(dirname)
            print(dirname + '创建成功')
        else:
            pass #print(dirname + '目录已存在')
        t0=time.time()
        file_size = 1
        download_flag = False
        for k in range(1,download_try_count+1):
            try:
                #坑:此处不建议使用第三方库requests.因为会卡死
                #使用urlib.request.urlretrieve也会卡死
                #通过socket类设置全局的超时
                #坑,有些网站的图片下载需要header,如:http://img.2mme.tv/tu/nvlb1scr2tq.jpg
                #Urlretrive的下载方式也需要.
                if download_flag == False:
                    socket.setdefaulttimeout(300)
                    if param_headers == None:
                        urlreq = urllib.request.Request(file_url,headers=生成一个header)
                    else:
                        urlreq = urllib.request.Request(file_url,headers=param_headers)
                    with urllib.request.urlopen(urlreq) as resp:
                        if "content-length" in resp.headers:
                            file_size = int(resp.headers['content-length'])
                        if "content-type" in resp.headers:
                            file_mime = resp.headers['content-type']
                        if file_mime == "text/html" :
                            print("拒绝下载text/html文件,可能爬虫已被网站封")
                            break
                        with open(local_path, 'wb') as local_file:
                            local_file.write(resp.read())
                    download_flag = True
                    if download_flag == False:
                        socket.setdefaulttimeout(300)
                        urllib.request.urlretrieve(file_url,local_path)
                        download_flag = True
                    break
            except Exception as err:
                print("↓:"+file_url +" Fail "+str(k)+"/"+str(download_try_count)+" "+str(err))
                time.sleep(5)
        if download_flag == True:
            t1=time.time()
            speed = file_size/(t1-t0)
            file_size = file_size/1048576
            speed = speed/1024
            print("↓:%s %0.2fM %0.2fKps" % (file_url,file_size,speed)) 
            return True
        else:
            print("dwloadFail: "+file_url)
            return False
    except Exception as err:
        print(traceback.print_exc())
        print(err)
        print("dwloadFail: "+file_url)
        return False
    finally:
        pass


def get_image_info(file_url,local_path):
    ok_flag = False
    try:
        if os.path.exists(local_path):
            #print("retrieFile:"+local_path)
            pass
        else:
            flag = Wcc.downloadFile(local_path, file_url)
            if flag == False:
                return False,0,0    
            else:
                pass
        im = Image.open(local_path);
        width,height = im.size
        ok_flag = True
    except Exception as err:
        print("get_image_info Error:"+local_path+"   "+str(err))
        width = 0
        height = 0
        ok_flag = False
    finally:
        pass
    
    return ok_flag,width, height

#返回:True/False,w,h,lot,fps
def get_video_info(file_url,local_path):
    ok_flag = False
    try:
        if os.path.exists(local_path):
            #print("retrieFile:"+local_path)
            pass
        else:
            flag = Wcc.downloadFile(local_path, file_url)
            if flag == False:
                return False,0,0,0,0    
            else:
                pass
        im = imageio.get_reader(local_path,'ffmpeg')
        im_meta = im.get_meta_data()
        """
        {
            'duration': 17.65, 
            'fps': 20.0, 
            'ffmpeg_version': '2.6.8 built with gcc 4.8.5 (GCC) 20150623 (Red Hat 4.8.5-4)', 
            'source_size': (544, 960), 
            'size': (544, 960), 
            'plugin': 'ffmpeg', 
            'nframes': 353
        }
        """
        print(im_meta)
        width = im_meta["source_size"][0]
        height = im_meta["source_size"][1]
        fps = im_meta["fps"]
        lot = im_meta["duration"]
        ok_flag = True
    except Exception as err:
        width = 0
        height = 0
        fps = 0
        lot = 0
        ok_flag = False
    finally:
        pass
    
    return ok_flag,width, height,lot,fps


#来自github TinyTag
def get_avdio_duration(file_url,local_path):
    try:
        if os.path.exists(local_path):
            print("retrieFile:"+local_path)
        else:
            flag = Wcc.downloadFile(local_path, file_url)
            if flag == False:
                return {}
            else:
                pass
        okFlag = True
        duration = 0
        try:
            tinytag_class = TinyTag.get(local_path)
            duration = tinytag_class.duration
        except Exception as err:
            #print(err)
            print("TinyTag Fail to get info of "+local_path)
            okFlag = False
        if okFlag == False:
            try:
                mp3_eyed3 = eyed3.load(local_path)
                duration = mp3_eyed3.info.time_secs
                okFlag = True
            except Exception as err:
                #print(err)
                print("Eyed3 Fail to get info of "+local_path)
        #if okFlag == False:
        #    try:
        #        mutagen_audio = MP3(local_path)
        #        print(mutagen_audio.items())
        #        for k, v in mutagen_audio.items():
        #            print(str(k)+":"+str(v))
        #        okFlag = True
        #    except Exception as err:
        #        print(err)
        #        print("mutagen Fail to get info of "+local_path)
        #获取音频长度的最后一道方案.github上的一个项目
        #https://github.com/philippbosch/mp3duration
        if okFlag == False:
            try:
                response = requests.get("http://mp3duration.herokuapp.com/?url="+file_url)
                response_json = response.json()
                duration = response_json["seconds"]
                okFlag = True
            except Exception as err:
                #print(err)
                print("herokuapp Fail get duration: "+local_path)
    
        print("audio/video:"+file_url+" lot:"+str(duration))
        if okFlag == True:
            return duration
        else:
            return 0
    
    except Exception as err:
        print(traceback.print_exc())
        print(err)
        return 0
    finally:
        pass
    return 0


#参考https://github.com/devsnd/tinytag
def tinytag_class2dict(tag_class):
    tag_dict = {}
    tag_dict['album']        =tag_class.album#albumasstring
    tag_dict['albumartist']  =tag_class.albumartist#albumartistasstring
    tag_dict['artist']       =tag_class.artist#artistnameasstring
    tag_dict['audio_offset'] =tag_class.audio_offset#numberofbytesbeforeaudiodatabegins
    tag_dict['bitrate']      =tag_class.bitrate#bitrateinkBits/s
    tag_dict['disc']         =tag_class.disc#discnumber
    tag_dict['disc_total']   =tag_class.disc_total#thetotalnumberofdiscs
    tag_dict['duration']     =tag_class.duration#durationofthesonginseconds
    tag_dict['filesize']     =tag_class.filesize#filesizeinbytes
    tag_dict['genre']        =tag_class.genre#genreasstring
    tag_dict['samplerate']   =tag_class.samplerate#samplespersecond
    tag_dict['title']        =tag_class.title#titleofthesong
    tag_dict['track']        =tag_class.track#tracknumberasstring
    tag_dict['track_total']  =tag_class.track_total#totalnumberoftracksasstring
    tag_dict['year']         =tag_class.year#yearordataasstringtag.album#albumasstring
    return tag_dict

