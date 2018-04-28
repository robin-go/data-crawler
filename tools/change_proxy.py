import json
import time

import requests


class GetProxy(object):
    """获取保存代理,并按需求给爬虫程序提供代理"""

    def __init__(self):
        self.proxy_list = []
        self.current_proxy = ''

    def save_proxies(self):
        # 获取代理并存入代理列表
        response = requests.get('https://proxyapi.mimvp.com/api/fetchopen.php?orderid=860180122190455733&num=20&http_type=1&anonymous=5&result_fields=1,2&result_format=json')
        response = json.loads(response.text)

        error_code = response.get('code', 0)  # 错误码13说明接口访问频率过快
        result = response.get('result')
        if error_code == 13:
            time.sleep(5)
            print('*********************************')
            self.save_proxies()
        else:
            for proxy in result:
                proxy = '%s://%s' % (proxy.get('http_type'), proxy.get('ip:port'))
                self.proxy_list.append(proxy)

    def update(self):
        # 更新current_proxy
        if len(self.proxy_list) == 0:
            self.save_proxies()
        proxy = self.proxy_list.pop()
        if self.judge_proxy(proxy):
            self.current_proxy = proxy
        else:
            self.update()


    def judge_proxy(self, proxy):
        # 用代理ip访问百度，判断代理是否可用
        url = 'http://www.baidu.com'
        try:
            proxy_dict = {
                "http": proxy,
            }
            response = requests.get(url, proxies=proxy_dict)
        except Exception as e:
            print("bad proxy")
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective proxy")
                return True
            else:
                print("bad proxy")
                return False

# 直接生成对象,在中间件import时直接使用单例模式,保证代理列表不被刷新
get_proxy = GetProxy()


