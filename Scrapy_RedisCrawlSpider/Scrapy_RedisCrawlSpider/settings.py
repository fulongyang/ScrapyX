# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_RedisCrawlSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_RedisCrawlSpider'

SPIDER_MODULES = ['Scrapy_RedisCrawlSpider.spiders']
NEWSPIDER_MODULE = 'Scrapy_RedisCrawlSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy_RedisCrawlSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    # 'Scrapy_RedisCrawlSpider.middlewares.PpRediscrawlspiderSpiderMiddleware': 543,
#    'Scrapy_RedisCrawlSpider.middlewares.RandomProxyMiddleware': 100,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'Scrapy_RedisCrawlSpider.middlewares.RandomProxyMiddleware': 100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'Scrapy_RedisCrawlSpider.pipelines.PpRediscrawlspiderPipeline': 300,
   'Scrapy_RedisCrawlSpider.pipelines.MongoPipeline': 200,
   'Scrapy_RedisCrawlSpider.pipelines.MysqlTwistedPipeline': 205,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'







# #--------------mysql

MYSQL_HOST           = 'mysql host'
MYSQL_DBNAME         = 'spider_data'         #数据库名字，请修改
MYSQL_USER           = 'root'             #数据库账号，请修改
MYSQL_PASSWORD       = 'mysql password'         #数据库密码，请修改
MYSQL_PORT           = 3306               #数据库端口
MYSQL_CHARSET        = 'utf8'               #
MYSQL_TABLE          = 'mysql table'               #






#---------------redis


# 设置重启爬虫时是否清空爬取队列
# 这样每次重启爬虫都会清空指纹和请求队列,一般设置为False
# SCHEDULER_FLUSH_ON_START=True

# 过滤器
DUPEFILTER_CLASS        = "scrapy_redis.dupefilter.RFPDupeFilter"
# DUPEFILTER_CLASS        = False
# # 调度器
SCHEDULER               = "scrapy_redis.scheduler.Scheduler"

# # 调度状态持久化设置为为True则不会清空redis里的dupefilter和requests队列
SCHEDULER_PERSIST       = True

# # 请求调度使用优先队列
SCHEDULER_QUEUE_CLASS   = 'scrapy_redis.queue.SpiderPriorityQueue'


REDIS_HOST              = '----redis house----'
REDIS_PORT              = 6379

# REDIS_URL = 'redis://user:pass@hostname:9001'
REDIS_ENCODING          = 'utf-8'
REDIS_PARAMS            = {'password':'----redis password ---'}


# The item pipeline serializes and stores the items in this redis key.
REDIS_ITEMS_KEY         = '%(spider)s:items'








#---------------------mongo
MONGO_URI               ='---- mongo host:port----'
MONGO_DATABASE          ='test'
MONGO_TABLE             ='pp_data'





#------------增加并发
# 默认 Item 并发数：100
CONCURRENT_ITEMS                    = 100
#
# # 默认 Request 并发数：16
CONCURRENT_REQUESTS                 = 120
#
# # 默认每个域名的并发数：8
CONCURRENT_REQUESTS_PER_DOMAIN    = 6
#
# # 每个IP的最大并发数：0表示忽略
CONCURRENT_REQUESTS_PER_IP        = 5

# #最大线程池
REACTOR_THREADPOOL_MAXSIZE        = 30








