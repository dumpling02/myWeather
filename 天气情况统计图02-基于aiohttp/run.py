# coding=utf-8
import pymysql
from lxml import etree
import asyncio
import aiohttp
import aiomysql
import time
from 异步爬取0529.爬地区 import getareas, setwhere


# 异步请求
async def async_get(url):
    headersvalue = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.97 Safari/537.36',
    }
    session = aiohttp.ClientSession()
    response = await session.get(url=url, headers=headersvalue)
    r = await response.text()
    await session.close()
    return r


# 连接数据库
async def download_db(where01, area, condition_list):
    mydb = await aiomysql.connect(host='localhost', user='root', password='111111', port=3306, db='my05')
    cursor = await mydb.cursor()

    area_id = format('%s' % area)

    sql = 'INSERT ignore INTO my05.%s (id) values("%s")' % (where01, area_id)
    print(sql)
    await cursor.execute(sql)  # (x,)表示一个元素的元组

    # 向数据库插入数据
    update_sql = 'update my05.%s set %s = %s+1 where id = "%s"'
    await cursor.execute(update_sql % (where01, condition_list[0], condition_list[0], area_id))
    await cursor.execute(update_sql % (where01, condition_list[1], condition_list[1], area_id))

    await mydb.commit()
    print(area, '数据存储完毕')


# http://www.weather.com.cn/weathern/101050201.shtml
# 爬取area
async def spider(where02, area_id, area):
    # 各地区对应的url
    url = format('http://www.weather.com.cn/weathern/%s.shtml' % area_id)
    r = await async_get(url=url)

    # 数据解析，解析各地区天气
    html = etree.HTML(r)
    condition = html.xpath('/html/body/div[5]/div[3]/div[1]/div/ul[2]/li[2]/p[1]/text()')[0]

    # 数据解析后格式化处理数据
    condition_list = condition.split('转')
    if len(condition_list) == 1:
        condition_list.append(condition_list[0])

    print(area, '天气情况：', condition_list)
    print(area, '数据爬取完毕')

    await download_db(where02, area, condition_list)


if __name__ == '__main__':
    where = setwhere()[0]
    areas = getareas(where)

    # 降维打击
    areas_flatten = [col for row in areas for col in row]
    start = time.time()

    # 通过发现规律，匹配对应地区的数字url
    # 事件循环启动协程
    # task:存储协程任务的列表
    tasks = [asyncio.ensure_future(spider(where, areas_flatten[i], areas_flatten[i + 1])) for i in
             range(0, len(areas_flatten), 2)]
    print('------------------------------------------------', tasks, 'type:', type(tasks))
    loop = asyncio.get_event_loop()
    # 根据列表循环启动协程任务
    loop.run_until_complete(asyncio.wait(tasks))

    # 计算花费时间 56个请求！不超过2秒！
    end = time.time()
    print('Cost time:', end - start)

    # 定时爬取
    print("to be continued...")
    time.sleep(86400)  # 每隔1天运行一次 24*60*60=86400s
