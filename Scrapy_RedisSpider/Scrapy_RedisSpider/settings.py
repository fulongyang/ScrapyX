# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_RedisSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html




#################################################重要配置

#-------------------阿布云代理配置
ABY_PROXY_USER= ''
ABY_PROXY_PASS= ''
ABY_PROXY_PORT= ''
ABY_PROXY_HOST= ''


#-------------------mysql配置
MYSQL_SETTING = {
   'MYSQL_HOST':'',
   'MYSQL_DBNAME':'',
   'MYSQL_USER':'',
   'MYSQL_PASSWORD':'',
   'MYSQL_PORT':'',
   'MYSQL_CHARSET':'',
}


#---------------------mongo配置
MONGO_SETTING = {
   'MONGO_URI':'',
   'MONGO_DATABASE':'',
}


#----------------------redis配置
REDIS_SETTING={
'REDIS_HOST':'',
'REDIS_PORT':'',
}



#设置获取cookie的url
QICHACHA_COOKIES_URL = None
COOKIES_POOL_URL = None


#----------获取代理ip的url
QICHACHA_GET_IP_URL = "http://127.0.0.1:5010/get/" if False else None  #有接口代理请打开
QICHACHA_DELETE_IP_URL = "http://127.0.0.1:5010/delete/?proxy={}"



###################################################################






BOT_NAME = 'Scrapy_RedisSpider'

SPIDER_MODULES = ['Scrapy_RedisSpider.spiders']
NEWSPIDER_MODULE = 'Scrapy_RedisSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy_RedisSpider (+http://www.yourdomain.com)'

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
DEFAULT_REQUEST_HEADERS = {
# 'Cookie':'UM_distinctid=16b07a5410188e-0370fbffdd06af-e353165-1fa400-16b07a54102adc; _uab_collina=155920140075412409340845; zg_did=%7B%22did%22%3A%20%2216b07a54a2ab69-020cbf4311ac2d-e353165-1fa400-16b07a54a2ba8a%22%7D; QCCSESSID=v0k6bn3k9kdo2m43o78k9pd201; acw_tc=2ff63b9615652582308674094e6d18b912a4b24b3a07d85f12fbfe420f; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1565258235,1565260494; CNZZDATA1254842228=1599181038-1559200185-%7C1565688721; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201565685400676%2C%22updated%22%3A%201565689890936%2C%22info%22%3A%201565258232518%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1565689892',
# 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}

#------------------设置true使用 middlewares 的cookies 有效
# COOKIES_ENABLED = True
COOKIES_ENABLED = False



# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'Scrapy_RedisSpider.middlewares.PpRedisspiderSpiderMiddleware': 543,
   # 'Scrapy_RedisSpider.middlewares.RandomProxyMiddleware': 100,
   # 'Scrapy_RedisSpider.middlewares.RandomUserAgent': 101,

}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'Scrapy_RedisSpider.middlewares.RandomUserAgent': 200,
   # 'Scrapy_RedisSpider.middlewares.CookieMiddleware': 201,
   'Scrapy_RedisSpider.middlewares.RandomProxyMiddleware': 202,
}


# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/



