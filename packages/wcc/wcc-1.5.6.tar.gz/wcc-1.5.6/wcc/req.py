"""
代码较多的依赖requests
参考文档：http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
"""
import  re
import  requests
import  time
import  chardet
import  traceback
import  json
import  os
import  random
from    selenium import webdriver
from    selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from    .proxy import get_proxy

def getpage(url, **kwargs):
    """
    使用get方式获取url对应的网页源码,如果是访问接口的话，返回是json字符串.
    :param url: 网页的url 
    :param headers: 请求头,默认从请求头库中随机选择一个
    :param timeout: 超时时间，默认是10s
    :param use_proxy: 是否使用代理，默认为True
    :param browser: 是否使用浏览器，默认为None，可选择chrome/firefox/None
    :param params: GET请求附带的参数，requests会把这个字典的params做成?k1=v1&k2=v2形式发送出去.
    :param payload: POST请求附带的参数.
    :param http_method: GET/POST/PUT/DELETE,必须接口
    :param use_ssl: 使用浏览器时是否使用ssl.
    :param wait: 浏览器的等待时间.
    :param cookies: 访问时的cookies.
    :return:经过渲染之后的网页源代码，是一个字符串
    """
    DEFAULT_TIMEOUT = 60
    MAX_TRY_COUNT = 1

    headers     = kwargs['headers']     if 'headers'    in kwargs else {'User-Agent':getua()}
    timeout     = kwargs['timeout']     if 'timeout'    in kwargs else DEFAULT_TIMEOUT
    use_proxy   = kwargs['use_proxy']   if 'use_proxy'  in kwargs else False
    browser     = kwargs['browser']     if 'browser'    in kwargs else None
    params      = kwargs['params']      if 'params'     in kwargs else None
    payload     = kwargs['payload']     if 'payload'    in kwargs else None
    http_method = kwargs['http_method'] if 'http_method'in kwargs else "GET"
    use_ssl     = kwargs['use_ssl']     if 'use_ssl'    in kwargs else False
    wait        = kwargs['wait']        if 'wait'       in kwargs else 0.5
    cookies     = kwargs['cookies']     if 'cookies'    in kwargs else None
    MAX_TRY_COUNT     = int(kwargs['max_try'])     if 'max_try'    in kwargs else 1
    
    if cookies != None:
        cookies = json.loads(cookies)

    resp_text        = ""
    resp_content     = ""
    error_text       = "error"
    resp_status_code = 200
    try_count        = 0
    error_flag       = False
    for k in range(0, MAX_TRY_COUNT):
        try:
            requests_params = {}
            #根据是否使用浏览器构造requests_param           
            # headers肯定有，至少也得随机一个User-Agent过来
            requests_params['headers'] = headers
            if timeout:
                requests_params['timeout'] = timeout
            if cookies is not None:
                requests_params['cookies'] = cookies

            if browser == 'chrome' or browser == 'firefox':
                requests_params['wait'] = wait

                # 浏览器中需要判断是否使用ssl，比如访问某些https的图片链接等
                if use_ssl:
                    requests_params['use_ssl'] = True
                if use_proxy:
                    proxy_iport = get_proxy(use_proxy)
                    if proxy_iport[0]:
                        requests_params['use_proxy'] = True
                        requests_params['proxy_ip'] = proxy_iport[0]
                        requests_params['proxy_port'] = proxy_iport[1]

                if params:
                    requests_params['params'] = params
                if payload:
                    requests_params['data'] = payload
            else:
                if use_proxy:
                    proxy_iport = get_proxy(use_proxy)
                    if proxy_iport[0]:
                        proxy_http  = 'http://' + proxy_iport[0] + ':' + str(proxy_iport[1])
                        proxy_https = 'https://' + proxy_iport[0] + ':' + str(proxy_iport[1])
                        requests_params['proxies'] = { "http": proxy_http, "https": proxy_https}
                if params:
                    requests_params['params'] = params
                if payload:
                    requests_params['data'] = payload
           
            if browser == 'chrome':
                resp_status_code, resp_text = getpage_browser_chrome(url, **requests_params)
            elif browser == 'firefox':
                resp_status_code, resp_text = getpage_browser_firefox(url, **requests_params)
            else:
                if http_method == "GET":
                    resp = requests.get(url, **requests_params) 
                    resp_status_code = resp.status_code
                    resp_text = resp.text
                    resp_content = resp.content # content留着，方便编码解码，尽管目前没有使用
                elif http_method == "POST":
                    resp = requests.post(url, **requests_params)
                    resp_status_code = resp.status_code
                    resp_text = resp.text
                    resp_content = resp.content
                else:
                    error_text = "不可预料的HTTP_METHOD"
                    print("url "+error_text)
                    break 
            if resp_status_code != 200:
                error_flag = True
                error_text = "resp_status_code "+str(resp_status_code)
                if resp_status_code == 503:
                    error_text = "503错误,您的IP可能被封"
                if resp_status_code == 504:
                    error_text = "504错误,您的IP可能被封"
                if resp_status_code == 405:
                    error_text = "405错误,您的方法是"+http_method

                time.sleep(0.5*k)
                continue
            else:
                error_flag = False
                try_count = k
                break
        except requests.exceptions.ConnectTimeout:
            error_flag = True
            error_text = "链接超时"
        except requests.exceptions.Timeout:
            error_flag = True
            error_text = "超时"
        except Exception as err:
            print(traceback.format_exc())
            error_flag = True
            error_text = str(err)
            print(url+" error "+str(err))
            print(resp_text)
        try_count   = k
     
    if error_flag:
        print(url + " error " + "(" + str(try_count) + " th)  "+error_text)
        return None
    else:
        #print(url+" ok"+"("+str(try_count)+" th) ")
        return resp_text

