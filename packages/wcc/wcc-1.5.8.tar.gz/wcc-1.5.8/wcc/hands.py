#针对企查查的爬虫代码.
#import wcc
#from wcc import getpage
from .req import getpage
import requests

def getpage_qichacha(url,**kwargs):
    max_try = 10
    timeout = 30
    if "max_try" in kwargs:
        max_try = int(kwargs["max_try"])
    if "timeout" in kwargs:
        timeout = int(kwargs["timeout"])
    resp_text = None
    actual_try = 0
    for k in range(max_try):
        actual_try +=1
        try:
            resp_text = getpage(url, use_proxy='all', timeout=timeout)
        except Exception as err:
            pass
        if not resp_text:
            continue
        if resp_text.startswith("<script>window.location.href='https://www.qichacha.com/index_verify?"):
            continue
        else:
            break
    if resp_text:
        print(url + " ok (" + str(actual_try)+"th)")
    else:
        print(url + " error ("+ str(actual_try)+"th)")
    return resp_text

def main():
    resp_html = getpage_qichacha("https://www.qichacha.com/firm_eda18f25c116f461879f838b15c596ae.html")
    print(resp_html)


if __name__ == "__main__":
    main()

