# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class HarvemPipeline:
    def process_item(self, item, spider):
        return item

from scrapy.exceptions import DropItem

class DuplicatesPipeline:

    def __init__(self):
        self.mails_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['mail'] in self.mails_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.mails_seen.add(adapter['mail'])
            return item           