def getpage_browser_firefox(url, **kwargs):
    """
    使用火狐浏览器打开url并获取网页源码
    :param url:网页的url 
    :param use_proxy:是否使用代理，默认为True 
    :param user_agent:请求头的User_Agent，默认从请求头配置库中随机选择一个 
    :param wait:渲染页面的等待时间，默认是0.5
    :return:经过渲染之后的网页源代码，是一个字符串
    """
    use_proxy = kwargs['use_proxy'] if 'use_proxy' in kwargs else True
    user_agent = kwargs['user_agent'] if 'user_agent' in kwargs else getua()
    wait = kwargs['wait'] if 'wait' in kwargs else 0.5
    use_ssl = kwargs['use_ssl'] if 'use_ssl' in kwargs else False

    # 火狐浏览器代理配置
    profile = FirefoxProfile()

    if use_proxy:
        # 0表示直接连接，1表示使用代理
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.http', kwargs['proxy_ip'])
        profile.set_preference('network.proxy.http_port', kwargs['proxy_port'])

        # 有些资源需要ssl验证，比如一些https的图片，这种情况需要配置ssl
        if use_ssl:
            if url[0:6] == 'https:':
                profile.set_preference('network.proxy.ssl', ip)
                profile.set_preference('network.proxy.ssl_port', port)

        # 所有协议共用一种 ip 及端口，如果单独配置，不必设置该项，因为其默认为 False
        profile.set_preference("network.proxy.share_proxy_settings", True)

        # 所有项配置完成后需要update_preferences，然后才能正常使用
        # 如果某些项配置不正确，可以在启动的浏览器中输入about:config来查看具体的配置情况
        profile.update_preferences()

    # 火狐浏览器其他配置
    # 可以参考 https://www.cnblogs.com/baoyu7yi/p/7058537.html
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')      # 使用无头模式
    options.add_argument('--disable-gpu')   # 不使用gpu
    options.add_argument('user-agent=' + user_agent)    # 更改请求头

    resp_status_code = 0
    resp_text = ""
    try:  
        browser = webdriver.Firefox(profile, options=options)
        #browser = webdriver.Firefox()
        # 打开网页，渲染网页需要等待一定的时间，这个时间应该人为指定
        # selenium默认的等待时间不可靠，需要用time中的方法来指定
        browser.get(url)
        time.sleep(wait)
        # resp_status_code = browser
        resp_text = browser.page_source
    except Exception as err:
        print ("打开浏览器失败:"+ str(err))

    browser.quit()
    #Quits the driver and closes every associated window. 
    #退出驱动并关闭所有关联的窗口。
    #Closes the current window. 
    #关闭当前窗口。
    return 200 if resp_text else None, resp_text

