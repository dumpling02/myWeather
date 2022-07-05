# coding:utf-8
import re
import scrapy
import sys

sys.path.append("D:\\anaconda3\\envs\\pythonProject1\\Lib\\site-packages")
print(sys.path)

from pypinyin import Style
from pypinyin.core import Pinyin
from scrapyweather.items import ScrapyweatherItem


class AreasSpider(scrapy.Spider):
    name = 'areas'
    allowed_domains = ['www.weather.com.cn']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        inputarea = self.setwhere()
        self.start_urls = ['http://www.weather.com.cn/textFC/%s.shtml' % inputarea]

    def setwhere(self):
        where_str = input("输入你要查询天气的地区（华北、东北、华东、华中、华南、西北、西南）:")

        p = Pinyin()
        where_py = ''.join(p.lazy_pinyin(where_str, style=Style.FIRST_LETTER))

        return where_py

    def parse(self, response):

        page_text = response.text
        ex = '<td width=".*?" height=".*?">\n<a href="http://www.weather.com.cn/weather/(.*?)" target="_blank">(.*?)</a></td>'

        areas = re.findall(ex, page_text, re.S)
        areas = list(set(areas))

        for area in areas:
            item = ScrapyweatherItem()
            item['area_url'] = 'http://www.weather.com.cn/weather/' + area[0]
            item['area_name'] = area[1]

            yield scrapy.Request(url=item['area_url'], callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):

        item = response.meta['item']
        weather_list = response.xpath('/html/body/div[5]/div[1]/div[1]/div[2]/ul/li[1]/p[1]/@title').extract_first()

        a = weather_list.replace('小到', '')
        b = a.replace('中到', '')
        weather_list = b.replace('大到', '')

        weather_list = weather_list.split('转')
        if len(weather_list) == 1:
            weather_list.append(weather_list[0])

        item['weather'] = weather_list

        yield item  # yield item给pipelines
