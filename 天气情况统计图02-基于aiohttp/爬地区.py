# coding=utf-8
import re
import requests
import time


# 爬各省份
from pypinyin import Style
from pypinyin.core import Pinyin


def getareas(where):
    start = time.time()

    url = 'http://www.weather.com.cn/textFC/%s.shtml' % where
    headersvalue = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.97 Safari/537.36',
    }
    r = requests.get(url=url, headers=headersvalue)
    print(r.encoding)
    page_text = r.text.encode('ISO-8859-1').decode('utf-8')

    # xpath爬不到，要用正则表达式
    # tree = etree.HTML('./areas/hn.html')
    # area_url = tree.xpath("/html/body/div[4]/div[2]/div/div/div[2]/div[1]/div[1]/table/tbody/tr[3]/td[2]/a/@target")

    ex = '<td width=".*?" height=".*?">\n<a href="http://www.weather.com.cn/weather/(.*?).shtml" target="_blank">(.*?)</a></td>'
    areas_url = re.findall(ex, page_text, re.S)
    # 去除重复项
    areas_url = list(set(areas_url))

    print(areas_url)
    print(len(areas_url))
    end = time.time()

    print('Cost time:', end - start)
    return areas_url


def setwhere():
    where_str = input("输入你要查询天气的地区（华北、东北、华东、华中、华南、西北、西南）:")

    # 实例化一共Pinyin对象，其实不要也可以
    p = Pinyin()
    # style=Style.FIRST_LETTER : 取首字母
    # ''.join([h,n]) : 用''连接列表(无缝连接)
    where_py = ''.join(p.lazy_pinyin(where_str, style=Style.FIRST_LETTER))
    # <class 'tuple'>
    return where_py, where_str

