# Scrapy爬虫测试



# 提交代码时

pip install pipreqs

pipreqs . --force

# 初始化

scrapy startproject test_10jqka_us

###
cd test_10jqka_us
scrapy genspider test_10jqka_us_list 10jqka.com.cn
scrapy crawl test_10jqka_us_list

#shell
scrapy shell

fetch('https://stock.10jqka.com.cn/usstock/mgyw_list/')
response.css('head_topic')
response.css('arc-title')
response.css('head_topic')