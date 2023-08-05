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

    cookies = req.getcookie('https://www.qichacha.com/', use_proxy=True)
    print(cookies)
    headers = {
            'Host':'www.qichacha.com',
            'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0', 
            'cookie':'UM_distinctid=166c812152d9aa-080d8f12550a04-8383268-1fa400-166c812152ebd9; zg_did=%7B%22did%22%3A%20%22166c812166ed6-0b52f8c8ed9ab5-8383268-1fa400-166c812166f591%22%7D; _uab_collina=154095492261001212862089; acw_tc=2a510ca615409549256816616ec65469f5e2e5af3f47cdd6940b15e937; QCCSESSID=kn1rthbphls18d31o11l28idd1; saveFpTip=true; hasShow=1; CNZZDATA1254842228=126119758-1540954455-https%253A%252F%252Fwww.baidu.com%252F%7C1543400815; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1543386480,1543391312,1543399757,1543404128; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201543403511447%2C%22updated%22%3A%201543405443571%2C%22info%22%3A%201542936815467%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1543405444'
            }
    url6 = 'https://www.qichacha.com/search?key=' + '昆明恒海科技有限公司'
    res = req.getpage(url6, use_proxy=True, cookies=cookies, timeout=20)
    print(res)
    # res = req.getpage(url5, use_proxy=True, browser='chrome')
    # print(res)




if __name__ == "__main__":
    main()
