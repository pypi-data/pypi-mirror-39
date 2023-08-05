"""

"""
import req



def main():
    # url = 'http://www.baidu.com'
    url = 'http://stockpage.10jqka.com.cn/000063/funds'
    url2 = 'https://zhuanlan.zhihu.com/p/47777088'
    url3 = 'http://www.ip138.com/'
    url4 = 'https://ip.cn/'
    url5 = 'https://www.qichacha.com/firm_8c9f7ddc1a7bcee3d1f7676773fe9404.html'  # 企查查
    #cookie_str = wcc.get_cookie("http://stockpage.10jqka.com.cn/000063/")
    #print (cookie_str)
    #resp_text = wcc.getpage(url, use_proxy=False, use_browser=False,use_cookie=cookie_str)
    #print (resp_text)

    # url6 = 'https://www.qichacha.com/search?key=' + '昆明恒海科技有限公司'
    # res = req.getpage(url6, use_proxy=True)
    # print(res)
    headers = {
            'Host':'www.qichacha.com',
            'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0', 
            'Accept':'*/*', 
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', 
            'Accept-Encoding':'gzip, deflate', 
            'If-Modified-Since':'Wed, 30 Aug 2017 10:48:38 GMT',
            }
    res = req.getpage(url5, use_proxy=True, browser='chrome')
    print(res)




if __name__ == "__main__":
    main()
