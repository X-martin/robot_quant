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

'''
获取最近的季度日期
'''
def getLastestQuarterlistByDate(d):
    year = d.year
    month = d.month
    day = d.day
    # print year, month, day
    quarter=[]
    if month <= 12 and month > 9:
        quarter.append((year, 3))
        quarter.append((year, 2))
        quarter.append((year, 1))
    elif month <= 9 and month > 6:
        quarter.append((year, 2))
        quarter.append((year, 1))
        quarter.append((year-1, 4))
    elif month <= 6 and month > 3:
        quarter.append((year, 1))
        quarter.append((year-1, 4))
        quarter.append((year-2, 3))
    elif month <= 3 and month > 0:
        quarter.append((year-1, 4))
        quarter.append((year-1, 3))
        quarter.append((year-1, 2))
    return quarter

if __name__ == '__main__':
    print dateRange("2016-01-01", "2016-02-01")
    conn = getConnection()
    c = conn.cursor()
    sql = "select * from r_strategy"
    c.execute(sql)
    alldata = c.fetchall()
    print alldata

    print getLastestQuarterlistByDate(datetime.datetime.now())