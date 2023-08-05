    #LOG,INFO,WARN,ERROR,
    def addWcclog(spider,wfrm,logtype,trace, **kw):
        endpoint = 'cn-beijing.log.aliyuncs.com'       # 选择与上面步骤创建Project所属区域匹配的Endpoint
        accessKeyId = "LTAIAXYxFrvPLR2j"    # 使用你的阿里云访问密钥AccessKeyId
        accessKey = "doG7ELiF2qeMA3xncVIK0UpCHGxTIE"      # 使用你的阿里云访问密钥AccessKeySecret
        project = 'wcc'        # 上面步骤创建的项目名称
        logstore = 'wcclog'       # 上面步骤创建的日志库名称
        # 构建一个client
        client = LogClient(endpoint, accessKeyId, accessKey)
        # list 所有的logstore
        #req1 = ListLogstoresRequest(project)
        #res1 = client.list_logstores(req1)
        #res1.log_print()
        topic = "mytopic"
        source = "mysource"
        compress = True
        #普通的trace必须通过如下方法获取.
        #trace = sys._getframe().f_code.co_filename+"-"+sys._getframe().f_code.co_name+"-"+str(sys._getframe().f_lineno)
        contents = [('spider', spider),('type', logtype),("wfrm",wfrm),("trace",trace)]
        if "url" in kw:
            contents.append(("url",kw["url"]))
        if "status" in kw:
            contents.append(("status",kw["status"]))

        logitemList = []  # LogItem list
        logItem = LogItem()
        logItem.set_time(int(time.time()))
        logItem.set_contents(contents)
        logitemList = [logItem]
        request = PutLogsRequest(project, logstore, topic, source, logitemList, compress=compress)
        response = client.put_logs(request)
        response.log_print()
        return True
