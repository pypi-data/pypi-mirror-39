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

    # HEADERS = {
    #        'User-Agent':req.getua(),
    #        'cookie':req.getcookie('https://www.qichacha.com/', use_proxy=True)
    #        }
    # print(HEADERS)
    headers = {
            'Host':'www.qichacha.com',
            'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0', 
            'cookie':'UM_distinctid=1673edcdfcfde-0bcb90b156074f-4313362-1fa400-1673edcdfd059c; _uab_collina=154294792218704372338883; zg_did=%7B%22did%22%3A%20%221673edce18c72-06c85c74aba259-4313362-1fa400-1673edce18d627%22%7D; acw_tc=7cc1e21b15429767581062363e3013318cefb62ab0ec8f762198fad6ed; QCCSESSID=uf1318qj1jkl1n1jufc07v96g3; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1543085411,1543085444,1543090052,1543329769; saveFpTip=true; CNZZDATA1254842228=1151905855-1542975082-https%253A%252F%252Fwww.google.com%252F%7C1543416485; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201543419002268%2C%22updated%22%3A%201543419256374%2C%22info%22%3A%201542947922323%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22d10367ac3f8bcdf2a776a34152de7743%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1543419257'
            }

    url6 = 'https://www.qichacha.com/search?key=' + '昆明恒海科技有限公司'
    res = req.getpage(url6, use_proxy=True, headers=headers, timeout=20)
    print(res)
    # res = req.getpage(url5, use_proxy=True, browser='chrome')
    # print(res)




if __name__ == "__main__":
    main()
