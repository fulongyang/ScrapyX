








#-----------------run spider
from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy','crawl','qj_spider'])
# execute(['scrapy','crawl','maigoo_spider'])


#----------抓取不重复
# execute(['scrapy','crawl','qj_spider','-s','JOBDIR=spider_info/001'])
# execute(['scrapy','crawl','maigoo_spider','-s','JOBDIR=spider_info/002'])














