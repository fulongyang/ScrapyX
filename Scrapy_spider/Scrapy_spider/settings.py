# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_spider'

SPIDER_MODULES      = ['Scrapy_spider.spiders']
NEWSPIDER_MODULE    = 'Scrapy_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy_spider (+http://www.yourdomain.com)'

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
#SPIDER_MIDDLEWARES = {
#    'Scrapy_spider.middlewares.PpSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'Scrapy_spider.middlewares.PpSpiderDownloaderMiddleware': 543,
   'Scrapy_spider.middlewares.RandomProxyMiddleware': 200,  #add proxy ip


}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'Scrapy_spider.pipelines.PpSpiderPipeline': 300,

    'Scrapy_spider.pipelines.MysqlTwistedPipeline'    : None,   #seve to mysql
    'Scrapy_spider.pipelines.MongoPipeline'           : None,   #save to mongo
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

MYSQL_HOST           = 'mysql host'          #mysql host
MYSQL_DBNAME         = 'spider_data'         #数据库名字，请修改
MYSQL_USER           = 'root'                #数据库账号，请修改
MYSQL_PASSWORD       = 'mysql password'   #数据库密码，请修改
MYSQL_PORT           = 3306                  #数据库端口
MYSQL_CHARSET        = 'utf8'                #
MYSQL_TABLE          = '***'   #数据库表名






#---------------------mongo
MONGO_URI               ='mongo host:port'
MONGO_DATABASE          ='test'
MONGO_TABLE             ='pp_data'





#--------------------性能配置

# #禁止重定向
# REDIRECT_ENABLED = True

#请求超时
DOWNLOAD_TIMEOUT = 30






#-----------------并发配置
# 默认 Item 并发数：100
CONCURRENT_ITEMS                    = 10
#
# # 默认 Request 并发数：16
CONCURRENT_REQUESTS                 = 5
#
# # 默认每个域名的并发数：8
CONCURRENT_REQUESTS_PER_DOMAIN      = 5
#
# # 每个IP的最大并发数：0表示忽略
CONCURRENT_REQUESTS_PER_IP          = 30

# #最大线程池
REACTOR_THREADPOOL_MAXSIZE          = 50




#---------------------------限速配置

#延迟爬取  默认 60.
# AUTOTHROTTLE_MAX_DELAY  =3.0


#
#禁止cookie
# COOKIES_ENABLED = True

#
# #
# # #禁止重试
# RETRY_ENABLED = False
#
# #
# # #减少下载超时
# DOWNLOAD_TIMEOUT = 15
#
#
# #禁止重定向
# REDIRECT_ENABLED = True

#下载延迟
# AUTOTHROTTLE_START_DELAY=2


