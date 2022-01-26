import scrapy
import csv
from .harv import HarvSpider
import scrapy_splash

#https://realpython.com/lessons/reading-csvs-pythons-csv-module/
class CsvSpider(HarvSpider):
    name = 'csv'
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
                yield scrapy_splash.SplashRequest(url=row["site"], callback=self.parse, endpoint='render.html', args={'wait': 2, 'images': 0, 'start_url': row["site"], "az": row["az"]})                

