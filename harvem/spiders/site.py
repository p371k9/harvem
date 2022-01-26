import scrapy
from .harv import HarvSpider

class SiteSpider(HarvSpider):
    name = 'site'    
    
    def __init__(self, url=None, *args, **kwargs):        
        if url == None:
            spider.crawler.engine.close_spider(self, reason='You should enter a URL!')
        else:
            self.start_urls = [url]  

