# apartments-crawler
fuck nyc rent price

本脚本实现了apartments.com网站的爬虫。

在/app/apartments_crawler.py脚本中：

- 根据条件执行：
  ```python
    c = Crawler()# run by conditions
    c.run(
              location= 'brooklyn-ny', 
              beds_num= 3, 
              price_low= 3000, 
              price_high= 4500, 
              is_cat= 1, 
              is_washer= 1
          )
  ```
- 根据已有url执行，在网站apartments.com输入条件后复制网站生成的url运行：
  ```python
      # run by existed url to save what you see
      c.run_by_url(
              url='https://www.apartments.com/3-bedrooms-3000-to-4200-pet-friendly-cat/washer-dryer/?bb=3mm6-t99vHw98oooB'
          )
  ```
