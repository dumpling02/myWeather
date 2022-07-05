# coding=utf-8
import pymysql
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def connect_html():
    mydb = pymysql.connect(host='localhost', user='root', password='111111', port=3306, db='my0326')
    cursor = mydb.cursor()

    result_sql = 'select sum(晴),sum(多云),sum(阴),sum(小雨), sum(阵雨),sum(中雨) ,sum(雾), sum(雷阵雨), sum(大雨) from t0419'
    cursor.execute(result_sql)
    row = cursor.fetchone()

    # print('Row:', row)
    # print(type(row))
    # print(type(row[0]))
    # print(row[0])
    # print(int(row[0]))

    count = []
    for r in row:  # row是元组
        count.append(int(r))
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
    return render_template("h0419.html", data1=data)


if __name__ == '__main__':
    app.run()
