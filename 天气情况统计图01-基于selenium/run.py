# coding=utf-8
import pymysql
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

import os
import time

global condition_list

mydb = pymysql.connect(host='localhost', user='root', password='111111', port=3306, db='my0326')
cursor = mydb.cursor()


def get_werather(num):
    global condition_list

    # 无头模式
    option = ChromeOptions()
    option.add_argument('--headless')

    browser = webdriver.Chrome(options=option)
    browser.minimize_window()

    url = format('http://www.weather.com.cn/weathern/10128%02d01.shtml' % num)
    browser.get(url)

    condition = browser.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[1]/div/ul[2]/li[2]/p[1]').text

    condition_list = condition.split('转')

    print(condition_list[0])

    if len(condition_list) == 1:
        condition_list.append(condition_list[0])

    print(condition_list)
    browser.close()
    browser.quit()


# href="http://www.weather.com.cn/weather/101280101.shtml"
# href="http://www.weather.com.cn/weather/101280201.shtml"
def connect_db(area):

    area_id = format('%s' % area)
    sql = 'INSERT ignore INTO t0419 (id) values(%s)'  # 这里还不能加""了？ 有bug!!!

    print(sql % (area_id,))
    cursor.execute(sql, (area_id,))  # (x,)表示一个元素的元组

    update_sql = 'update t0419 set %s = %s+1 where id = "%s"'

    # update_sql1 = format(update_sql % (condition_list[0], condition_list[0], id))

    print(update_sql % (condition_list[0], condition_list[0], area_id))
    cursor.execute(update_sql % (condition_list[0], condition_list[0], area_id))
    mydb.commit()

    print(update_sql % (condition_list[1], condition_list[1], area_id))
    cursor.execute(update_sql % (condition_list[1], condition_list[1], area_id))
    mydb.commit()

    select_sql = 'select * from t0419 where id = "%s"'
    print(select_sql % area_id)
    cursor.execute(select_sql % area_id)

    row = cursor.fetchone()
    while row:
        print('Row:', row)
        print(type(row))
        row = cursor.fetchone()

    mydb.commit()


if __name__ == '__main__':
    area_list = ['广州', '韶关', '惠州', '梅州', '汕头', '深圳', '珠海', '佛山', '肇庆', '湛江', '江门', '河源', '清远', '云浮', '潮州', '东莞', '中山',
                 '阳江', '揭阳', '茂名', '汕尾']
    while True:

        for i in range(1, 22):
            get_werather(i)
            connect_db(area_list[i - 1])
        os.system("to be continue...")
        time.sleep(86400)  # 每隔1天运行一次 24*60*60=86400s
