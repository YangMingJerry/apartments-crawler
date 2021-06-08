# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/6/8
# tool      ：PyCharm

import sys
import time

from app.apartments_crawler import Crawler
from conf.configure import *

time_sleep_sec = time_sleep * 3600

def count_down(time_left):
    while time_left > 0:
        print(f'\rrefresh in:{time_left}(s)',end="")
        time.sleep(1)
        time_left = time_left - 1

c = Crawler()
while True:
    if use_url:
        c.run_by_url(url)
    else:
        c.run(
                location= location ,
                beds_num= beds_num,
                price_low= price_low,
                price_high= price_high,
                is_cat= is_cat,
                is_washer= is_washer
        )
    count_down(time_sleep_sec)



