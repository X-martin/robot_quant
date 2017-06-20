#!/usr/bin/python
#coding=utf-8

'''
工具

'''

import datetime


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