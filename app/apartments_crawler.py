# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/6/8
# tool      ：PyCharm

from lxml import etree
from loguru import logger

from schema.crawler_abc import *

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

    def get_save_path(self, json_save_path):
        name = os.path.split(__file__)[-1].split('_')[0]
        # name = os.path.split(os.path.abspath(sys.argv[0]))[-1].split('_')[0]
        path = json_save_path.replace('__token__',name)
        return path

if __name__ == '__main__':
    c = Crawler()

    # run by conditions
    c.run(location='brooklyn-ny', beds_num=3, price_low=3000, price_high=4500, is_cat=1, is_washer=1)

    # run by existed url to save what you see
    # c.run_by_url(url='https://www.apartments.com/3-bedrooms-3000-to-4200-pet-friendly-cat/washer-dryer/?bb=3mm6-t99vHw98oooB')
