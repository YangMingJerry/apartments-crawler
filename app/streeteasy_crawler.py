# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/6/10
# tool      ：PyCharm

from lxml import etree
from loguru import logger

from schema.crawler_abc import *


class Crawler(CrawlerABC):

    def html_parser(self, html):
        ehtml = etree.HTML(html)
        rooms = ehtml.xpath('//*[@id="result-details"]/div[1]/ul/li')
        out = {}
        for room in rooms:
            room_out = {}
            room_out['url'] = room.xpath('./div/a/@href')[0]
            room_out['price'] = room.xpath('.//div[@class="listingCardBottom-emphasis"]/span/text()')
            room_out['address'] = room.xpath('.//address/a/text()')[0]
            room_out['phone'] = []
            room_out['update_at'] = []
            out[room_out['address']] = room_out
        return out

    def get_save_path(self, json_save_path):
        name = os.path.split(__file__)[-1].split('_')[0]
        # name = os.path.split(os.path.abspath(sys.argv[0]))[-1].split('_')[0]
        path = json_save_path.replace('__token__',name)
        return path

if __name__ == '__main__':
    c = Crawler()
    url_1 = 'https://streeteasy.com/3-bedroom-apartments-for-rent/williamsburg/status:open%7Cprice:3000-4000%7Camenities:washer_dryer,pets'
    c.run_by_url(url_1)