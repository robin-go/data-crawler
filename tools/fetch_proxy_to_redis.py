# coding:utf-8

import random
import time
import requests
import gevent
from gevent import monkey

import redis

monkey.patch_all()


class ProxyIp(object):
    """获取代理验证并存进redis"""

    def __init__(self):
        self.iplist = []
        self.r = redis.StrictRedis(host='localhost', port=6379)

    def requests_url(self, url):
        """获取代理ip"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        result = requests.get(url, headers=headers, timeout=10)
        print(result.status_code)
        if result.status_code == 200:
            return result.text

    def check_ip(self, ip):
        """验证代理ip是否可用"""
        proxies = {
            'http': 'http://' + ip,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        url_list = [
            'http://www.xiachufang.com/category/40076/',
            'http://www.xiachufang.com/category/40077/',
            'http://www.xiachufang.com/category/40078/',
            'http://www.xiachufang.com/category/40071/',
            'http://www.xiachufang.com/category/957/',
            'http://www.xiachufang.com/category/394/',
            'http://www.xiachufang.com/category/20130/',
            'http://www.xiachufang.com/category/20133/',
            'http://www.xiachufang.com/category/51490/',
            'http://www.xiachufang.com/category/51761/',
        ]

        url = random.choice(url_list)
        try:
            result = requests.get(url, proxies=proxies, headers=headers, timeout=10)
        except Exception as e:
            print(ip + '访问出错，代理不可用：' + str(e))
        else:
            print(result.status_code)
            if result.status_code == 200:
                self.iplist.append('http://' + ip)

    def save_ip(self):
        """可用代理存到redis"""
        for ip in self.iplist:
            self.r.setex(ip, 140, 0)

    def start(self):
        while True:
            try:
                url = 'https://proxy.horocn.com/proxies?order_id=1590365027257304274&num=20&format=text'
                response_text = self.requests_url(url)
                ip_list = response_text.split('\n')
                tasks = []
                for ip in ip_list:
                    if len(tasks) <= 40:
                        tasks.append(gevent.spawn(self.check_ip, ip))
                    else:
                        tasks.append(gevent.spawn(self.check_ip, ip))
                        # 防止丢数据。
                        gevent.joinall(tasks)
                        tasks = []
                if len(tasks) != 0:
                    gevent.joinall(tasks)
                    tasks = []
                self.save_ip()
                self.iplist = []
            except Exception as e:
                print('error' + str(e))
            time.sleep(10)


if __name__ == '__main__':
    proxy = ProxyIp()
    proxy.start()
