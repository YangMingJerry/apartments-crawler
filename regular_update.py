# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/6/8
# tool      ：PyCharm

import sys
import time

from app.apartments_crawler import Crawler
from conf.configure import *

time_sleep_sec = time_sleep * 3600


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
    time.sleep(time_sleep_sec)
