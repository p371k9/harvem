import scrapy
import scrapy_splash
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
import re
from html import unescape
from harvem.items import hItem
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.shell import inspect_response
#from time import sleep

class HarvSpider(scrapy.Spider):
    name = 'harv'
    allowed_domains = []    #['localhost']
    #start_urls = ['http://www.hotelbenczur.hu', 'http://www.konyveles-miskolcon.hu/', 'https://www.anytimefitness.com']
    start_urls = ['http://www.hotelbenczur.hu']  # https://lakas-bgy.github.io/kapcsolat/  http://amiidonk.hu/bemutatkozas
    
    def start_requests(self):
        # https://github.com/scrapy/scrapy/blob/9dd77b42b5485856c7647c699c80532f5db2e5b6/scrapy/pipelines/files.py#L508
        for u in self.start_urls:
            #sleep(30)     
            yield scrapy_splash.SplashRequest(url=u, callback=self.parse, endpoint='render.html', args={'wait': 1, 'timeout': 60, 'images': 0, 'start_url': u, "az": hashlib.sha1(to_bytes(u)).hexdigest()})
        
    def getMails(self, response):
        source1 = unescape(response.text).replace('<em>', '')
        mails = re.findall(r'[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', source1)
        return list(set(mails)) #unique it. but... Csak a tiszta output miatt. Különben a DuplicatesPipeline önmagában is elvégzi amit kell
        
    def subParse(self, response):
        item = hItem()
        for m in self.getMails(response):
            item['az'] = response.meta['splash']['args']['az']
            item['site'] = response.meta['splash']['args']['start_url']
            item['mail'] = m
            yield item

    def parse(self, response):        
        for item in self.subParse(response):
            yield item

        domain = urlparse(response.url).netloc
        le = scrapy.linkextractors.LinkExtractor(allow=self.settings.get('LEA'), allow_domains=domain)
        
        #self.logger.info(le.extract_links(response))         
        #self.logger.info('Download_delay== %d',self.settings.get('DOWNLOAD_DELAY'))
        #inspect_response(response, self)         
        
        for l in le.extract_links(response):                                    
            yield scrapy_splash.SplashRequest(url=l.url, callback=self.subParse, endpoint='render.html', args={'wait': 1, 'timeout': 60, 'images': 0, 'start_url': response.meta['splash']['args']['start_url'], 'az': response.meta['splash']['args']['az']})            
