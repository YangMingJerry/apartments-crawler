# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/6/8
# tool      ：PyCharm

from lxml import etree
from loguru import logger

from schema.crawler_abc import *


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


class Crawler(CrawlerABC):
    def html_parser(self, html):
        ehtml = etree.HTML(html)
        rooms = ehtml.xpath('//li[@class="mortar-wrapper"]')
        out = {}
        for room in rooms:
            room_out = {}
            room_out['url'] = room.xpath('.//a[@class="property-link"]/@href')
            room_out['price'] = room.xpath('.//div[@class="price-range"]/text()')
            address_1 = room.xpath('.//div[@class="property-title"]//text()')[0]
            address_2 = room.xpath('.//div[@class="property-address js-url"]/text()')[0]
            room_out['address'] = address_1 + ' | ' + address_2
            room_out['phone'] = room.xpath('.//div[@class="phone-wrapper"]//span/text()')
            room_out['update_at'] = room.xpath('.//span[@class="lastUpdated"]/span/text()')
            out[room_out['address']] = room_out
        return out

    def get_url(self, **kwargs):
        location = kwargs.get('location')
        beds_num = kwargs.get('beds_num')
        price_low = kwargs.get('price_low')
        price_high = kwargs.get('price_high')
        is_cat = kwargs.get('cat')
        is_washer = kwargs.get('washer')
        "https://www.apartments.com/queens-ny/3-bedrooms-3000-to-4200-pet-friendly-cat/washer-dryer/"
        url = f'https://www.apartments.com/{location}/{beds_num}-bedrooms-{price_low}-to-{price_high}'
        if is_cat:
            url = url + '-pet-friendly-cat'
        if is_washer:
            url = url + '/washer-dryer/'
        return url

    def write_back_json(self, out):
        js = JsonHandler(path='apartments.json')
        for key, value in out.items():
            if not js.is_in_json(key):
                js.update_json(key,value)
                logger.info(f'NEW ROOM FOUND: {key}')
            elif js.is_changed(key,value):
                js.update_json(key,value)
                logger.info(f'ROOM CHANGED: \naddress: {key}\ncontent: {value}')
            else:
                logger.info(f'PASS, OLD ROOM: {key}')
        js.write_back()




    def run(self, **kwargs):
        url = self.get_url(**kwargs)
        html = self.get_html(url)
        out = self.html_parser(html)
        self.write_back_json(out)



if __name__ == '__main__':
    c = Crawler()
    c.run(location='brooklyn-ny', beds_num=3, price_low=3000, price_high=4500, is_cat=1, is_washer=1)