def getpage_browser_chrome(url, **kwargs):
    """
    使用谷歌浏览器打开url并获取网页源码
    浏览器暂时不支持referer，selenium不支持referer
    如果确实需要，就必须使用一个新的工具：browsermob-proxy
    这个工具的开源地址是：https://github.com/webmetrics/browsermob-proxy
    :param url:网页的url 
    :param use_proxy:是否使用代理，默认为True 
    :param user_agent:请求头的User_Agent，默认从请求头配置库中随机选择一个 
    :param wait:渲染页面的等待时间，默认是0.5
    :param cookies:访问网站时的cookies
    :return:经过渲染之后的网页源代码，是一个字符串
    """
    use_proxy   = kwargs['use_proxy']   if 'use_proxy'  in kwargs else False
    wait        = kwargs['wait']        if 'wait'       in kwargs else 0.5
    use_ssl     = kwargs['use_ssl']     if 'use_ssl'    in kwargs else False
    cookies     = kwargs['cookies']     if 'cookies'    in kwargs else None
    timeout     = kwargs['timeout']     if 'timeout'    in kwargs else 60
    user_agent  = kwargs['headers']['User-Agent'] if 'headers' in kwargs and 'User-Agent' in kwargs['headers'] else None

    chrome_options = webdriver.ChromeOptions()

    # 浏览器代理配置
    # 参考 https://developers.google.com/web/updates/2017/04/headless-chrome
    if use_proxy:
        PROXY = kwargs['proxy_ip'] + ':' + str(kwargs['proxy_port'])
        chrome_options.add_argument('--proxy-server={0}'.format(PROXY))

    # 浏览器其他配置
    chrome_options.add_argument('--headless')       # 使用无头模式
    chrome_options.add_argument('--disable-gpu')  # 不使用gpu

    # 更改请求头
    if user_agent:
        chrome_options.add_argument('user-agent=' + user_agent)         # 更改请求头

    resp_text = ""
    try:  
        browser = webdriver.Chrome(options=chrome_options)
        # 打开网页，渲染网页需要等待一定的时间，这个时间应该人为指定
        # selenium默认的等待时间不可靠，需要用time中的方法来指定
        # 设置连接超时时间，默认是60秒
        browser.set_page_load_timeout(timeout)
        browser.get(url)
        # https://www.cnblogs.com/mengyu/p/7078561.html
        cookiesList = []
        if cookies:
            for cookieName, cookieValue in cookies.items():
                cookie_item = {}
                cookie_item['name'] = cookieName
                cookie_item['value'] = cookieValue
                cookiesList.append(cookie_item)
                browser.add_cookie(cookie_item)
            browser.refresh()
        time.sleep(wait)
        resp_text = browser.page_source
    except Exception as err:
        print ("打开浏览器失败:"+ str(err))
    finally:
        browser.quit()
        #Quits the driver and closes every associated window. 
        #退出驱动并关闭所有关联的窗口。
        #Closes the current window. 
        #关闭当前窗口。
    return 200 if resp_text else None, resp_text

def getcookie(url, **kwargs):
    """
    使用谷歌浏览器打开url并获取网页cookie
    :param url:网页的url 
    :param use_proxy:是否使用代理，默认为True 
    :param user_agent:请求头的User_Agent，默认从请求头配置库中随机选择一个 
    :param wait:渲染页面的等待时间，默认是0.5
    :return:经过渲染之后的网页源代码，是一个字符串
    """
    use_proxy   = kwargs['use_proxy'] if 'use_proxy' in kwargs else False
    user_agent  = kwargs['User-Agent'] if 'User-Agent' in kwargs else getua()
    wait        = kwargs['wait'] if 'wait' in kwargs else 0.5
    use_ssl     = kwargs['use_ssl'] if 'use_ssl' in kwargs else False

    # 浏览器代理配置
    # 参考 https://developers.google.com/web/updates/2017/04/headless-chrome
    chrome_options = webdriver.ChromeOptions()

    if use_proxy:
        proxy_iport = get_proxy(use_proxy)
        if proxy_iport[0]:
            proxy_ip    = proxy_iport[0]
            proxy_port  = proxy_iport[1]
            PROXY       = proxy_ip + ':' + str(proxy_port)
            chrome_options.add_argument('--proxy-server={0}'.format(PROXY))

    # 浏览器其他配置
    chrome_options.add_argument('--headless')       # 使用无头模式
    # chrome_options.add_argument('--disable-gpu')  # 不使用gpu
    chrome_options.add_argument('user-agent=' + user_agent)         # 更改请求头

    cookie_str = ""
    try:  
        browser = webdriver.Chrome(options=chrome_options)
        # 打开网页，渲染网页需要等待一定的时间，这个时间应该人为指定
        # selenium默认的等待时间不可靠，需要用time中的方法来指定
        browser.get(url)
        #获取cookies
        cookie_items = browser.get_cookies()
        post = {}
        #获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
        for cookie_item in cookie_items:
            post[cookie_item['name']] = cookie_item['value']
        # for item_key, item_value in cookie_items.item():
        #     post[item_key] = item_value
        cookie_str = json.dumps(post)
    except Exception as err:
        print ("打开浏览器失败:"+ str(err))

    browser.quit()
    #Quits the driver and closes every associated window. 
    #退出驱动并关闭所有关联的窗口。
    #Closes the current window. 
    #关闭当前窗口。
    return  cookie_str

def getua(path = 'user_agents.json'):
    """
    从配置文件user_agents.json中随机获取一个User_Agent
    :return:一个随机获取的User_Agent字符串
    """
    current_path = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(current_path, path)
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            user_agents = json.load(f)
            num = random.randint(0, len(user_agents) - 1)
            return user_agents[num]
    except:
        print (u"打开配置文件失败")
        return None

