    # ce=CrawlerError:页面403拉，代码exception了,
    # addWccpmc("pla","dzb.p2peye","AddArt",ce=1)
    def addWccpmc(spider,wtype,wfrm,pmctype, **kw):
        logger = logging.getLogger()
        wccpmc={
            "spider":spider,
            "wtype" :wtype,
            "wfrm"  :wfrm,
            "t"     :pmctype,
            "v"     :0,
            "m"     :0,
            "i"     :0,
            "e"     :0,
            "u"     :0,
            "pcd"   :0,  # publictime ->createtime delay
            "lot"   :0   # run time
        }
        resp=None
        try:
            
            if "v" in kw:
                wccpmc["v"]  = kw["v"]
            if "m" in kw:
                wccpmc["m"]  = kw["m"]
            if "i" in kw:
                wccpmc["i"] = kw["i"]
            if "x" in kw:
                wccpmc["x"] = kw["x"]
            if "e" in kw:
                wccpmc["e"] = kw["e"]
            if "u" in kw:
                wccpmc["u"] = kw["u"]
            if "pcd" in kw:
                wccpmc["pcd"] = kw["pcd"]
            ##参数检查
            #m=ia+xa+ea
            #pmctype="AddArt"
            #ce=0/1
            #pcd>0
            ##参数检查
            resp = requests.post("http://api.wikicivi.com/wccpmc",data=wccpmc)
            resp_json   =  resp.json()
            resp_status =  resp_json["status"]
            resp_reason =  resp_json["reason"]
            resp_result =  resp_json["result"]
        except Exception as err:
            logger.info(traceback.format_exc())
            logger.info(wccpmc)
            logger.info(err)
            reason = str(err)+":"+traceback.format_exc()+":|"+json.dumps(wccpmc)+":-------------"+resp.text
            return reason
        return "success"
