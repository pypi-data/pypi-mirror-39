import oss2
from .urllibx import *
import os

"""
判断oss_bucket里有没有存在某个文件
"""
def existsFile(oss_bucket,file_localname):
    #如果用bucket.get_object(key),目测会真实下载object,会带来很大出网流量
    #目前暂时使用False
    #return False
    access_key_id       = os.environ['OSS_WCC_ACCESS_KEY_ID']
    access_key_secret   = os.environ['OSS_WCC_ACCESS_KEY_SECRET']
 
    bucket_name         = oss_bucket
    endpoint            = 'http://oss-cn-beijing.aliyuncs.com'
    #endpoint = os.getenv('OSS_WCC_ENDPOINT','http://oss-cn-beijing-internal.aliyuncs.com')
    # 确认上面的参数都填写正确了
    for param in (access_key_id, access_key_secret, bucket_name, endpoint):
        assert '<' not in param, '请设置参数：' + param
    
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    
    # 获取不存在的文件会抛出oss2.exceptions.NoSuchKey异常
    #"""如果文件存在就返回True，否则返回False。如果Bucket不存在，或是发生其他错误，则抛出异常。"""
    #https://github.com/aliyun/aliyun-oss-python-sdk/blob/master/oss2/api.py
    flag = False
    try:
        flag = bucket.object_exists(file_localname)
    except oss2.exceptions.NoSuchKey as e:
        print(e)
        return False
    except Exception as err:
        print(err)
        return False
    return flag

def uploadFile(file_localname, file_oss_name,oss_bucket='file-wikicivi-com'):
    access_key_id       = os.environ['OSS_WCC_ACCESS_KEY_ID']
    access_key_secret   = os.environ['OSS_WCC_ACCESS_KEY_SECRET']
 
    bucket_name = oss_bucket
    endpoint = 'http://oss-cn-beijing.aliyuncs.com'
    #确认上面的参数都填写正确了
    for param in (access_key_id, access_key_secret, bucket_name, endpoint):
        assert '<' not in param, '请设置参数：' + param
    # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    # 把本地文件 “座右铭.txt” 上传到OSS，新的Object叫做 “我的座右铭.txt”
    # 注意到，这次put_object()的第二个参数是file object；而上次上传是一个字符串。
    # put_object()能够识别不同的参数类型
    success = True
    for k in range(1,6):
        try:
            bucket.put_object_from_file(file_oss_name, file_localname)
            success = True
            break
        except Exception as err:
            #print(err)
            success = False
            time.sleep(1.0)
            print("uploadFile:"+file_oss_name+" Fail "+str(k)+"/6 due to "+str(err))
            continue
    if success == True:
        print("↑:%-45s→%-45s" % (file_localname,file_oss_name)) 
    else:
        print("uploadFile:"+file_oss_name+" Abort")
    # # 上面两行代码，也可以用下面的一行代码来实现
    # bucket.put_object_from_file(file_localname, file_localname)
    return success

##本函数仅仅是把一个网页源码保存在files.wikicivi.com/html下. 
##传进来的html_text一定要是utf-8格式，各个爬虫作者在调用这个函数的时候务必确认这点，保证转码后的html_text没有乱码.
##如果成功，返回文件名，如果失败，返回
def uploadHtml(html_text, oss_bucket='file-wikicivi-com'):
    file_oss_name = "html/"+md5(html_text.encode(encoding='utf_8')).hexdigest()+".html"
    access_key_id       = os.environ['OSS_WCC_ACCESS_KEY_ID']
    access_key_secret   = os.environ['OSS_WCC_ACCESS_KEY_SECRET']
    bucket_name = oss_bucket
    endpoint = 'http://oss-cn-beijing.aliyuncs.com'
    #确认上面的参数都填写正确了
    for param in (access_key_id, access_key_secret, bucket_name, endpoint):
        assert '<' not in param, '请设置参数：' + param
    # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    # 把本地文件 “座右铭.txt” 上传到OSS，新的Object叫做 “我的座右铭.txt”
    # 注意到，这次put_object()的第二个参数是file object；而上次上传是一个字符串。
    # put_object()能够识别不同的参数类型
    hasFlag = False
    try:
        hasFlag = bucket.object_exists(file_oss_name)
    except oss2.exceptions.NoSuchKey as e:
        print(e)
        hasFlag= False
    except Exception as err:
        print(err)
        hasFlag=False
    if hasFlag:
        print("!:text@%-45s" % (file_oss_name)) 
        file_oss_name = "http://file.wikicivi.com/"+file_oss_name
        return file_oss_name


    success = True
    for k in range(1,6):
        try:
            bucket.put_object(file_oss_name, html_text)
            success = True
            break
        except Exception as err:
            #print(err)
            success = False
            time.sleep(1.0)
            print("uploadFile:"+file_oss_name+" Fail "+str(k)+"/3 due to "+str(err))
            continue
    file_oss_name = "http://file.wikicivi.com/"+file_oss_name
    if success == True:
        print("↑:text→%-45s" % (file_oss_name)) 
        return file_oss_name
    else:
        print("uploadFile:"+file_oss_name+" Abort")
        return None

