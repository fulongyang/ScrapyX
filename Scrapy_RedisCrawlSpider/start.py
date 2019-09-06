




import os

import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scrapy.cmdline import execute



# os.system('scrapy crawl GlobrandRedisCrawlSpider')

# execute(['scrapy','crawl','qj_spider'])
execute(['scrapy','crawl','GlobrandRedisCrawlSpider'])



'lpush GlobrandRedisCrawlQueue:GlobrandRedisCrawlQueue https://china.globrand.com/join/1/'




