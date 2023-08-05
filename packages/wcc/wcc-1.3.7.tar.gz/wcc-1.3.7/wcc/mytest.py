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
    res = req.getpage(url5, use_proxy=True, browser='chrome')
    print(res)




if __name__ == "__main__":
    main()
