# -*- coding: utf-8 -*-



from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


#------------------todo 企查查
execute(['scrapy','crawl','QichachaSpider'])

'''
lpush QichachaSpider:QichachaSpiderQueue https://www.qichacha.com/search?key=河南龙佰智能装备制造有限公司                                
lpush QichachaSpider:QichachaSpiderQueue https://www.qichacha.com/search?key=淄博金刚贸易有限公司                                                                
lpush QichachaSpider:QichachaSpiderQueue https://m.qichacha.com/firm_d724b2adef662c73e5cdeb66a57ae399.html


分析：
    COOKIES_ENABLED 为False，启动setting里headers里面的参数，为True,启动Middleware里面的参数
    
    COOKIES_ENABLED = False 
    
    2.使用middleword 的proxy代理的时候会出现无法使用cookies的现象
    
    3.select other from ye_pinpai order by other desc limit 50;  找这里面的企业名字
    
    4.延迟10秒爬虫可爬50个左右，后面需要换cookies
    
    5.cookies设置后，用明文代理失败的问题

'''



#-------------------todo 好315加盟网
# execute(['scrapy','crawl','Hao315Spider'])

# lpush Hao315Spider:Hao315SpiderQueue http://jm.hao315.com/class/7_0_0_0_1.html


#---------------------todo  安心加盟网
# os.system('scrapy crawl BaiduCompanySpider')
# execute(['scrapy','crawl','AnxjmSpider'])




#---------------------todo  91加盟网
# os.system('scrapy crawl BaiduCompanySpider')
# execute(['scrapy','crawl','Jmw91Spider'])






#---------------------todo  百度企业爬虫
# os.system('scrapy crawl BaiduCompanySpider')
# execute(['scrapy','crawl','BaiduCompanySpider'])


'''
    lpush BaiduCompanySpider:BaiduCompanySpiderQueue https://xin.baidu.com/mark?q=%E9%B9%8F%E8%AE%AF&t=7

'''


#-----------------------todo  全球加盟网
#http://so.jiameng.com/bj/

# os.system('scrapy crawl JiamengSpider')
# execute(['scrapy','crawl','JiamengSpider'])


'''
lpush JiamengSpider:JiamengSpiderQueue http://so.jiameng.com/bj/


'''




#-------------todo 时尚品牌网
# os.system('scrapy crawl ChinassppSpider')






#------------------------maigoo
# execute(['scrapy','crawl','MaiGooSpider'])
# execute(['scrapy','crawl','QianjinReadisSpider_v2'])
# execute(['scrapy','shell',"https://www.qj.com.cn/so/"])
# execute(['scrapy','crawl','MaiGooSpiderV2'])
# execute(['scrapy','crawl','MaiGooSpiderV3'])
# os.system('scrapy crawl MaiGooSpiderV2')




'''

lpush MaiGooSpiderV2:RequestQueueV2 https://www.maigoo.com/brand/search/?catid=7 


lpush MaiGooSpiderV3:RequestQueueV3 https://www.maigoo.com/brand/search/?catid=7 


1.存在于mongo就从mongo里面取出来
2.scrapy 错误情况下的处理
3.将mongo中的数据带入到scrapy中以xpath进行处理

'''








