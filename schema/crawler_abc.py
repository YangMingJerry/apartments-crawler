# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/3/29
# tool      ：PyCharm
import json
import os
import random

from loguru import logger
import time
import requests

from utils.google_sheet_handler import GoogleSheetHandler
from data import data_path as json_save_path
sheets_url = 'https://docs.google.com/spreadsheets/d/14KGHHymCvKqTNizqU5D8eB5DhqmmlToWl7krQJw0jgo/edit#gid=1316632945'

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

class JsonHandler:
    def __init__(self, path):
        self.path = path
        self.content = self.load_json()

    def is_in_json(self, key):
        return key in self.content

    def is_changed(self, key, content):
        return self.content.get(key,None) != content

    def update_json(self, key, content):
        self.content[key] = content

    def write_back(self):
        out_str = json.dumps(self.content)
        with open(self.path, 'w') as file:
            file.write(out_str)

    def load_json(self):
        if not os.path.isfile(self.path):
            return {}
        with open(self.path, 'r') as file:
            out = file.read()
        out_json = json.loads(out)
        return out_json


class CrawlerABC:
    def __init__(self):
        with open('{}/../conf/user_agents.txt'.format(os.path.split(__file__)[0]), 'r', encoding='utf-8') as f:
            self.user_agents = f.readlines()
        self.cookies = [
            # '__cfduid=dd45fed1151427cd2927a6b880f2e82021595926590; __ssds=2; __auc=78ae8e2317394a338f9f5910996; _ga=GA1.2.880461803.1595926592; _gid=GA1.2.1455488603.1595926592; __ssuzjsr2=a9be0cd8e; __uzmaj2=0899d6fd-555b-4e97-bb28-9b520f982479; __uzmbj2=1595926591; _fbp=fb.1.1595926592034.721529629; m2_analytics=disabled; __stripe_mid=d408c3fb-1a42-4a5b-a951-7e5d9e796ae6; custom_timeout=; m2_ip=45.255.126.164; mm2_cookieA=819ff2f6-881c-4d72-8169-3afb9e72acee; __gads=ID=f8f903995a846bdd:T=1595926755:S=ALNI_MY_OBFax_qGMzwamnKVC3STRkhvtA; WuxiaWorld.CsrfToken=CfDJ8Eo2mp8QJcZHjkgpukMnlzWn-ivyogon23aJ6mVuiQ8qsCjcw6JrWJLY0JKr8XDXKENUXvnyTUs4W-3hSHSgsERlK2lw-kN4TudLoGXGnnobd0IBpGiQcz9PhfbGG_RJuoO53lGnkVxOoLB88TDdqXs; pg_tc=not-sampled; ___iat_vis=A5C7472F21191E2F.1596019502670; __asc=06dfc2d11739a73731fd11e0919; _gat=1; AWSALB=WwEAaNGr/fCOd3Q7zmBqppm7YYFSKQS5StC15J3i3BoUiF4Pf6NXGkIVdFgAkI76EtsH+PtAfmGbAcJHIssDeC8hPrKRg5CezNqGougsARyieO9a0INDPMCtVNHJ; AWSALBCORS=WwEAaNGr/fCOd3Q7zmBqppm7YYFSKQS5StC15J3i3BoUiF4Pf6NXGkIVdFgAkI76EtsH+PtAfmGbAcJHIssDeC8hPrKRg5CezNqGougsARyieO9a0INDPMCtVNHJ; __uzmcj2=1787025320705; __uzmdj2=1596024288',
            # '__cfduid=dd45fed1151427cd2927a6b880f2e82021595926590; __ssds=2; __auc=78ae8e2317394a338f9f5910996; _ga=GA1.2.880461803.1595926592; _gid=GA1.2.1455488603.1595926592; __ssuzjsr2=a9be0cd8e; __uzmaj2=0899d6fd-555b-4e97-bb28-9b520f982479; __uzmbj2=1595926591; _fbp=fb.1.1595926592034.721529629; m2_analytics=disabled; __stripe_mid=d408c3fb-1a42-4a5b-a951-7e5d9e796ae6; custom_timeout=; m2_ip=45.255.126.164; mm2_cookieA=819ff2f6-881c-4d72-8169-3afb9e72acee; __gads=ID=f8f903995a846bdd:T=1595926755:S=ALNI_MY_OBFax_qGMzwamnKVC3STRkhvtA; WuxiaWorld.CsrfToken=CfDJ8Eo2mp8QJcZHjkgpukMnlzWn-ivyogon23aJ6mVuiQ8qsCjcw6JrWJLY0JKr8XDXKENUXvnyTUs4W-3hSHSgsERlK2lw-kN4TudLoGXGnnobd0IBpGiQcz9PhfbGG_RJuoO53lGnkVxOoLB88TDdqXs; pg_tc=not-sampled; ___iat_vis=A5C7472F21191E2F.1596019502670; __asc=06dfc2d11739a73731fd11e0919; _gat=1; AWSALB=6DuOrQmhnvnzRuMZCi8tETzJIcJfcGWtm1p5fOm/T8905/5x+OzOxkDwY7BWBvnY4jYYeCVsmcmIBzbT6EFqGk4pj2hFYs6eco3APF3cp92oeQwjzWlzz0g6NF77; AWSALBCORS=6DuOrQmhnvnzRuMZCi8tETzJIcJfcGWtm1p5fOm/T8905/5x+OzOxkDwY7BWBvnY4jYYeCVsmcmIBzbT6EFqGk4pj2hFYs6eco3APF3cp92oeQwjzWlzz0g6NF77; __uzmcj2=2705224498553; __uzmdj2=1596024187'
            '_se_t=4dd7bba2-fe37-4bc3-b335-0a446710e76d; _gcl_au=1.1.539885244.1623143263; _ga=GA1.2.2005399838.1623143263; _pxvid=fbee2b4b-c838-11eb-915e-0242ac120010; zjs_anonymous_id=%224dd7bba2-fe37-4bc3-b335-0a446710e76d%22; KruxPixel=true; se%3Asearch%3Asales%3Astate=%7C%7C%7C%7C; g_state={"i_l":0}; zjs_user_id=%227451443%22; ezab_ursa_srp_filters_ab_test=show_legacy_filters; ezab=%7B%22ursa_srp_filters_ab_test%22%3A%22show_legacy_filters%22%7D; __gads=ID=d0e41e5bcd62690f:T=1623143320:S=ALNI_MawD5N0pM7mq163PkngGIIFE4ruxw; _gid=GA1.2.584473341.1623293298; se%3Asearch%3Ashared%3Astate=302%7C3%7C%7C%7Cfalse; se%3Asearch%3Arentals%3Astate=false%7C3000%7C4000%7C%7C; google_one_tap=0; anon_searcher_stage=initial; _uetsid=dc9aea40ca8911eb98840d0bed878247; _uetvid=8cf2a030c83911ebb56849077601e561; ki_r=; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IlcxczNORFV4TkRRelhTd2lla2Q1VVdWcmFtdDZRVzF2TFdrMFoyZDZlVmNpTENJeE5qSXpNemszT1RJMkxqWXlNRFl5TnpRaVhRPT0iLCJleHAiOiIyMDMxLTA2LTExVDA3OjUyOjA2WiIsInB1ciI6bnVsbH19--80ec9f76f823a96db61ad1bbfb96a63f9436b1b6; last_search_tab=rentals; se_rs=169948405; user_auth_token=YzHrjxZ8Dxu4yeV_f6n1; se_lsa=2021-06-11+03%3A58%3A03+-0400; _ses=L0dQdFhwWDJXS2QzTHJidGdpNGMxa3ZpbUEyVFQyWU5yTWxudzV6emlnVWZEM3UvdXNSUU94S2U1M0RsT3QyNUpXUEk4RzgwTkdYUFBDcitCcDdIbE44ZjBZWStrREhiNTZBMzdYMU5KUzY2V09FMm9oNVRQWDJLK3dPMmR0dEcxd2R0am9Fd2Q4RDBXeWowcXJzK0pyL2dYNHpuaEJ3TDc5OHFYMmp3VW1WanFhbWp3a0M3KzZmbFJSWlpYRndUMEpXTFVCbFBKd1lZYjlQblBwT0pPVysva0grSVV2KzA4U0J6ZDBpUHFpYWd0RTdyNzhLUllVeXdtcGlZYkZTemlyalhYdjhmcFMyR2lpR2Uvd1VUUWc9PS0td1B0SHhzQVViN3BCNTIzMVNDZ28xdz09--5c54508bcf7fde9fdac43e2a11e8ec65bcadd4c3; _px3=b8578cc2fd7b0cc75a556619e79fd34ec4fbc1ef8247a3ba84f35133e6ac9e1f:Rr38FityyM1vM5dbXbMyD54DqjU6jOYkcccijNmDCgYnoXJGcHkaiazkded2NK1tqvHZZ7zGPfrHrO13pb6ypQ==:1000:NNU2YIKd4BtWtnrff8W0FMJhbgI+nt7J16MGcjQ8t8lnLjlQlwpPHwYtgVFJZpS7HxFWGn261YOi9Lzh5SQgjAoqD5ElYcu/jlmbDH111cCp+9oRroUmnI0jwlo/fUrBCIQHyVnv9mtIxNRYahMJB7U9F9r2MKKSbCOA9eGYMukMO2cVn+zGuIko30O4eruU0OTzvbX9Q+I892iKickMhw==; ki_t=1623143272126%3B1623397619896%3B1623398283674%3B3%3B32'
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

    def write_back_json(self, out, json_save_path):
        js = JsonHandler(path= json_save_path)
        for key, value in out.items():
            if not js.is_in_json(key):
                js.update_json(key,value)
                logger.info(f'NEW ROOM FOUND: \naddress: {key}\ncontent: {value}')
            elif js.is_changed(key,value):
                js.update_json(key,value)
                logger.debug(f'ROOM CHANGED: \naddress: {key}\ncontent: {value}')
            else:
                # logger.info(f'PASS, OLD ROOM: {key}')
                pass
        js.write_back()

    def html_parser(self, html):
        pass

    def get_url(self, **kwargs):
        pass

    def run(self, **kwargs):
        url = self.get_url(**kwargs)
        return self.run_by_url(url, **kwargs.get('mode'))

    def run_by_url(self, url, mode):
        html = self.get_html(url)
        out = self.html_parser(html)
        if mode == 'json':
            self.write_back_json(out, self.get_save_path(json_save_path))
        elif mode == 'google sheets':
            self.write_back_google_sheets(out)
        return out

    def write_back_google_sheets(self, out):
        gsh = GoogleSheetHandler(sheets_url)
        gsh.writeback(out)


    def get_save_path(self, json_save_path):
        pass
        # name = os.path.split(__file__)[-1].split('_')[0]
        # # name = os.path.split(os.path.abspath(sys.argv[0]))[-1].split('_')[0]
        # path = json_save_path.replace('__token__',name)
        # return path