#!/usr/bin/python
#coding=utf-8

'''
基础数据接口

'''
class Basedata(object):

    '''
    通过日期、股票列表、类型查询因子值列表

    tradedateStr：日期-字符串，格式：YYYY-MM-DD
    stocklist：股票列表
    type：因子类型
    conn
    '''
    def getFactorValueByTradedate(tradedateStr, stocklist, type, conn):
        pass