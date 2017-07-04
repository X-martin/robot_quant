#!/usr/bin/python
#coding=utf-8

'''
回测接口

'''

import common.Constants as c
import common.BaseTools as bt

import pandas as pd

'''
下订单


'''
def order(tradedate, stockcode, price, volume):
    v = (c.strategyId, stockcode, tradedate, price, volume)
    sql = "insert into r_order(strategy_id, stockcode, tradedate, price, volume) values(:1, :2, :3, :4, :5)"

    # TODO 更新仓位

'''
获取账户基本信息

'''
def getAccountInfo():
    pass

'''
获取仓位列表
'''
def getPositionList(strategyId, conn):
    sql = "select * from r_position where strategy_id="+str(strategyId)
    #print sql
    positionDf = pd.read_sql(sql, conn)
    return positionDf

'''
获取订单列表

'''
def getOrderList(strategyId, conn):
    sql = "select * from r_order where strategy_id="+str(strategyId)
    #print sql
    orderDf = pd.read_sql(sql, conn)
    return orderDf

conn = bt.getConnection()
print getPositionList(1, conn)
print getOrderList(1, conn)