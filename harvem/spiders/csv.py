from harvem.spiderclasses import NormalSpider, CsvClass

class CsvSplashSpider(CsvClass, NormalSpider):
    name = 'csv'

