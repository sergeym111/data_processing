# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient()
        self.mongo_base = client.vac

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            salary_processed = self.process_salary_hh(item['salary'])
            item['min_salary'] = salary_processed[0]
            item['max_salary'] = salary_processed[1]
            item['currency'] = salary_processed[2]
        elif spider.name == 'superjobru':
            salary_processed = self.process_salary_sj(item['salary'])
            item['min_salary'] = salary_processed[0]
            item['max_salary'] = salary_processed[0]
            
        del item['salary']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def process_salary_hh(self, salary):
        try:
            if salary[0] == 'от ' and salary[2] == ' до ':
                min = salary[1].replace(u'\xa0', u' ')
                max = salary[3].replace(u'\xa0', u' ')
                cur = 'не указана'
                return min, max, cur
            elif salary[0] == 'от ':
                min = salary[1].replace(u'\xa0', u' ')
                max = 'не указана'
                cur = 'не указана'
                return min, max, cur
            elif salary[0].strip() == 'до':
                min = 'не указана'
                max = salary[1].replace(u'\xa0', u' ')
                cur = 'не указана'
                return min, max, cur
            elif salary[0] == 'з/п не указана':
                min = 'не указана'
                max = 'не указана'
                cur = 'не указана'
                return min, max, cur
        except:
            return 'не указана', 'не не указана', 'не указана'

    def process_salary_sj(self, salary):
        try:
            if salary[0] == 'от':
                min = salary[2].replace(u'\xa0', u' ')
                return min, 'не указана'
            else:
                return 'не указана', 'не указана'
        except:
            return 'не указана', 'не указана'