#把网络上的一个文件转移到oss上,目标文件命名使用MD5
#如果已经存在或者成功返回oss上的url
#如果失败返回""
@staticmethod
def uploadFurl(file_url,bucket,file_oss_path,download_params=None):
        if bucket == "file-xdua-com":
            oss_url_pfx = "http://file.xdua.com/"
        elif bucket == "file-wikicivi-com":
            oss_url_pfx = "http://file.wikicivi.com/"
        else:
            print("Error:错误的bucket名字")
        fileurlmd5 = md5(file_url.encode(encoding='utf_8')).hexdigest()
        mime_type,file_ext,file_size = getFurlInfo(file_url)
        file_local_path=file_oss_path+"/"+fileurlmd5+"."+file_ext
        down_flag = downloadFile(file_local_path,file_url,download_params)
        if down_flag == False:
            print("Error:不能回避的错误,下载文件失败 "+file_url)
            return None
        
        filedatmd5 = md5_file(file_local_path)
        if filedatmd5 == None:
            print("getmd5File:"+file_local_path+" Fail")
            return None
        file_oss_path = file_oss_path+"/"+filedatmd5+"."+file_ext
        file_oss_url = oss_url_pfx+file_oss_path

        has_flag = existsFile(bucket,file_oss_path)
        if has_flag == True:
            #print("bucket "+bucket+" has "+file_oss_path)
            return file_oss_url

        upload_flag = uploadFile(file_local_path,file_oss_path,bucket)
        if upload_flag == False:
            print("Error:不能回避的错误,文件上传失败 "+file_oss_path)
            return None
        print(""+file_oss_url+" ossuploadurlmd5 ok")
        return file_oss_url

#把网络上的一个文件转移到oss上,目标文件命名使用MD5
#如果已经存在或者成功返回oss上的url
#如果失败返回""
@staticmethod
def uploadFurlMd5(file_url,bucket,file_oss_dir,myheaders=None):
        if bucket == "file-xdua-com":
            oss_url_pfx = "http://file.xdua.com/"
        elif bucket == "file-wikicivi-com":
            oss_url_pfx = "http://file.wikicivi.com/"
        else:
            print("Error:错误的bucket名字")
        fileurlmd5 = md5(file_url.encode(encoding='utf_8')).hexdigest()
        mime_type,file_ext,file_size = getFurlInfo(file_url)
        file_local_path=file_oss_dir+"/"+fileurlmd5+"."+file_ext
        down_flag = downloadFile(file_local_path,file_url,myheaders)
        if down_flag == False:
            print("Error:不能回避的错误,下载文件失败 "+file_url)
            return None
        
        filedatmd5 = md5_file(file_local_path)
        if filedatmd5 == None:
            print("getmd5File:"+file_local_path+" Fail")
            return None
        file_oss_path = file_oss_dir+"/"+filedatmd5+"."+file_ext
        file_oss_url = oss_url_pfx+file_oss_path

        has_flag = existsFile(bucket,file_oss_path)
        if has_flag == True:
            #print("bucket "+bucket+" has "+file_oss_path)
            return file_oss_url

        upload_flag = uploadFile(file_local_path,file_oss_path,bucket)
        if upload_flag == False:
            print("Error:不能回避的错误,文件上传失败 "+file_oss_path)
            return None
        print(""+file_oss_url+" ossuploadurlmd5 ok")
        return file_oss_url
    