ITEM_PIPELINES = {
   'Scrapy_RedisSpider.pipelines.MongoPipeline': 501,
   'Scrapy_RedisSpider.pipelines.MysqlTwistedPipeline': 505,

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





#--------------todo   mysql配置
MYSQL_HOST           = MYSQL_SETTING['MYSQL_HOST']
MYSQL_DBNAME         = MYSQL_SETTING['MYSQL_DBNAME']                    #数据库名字，请修改
MYSQL_USER           = MYSQL_SETTING['MYSQL_USER']                          #数据库账号，请修改
MYSQL_PASSWORD       = MYSQL_SETTING['MYSQL_PASSWORD']         #数据库密码，请修改
MYSQL_PORT           = MYSQL_SETTING['MYSQL_PORT']                            #数据库端口
MYSQL_CHARSET        = MYSQL_SETTING['MYSQL_CHARSET']                           #数据库默认编码，别修改





#---------------------todo  mongo配置
MONGO_URI               =MONGO_SETTING['MONGO_URI']
MONGO_DATABASE          =MONGO_SETTING['MONGO_DATABASE']




#------------增加并发
# 默认 Item 并发数：100
CONCURRENT_ITEMS                    = 10
#
# # 默认 Request 并发数：16
CONCURRENT_REQUESTS                 = 10
#
# # 默认每个域名的并发数：8
CONCURRENT_REQUESTS_PER_DOMAIN      = 10
#
# # 每个IP的最大并发数：0表示忽略
CONCURRENT_REQUESTS_PER_IP          = 10

# #最大线程池
REACTOR_THREADPOOL_MAXSIZE          = 10


#最大并行请求数 ,待测试
# CONCURRENT_REQUESTS_PER_SPIDER =10


#可以开启dns cache来提高性能。在配置里面加上 ,待测试
# 自定义扩展，基于信号进行调用
# EXTENSIONS={'scrapy.contrib.resolver.CachingResolver': 0,}




#---------------todo redis
# 设置重启爬虫时是否清空爬取队列
# 这样每次重启爬虫都会清空指纹和请求队列,一般设置为False
# SCHEDULER_FLUSH_ON_START=True

#------------------清空dupefilter 队列
# SCHEDULER_FLUSH_ON_START = True


# 过滤器
DUPEFILTER_CLASS        = "scrapy_redis.dupefilter.RFPDupeFilter"

# # 调度器
SCHEDULER               = "scrapy_redis.scheduler.Scheduler"

# # 调度状态持久化设置为为True则不会清空redis里的dupefilter和requests队列
SCHEDULER_PERSIST       = True
# SCHEDULER_PERSIST       = False


# 请求调度使用优先队列
# SCHEDULER_QUEUE_CLASS   = 'scrapy_redis.queue.SpiderPriorityQueue'
#先进先出队列：
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#后进先出队列：
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

REDIS_HOST              = REDIS_SETTING['REDIS_HOST']
REDIS_PORT              = REDIS_SETTING['REDIS_PORT']

# REDIS_URL = 'redis://user:pass@hostname:9001'
REDIS_ENCODING          = 'utf-8'

# The item pipeline serializes and stores the items in this redis key.
REDIS_ITEMS_KEY         = '%(spider)s:items'

DOWNLOADER_CLIENTCONTEXTFACTORY = 'Scrapy_RedisSpider.context.CustomContextFactory'




#------------log
# 日志文件(文件名)
# LOG_FILE='scrapy_log.log'
# # 日志格式
# LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# # # 日志级别 CRITICAL, ERROR, WARNING, INFO, DEBUG
# LOG_LEVEL  = 'INFO'

# 如果等于True，所有的标准输出（包括错误）都会重定向到日志，例如：print('hello')
# LOG_STDOUT=True



#-------------------------------异常处理

#异常可被spider识别
HTTPERROR_ALLOWED_CODES = [405,404,300,301,302]

#禁止重试
# RETRY_ENABLED = False

# 减小下载超时:
DOWNLOAD_TIMEOUT = 15


#设置下载延迟(2或更高)
DOWNLOAD_DELAY =0

#-------禁止重定向
REDIRECT_ENALBED =False

#-------------------cookie 设置
# settings文件中给Cookies_enabled=False解注释
# settings的headers配置的cookie就可以用了
# COOKIES_ENABLED = False


'''
------------------------------------------------------ cookie 设置
# settings文件中给Cookies_enabled=False解注释
# settings的headers配置的cookie就可以用了
Cookies_enabled = False


yield scrapy.Request(url,dont_filter=True,cookies={自己的cookie})
修改process_request，添加request.cookies={}即可。
当COOKIES_ENABLED没有注释设置为False的时候scrapy默认使用了settings里面的cookie

当COOKIES_ENABLED设置为True的时候scrapy就会把settings的cookie关掉，使用自定义cookie

如果使用自定义cookie就把COOKIES_ENABLED设置为True

如果使用settings的cookie就把COOKIES_ENABLED设置为False
'''


#------------------------------------------账号密码基础配置---------------------------------------------------------------



























