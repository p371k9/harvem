import scrapy, scrapy_splash
from scrapy.utils.python import to_bytes
from scrapy.linkextractors import LinkExtractor
import csv, hashlib, re    
from urllib.parse import urlparse
from html import unescape
from .items import hItem
from abc import ABCMeta, abstractmethod
#from scrapy.shell import inspect_response

class AbstractSpider(scrapy.Spider, metaclass=ABCMeta):
    allowed_domains = []    #['localhost']
    #start_urls = ['http://www.hotelbenczur.hu', 'http://www.konyveles-miskolcon.hu/', 'https://www.anytimefitness.com']
    start_urls = ['http://www.hotelbenczur.hu']  # https://lakas-bgy.github.io/kapcsolat/  http://amiidonk.hu/bemutatkozas     
    def start_requests(self):
        # https://github.com/scrapy/scrapy/blob/9dd77b42b5485856c7647c699c80532f5db2e5b6/scrapy/pipelines/files.py#L508
        for u in self.start_urls:
            #sleep(30)     
            yield self.req(url=u, callback=self.parse, start_url=u, az=hashlib.sha1(to_bytes(u)).hexdigest())     

    @abstractmethod
    def req(self, url, callback, start_url, az):
        pass   
        
    @abstractmethod
    def getaz(self, response):
        pass
    
    @abstractmethod
    def getstarturl(self, response):
        pass
        
    def getMails(self, response):
        source1 = unescape(response.text).replace('<em>', '')
        mails = re.findall(r'[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', source1)
        return list(set(mails)) #unique it. but... Csak a tiszta output miatt. Különben a DuplicatesPipeline önmagában is elvégzi amit kell        
        
    def subParse(self, response):
        item = hItem()
        for m in self.getMails(response):
            item['az'] = self.getaz(response)
            item['site'] = self.getstarturl(response)
            item['mail'] = m
            yield item

    def parse(self, response): 
        for item in self.subParse(response):
            yield item

        domain = urlparse(response.url).netloc
        le = scrapy.linkextractors.LinkExtractor(allow=self.settings.get('LEA'), allow_domains=domain)
        #print(self.settings.get('LEA'))
        #inspect_response(response, self)         
        for l in le.extract_links(response):      
            yield self.req(url=l.url, callback=self.subParse, start_url=self.getstarturl(response), az=self.getaz(response))      
            
class NormalSpider(AbstractSpider):
    custom_settings = {}
    def getaz(self, response):
        return response.meta['az']
    
    def getstarturl(self, response):
        return response.meta['start_url']

    def req(self, url, callback, start_url, az):
        r = scrapy.Request(url=url, callback=callback, meta={'start_url': start_url, 'az': az})
        prox = self.settings.get('PROXY') # settings.py-ben nagybetűs, a meta-ban kicsi
        if type(prox) == str:            
            r.meta['proxy'] = prox
        return r
            
class SplashSpider(AbstractSpider):
    custom_settings = {
        'CONCURRENT_REQUESTS': 1, 
        'SPLASH_URL': 'http://0.0.0.0:8050',
        'DOWNLOADER_MIDDLEWARES': {
            'harvem.middlewares.JustDelayMiddleware': 543,
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage'
    }    # https://github.com/scrapy-plugins/scrapy-splash#configuration
    def getaz(self, response):
        return response.meta['splash']['args']['az']
    
    def getstarturl(self, response):
        return response.meta['splash']['args']['start_url']

    def req(self, url, callback, start_url, az):
        r = scrapy_splash.SplashRequest(url=url, callback=callback, endpoint='render.html', args={'wait': 1, 'timeout': 10, 'images': 0, 'start_url': start_url, 'az': az})
        prox = self.settings.get('PROXY')
        if type(prox) == str:
            r.meta['splash']['args']['proxy'] = prox
        return r
        
class Site:    
    def __init__(self, url=None, *args, **kwargs):        
        if url == None:
            spider.crawler.engine.close_spider(self, reason='You should enter a URL!')
        else:
            self.start_urls = [url]  
            
class List:            
    def __init__(self, file=None, *args, **kwargs):        
        if file == None:
            spider.crawler.engine.close_spider(self, reason='You should enter a list file name!')
        else:
            with open(file) as f:
                content = f.readlines()
            content = [x.strip() for x in content]
            self.start_urls = content                                    
            
#https://realpython.com/lessons/reading-csvs-pythons-csv-module/
class CsvClass:
    start_urls = []
    def __init__(self, file=None, *args, **kwargs):        
        if file == None:
            spider.crawler.engine.close_spider(self, reason='You should enter a csv file name!')
        else:
            self.file = file
   
    def start_requests(self):
        # https://github.com/scrapy/scrapy/blob/9dd77b42b5485856c7647c699c80532f5db2e5b6/scrapy/pipelines/files.py#L508
        with open(self.file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            #line_count = 0
            for row in csv_reader:
                yield self.req(url=row["site"], callback=self.parse, start_url=row["site"], az=row["az"])                
                          
