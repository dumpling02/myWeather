# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sys
sys.path.append("D:\\anaconda3\\envs\\scrapy\\lib\\site-packages")

import pymysql


class ScrapyweatherPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline:

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        # print('***'*30)
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):

        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):

        self.db.close()

    def process_item(self, item, spider):

        update_sql = 'update my05.%s set %s = %s+1 where id = "%s"'

        self.cursor.execute(update_sql % ('hn', item['weather'][0], item['weather'][0], item['area_name']))
        self.cursor.execute(update_sql % ('hn', item['weather'][1], item['weather'][1], item['area_name']))

        self.db.commit()

        print('---------', item['area_name'], '存储完毕', '---------')

        return item
