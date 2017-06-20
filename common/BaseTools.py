#!/usr/bin/python
#coding=utf-8

'''
工具类

'''

import datetime
import MySQLdb

'''
获取mysql的链接
'''
def getConnection():
    conn = MySQLdb.connect(host='192.168.2.31', user='root', passwd='1qaz@WSX+!', db='strategy', port=3306)
    return conn

def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        print dt.weekday()
        date = dt.strftime("%Y-%m-%d")
    return dates

if __name__ == '__main__':
    print dateRange("2016-01-01", "2016-02-01")
    conn = getConnection()
    c = conn.cursor()
    sql = "select * from r_strategy"
    c.execute(sql)
    alldata = c.fetchall()
    print alldata