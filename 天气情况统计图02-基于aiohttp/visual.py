# coding=utf-8
import pymysql
from flask import Flask, render_template

from 异步爬取0529.爬地区 import setwhere

app = Flask(__name__)

where = setwhere()
where_py, where_str = where[0], where[1]
where_str = where_str + '地区天气情况'


@app.route("/")
def connect_html():
    mydb = pymysql.connect(host='localhost', user='root', password='111111', port=3306, db='my05')
    cursor = mydb.cursor()

    result_sql = 'select sum(晴),sum(多云),sum(阴),sum(小雨), sum(阵雨),sum(中雨) ,sum(雾), sum(雷阵雨), sum(大雨) from my05.%s' % where_py
    print(result_sql)
    cursor.execute(result_sql)
    row = cursor.fetchone()

    count = [int(r) for r in row]
    print(count)

    data = [
        {'value': count[0], 'name': '晴'},
        {'value': count[1], 'name': '多云'},
        {'value': count[2], 'name': '阴'},
        {'value': count[3], 'name': '小雨'},
        {'value': count[4], 'name': '阵雨'},
        {'value': count[5], 'name': '中雨'},
        {'value': count[6], 'name': '雾'},
        {'value': count[7], 'name': '大雨'},
        {'value': count[8], 'name': '雷阵雨'}
    ]
    return render_template("h0419.html", data1=data, where=where_str)


if __name__ == '__main__':
    app.run()
