# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/6/8
# tool      ：PyCharm

import sys
import time

from loguru import logger

from conf.configure import *
from utils.google_sheet_handler import GoogleSheetHandler

time_sleep_sec = time_sleep * 3600
gsh = GoogleSheetHandler(sheets_url)

def count_down(time_left):
    while time_left > 0:
        print(f'\rrefresh in:{time_left}(s)',end="")
        time.sleep(1)
        time_left = time_left - 1

def unit_worker(unit):
    neigh = unit['neighbourhood']
    url = unit['url']
    source = unit['source']
    c = c_dict.get(source, None)
    if not c:
        logger.error(f'CANT find parser for unit{unit}')
        return

    out = c.run_by_url(url, mode='json')
    for key, value in out.items():
        value['neighbourhood'] = neigh
        value['source'] = source
    gsh.writeback(out)

def nous_allons():

    while True:
        gsh.purge()
        for unit in url_list:
            unit_worker(unit)
            # else:
            #     c.run(
            #             location= location ,
            #             beds_num= beds_num,
            #             price_low= price_low,
            #             price_high= price_high,
            #             is_cat= is_cat,
            #             is_washer= is_washer
            #     )
        count_down(time_sleep_sec)

if __name__ == '__main__':
    nous_allons()

