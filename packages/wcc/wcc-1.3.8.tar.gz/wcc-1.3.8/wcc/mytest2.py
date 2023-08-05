


import req 



def main():
    # url = 'http://www.baidu.com'
    url = 'http://stockpage.10jqka.com.cn/000063/funds'
    resp_text = req.getpage(url, use_proxy=False, use_browser=True)
    print (resp_text)


if __name__ == "__main__":
    main()
