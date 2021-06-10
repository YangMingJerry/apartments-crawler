# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/6/8
# tool      ：PyCharm
from data import data_path
from app.apartments_crawler import Crawler as Crawler_apartments
from app.streeteasy_crawler import Crawler as Crawler_streeteasy

json_save_path = data_path
sheets_url = 'https://docs.google.com/spreadsheets/d/14KGHHymCvKqTNizqU5D8eB5DhqmmlToWl7krQJw0jgo/edit#gid=1316632945'
use_url = True

location='brooklyn-ny'
beds_num=3
price_low=3000
price_high=4500
is_cat=1
is_washer=1



c1 = Crawler_apartments()
c2 = Crawler_streeteasy()
c_dict = {'apartments': c1,
          'streeteasy': c2}

url_list = [{
    'neighbourhood': 'williamsburg',
    'source': 'streeteasy',
    'url': 'https://streeteasy.com/3-bedroom-apartments-for-rent/williamsburg/status:open%7Cprice:3000-4000%7Camenities:washer_dryer,pets'
},
    {'neighbourhood': 'LIC',
     'source': 'streeteasy',
     'url': 'https://streeteasy.com/3-bedroom-apartments-for-rent/long-island-city/status:open%7Cprice:3000-4000%7Camenities:washer_dryer,pets'},
{
    'neighbourhood': 'greenpoint',
    'source': 'streeteasy',
    'url': 'https://streeteasy.com/3-bedroom-apartments-for-rent/greenpoint/status:open%7Cprice:3000-4000%7Camenities:washer_dryer,pets'
},
]
# refresh for every xx hours
time_sleep = 1/360

