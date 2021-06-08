# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/3/29
# tool      ：PyCharm
import json
import os
import random
from loguru import logger
import time
import hashlib
import pymysql
import requests
import datetime
import re

from multiprocessing import Pool, Process
from functools import partial


class Proxy:

    def request(self, url, headers):

        '''
        :param same as requests.get params
        '''

        # 每次请求一个新的网页前，先获取新的ip，通过这个IP访问
        proxies = self.fetch_one()

        # 通过代理发送请求
        return requests.get(url, headers=headers, proxies=proxies, timeout=20)

    # 获取新的ip和端口号
    def fetch_one(self):
        '''
        ip池购买网址,账号,密码
        # http://www.zhilianhttp.com/Index/getapi.html
        # 账号：terry21
        # 密码：123456789aA$
        :return:
        '''
        proxy_url = 'http://t.ipjldl.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&groupid=0&qty=1&time=1&pro=&city=&port=1&format=json&ss=5&css=&ipport=1&dt=1&specialTxt=3&specialJson=&usertype=16'
        while True:
            try:
                # 返回一个json {"code":0,"success":"true","msg":"","data":[{"IP":"122.232.37.233:28803"}]}
                r = requests.get(proxy_url, timeout=60)
                if r.status_code != 200:
                    logger.warning('请求失败：{}'.format(r.status_code))
            except Exception as e:
                logger.error(e)
            # text = r.content
            # ip_ports = re.findall('\d+.\d+.\d+.\d+:\d+', str(text))
            text = json.loads(r.text)
            # print(text)
            ip_ports = text['data'][0]['IP']
            print(ip_ports)
            if ip_ports:
                break
        ip_port = {'https': 'https://' + ip_ports}
        return ip_port

class DataBaseHandlerABC:
    def __init__(self, envir='debug'):
        pass



class CrawlerABC:
    def __init__(self):
        with open('{}/../conf/user_agents.txt'.format(os.path.split(__file__)[0]), 'r', encoding='utf-8') as f:
            self.user_agents = f.readlines()
        self.cookies = [
            '__cfduid=dd45fed1151427cd2927a6b880f2e82021595926590; __ssds=2; __auc=78ae8e2317394a338f9f5910996; _ga=GA1.2.880461803.1595926592; _gid=GA1.2.1455488603.1595926592; __ssuzjsr2=a9be0cd8e; __uzmaj2=0899d6fd-555b-4e97-bb28-9b520f982479; __uzmbj2=1595926591; _fbp=fb.1.1595926592034.721529629; m2_analytics=disabled; __stripe_mid=d408c3fb-1a42-4a5b-a951-7e5d9e796ae6; custom_timeout=; m2_ip=45.255.126.164; mm2_cookieA=819ff2f6-881c-4d72-8169-3afb9e72acee; __gads=ID=f8f903995a846bdd:T=1595926755:S=ALNI_MY_OBFax_qGMzwamnKVC3STRkhvtA; WuxiaWorld.CsrfToken=CfDJ8Eo2mp8QJcZHjkgpukMnlzWn-ivyogon23aJ6mVuiQ8qsCjcw6JrWJLY0JKr8XDXKENUXvnyTUs4W-3hSHSgsERlK2lw-kN4TudLoGXGnnobd0IBpGiQcz9PhfbGG_RJuoO53lGnkVxOoLB88TDdqXs; pg_tc=not-sampled; ___iat_vis=A5C7472F21191E2F.1596019502670; __asc=06dfc2d11739a73731fd11e0919; _gat=1; AWSALB=WwEAaNGr/fCOd3Q7zmBqppm7YYFSKQS5StC15J3i3BoUiF4Pf6NXGkIVdFgAkI76EtsH+PtAfmGbAcJHIssDeC8hPrKRg5CezNqGougsARyieO9a0INDPMCtVNHJ; AWSALBCORS=WwEAaNGr/fCOd3Q7zmBqppm7YYFSKQS5StC15J3i3BoUiF4Pf6NXGkIVdFgAkI76EtsH+PtAfmGbAcJHIssDeC8hPrKRg5CezNqGougsARyieO9a0INDPMCtVNHJ; __uzmcj2=1787025320705; __uzmdj2=1596024288',
            '__cfduid=dd45fed1151427cd2927a6b880f2e82021595926590; __ssds=2; __auc=78ae8e2317394a338f9f5910996; _ga=GA1.2.880461803.1595926592; _gid=GA1.2.1455488603.1595926592; __ssuzjsr2=a9be0cd8e; __uzmaj2=0899d6fd-555b-4e97-bb28-9b520f982479; __uzmbj2=1595926591; _fbp=fb.1.1595926592034.721529629; m2_analytics=disabled; __stripe_mid=d408c3fb-1a42-4a5b-a951-7e5d9e796ae6; custom_timeout=; m2_ip=45.255.126.164; mm2_cookieA=819ff2f6-881c-4d72-8169-3afb9e72acee; __gads=ID=f8f903995a846bdd:T=1595926755:S=ALNI_MY_OBFax_qGMzwamnKVC3STRkhvtA; WuxiaWorld.CsrfToken=CfDJ8Eo2mp8QJcZHjkgpukMnlzWn-ivyogon23aJ6mVuiQ8qsCjcw6JrWJLY0JKr8XDXKENUXvnyTUs4W-3hSHSgsERlK2lw-kN4TudLoGXGnnobd0IBpGiQcz9PhfbGG_RJuoO53lGnkVxOoLB88TDdqXs; pg_tc=not-sampled; ___iat_vis=A5C7472F21191E2F.1596019502670; __asc=06dfc2d11739a73731fd11e0919; _gat=1; AWSALB=6DuOrQmhnvnzRuMZCi8tETzJIcJfcGWtm1p5fOm/T8905/5x+OzOxkDwY7BWBvnY4jYYeCVsmcmIBzbT6EFqGk4pj2hFYs6eco3APF3cp92oeQwjzWlzz0g6NF77; AWSALBCORS=6DuOrQmhnvnzRuMZCi8tETzJIcJfcGWtm1p5fOm/T8905/5x+OzOxkDwY7BWBvnY4jYYeCVsmcmIBzbT6EFqGk4pj2hFYs6eco3APF3cp92oeQwjzWlzz0g6NF77; __uzmcj2=2705224498553; __uzmdj2=1596024187'
            ]
        self.proxies = None

    def get_html(self, url):
        res = None
        while True:
            headers = {
                'User-Agent': random.choice(self.user_agents).strip(),
                'cookie': random.choice(self.cookies).strip()
            }
            # headers = {'User-Agent': str(UserAgent().random)}  # 'cookie': random.choice(cookies).strip()
            s = requests.session()
            s.keep_alive = False
            try:
                r = s.get(url, headers=headers, proxies=self.proxies, timeout=30)  # , timeout=300
                # logger.info('正在使用代理请求网页')
                # 获取页面信息
                # r = proxy_client.request(url, headers=headers)
                if r.status_code == 200 or r.status_code == 404:
                    # r = html.unescape(r)
                    # 为二进制格式
                    res = r.text
                    break
                else:
                    logger.debug('{}请求没成功,状态码{}'.format(url, r.status_code))
            except Exception as e:
                logger.info('重试{}'.format(url))
                logger.error(e)
        return res

    def get_time(self):
        return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())