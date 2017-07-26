#!/usr/bin/python
#coding=utf-8

'''
回测接口

'''

import common.Constants as c
import common.BaseTools as bt
import StockOrder as StockOrder
import StockPosition as StockPosition

import pandas as pd
import BaseTools as bt
from datetime import datetime
from datetime import timedelta
import traceback

'''
下订单
佣金、手续费、印花税等

'''
def order(orderList):
    orderListNew = []
    try:
        for order in orderList:
            # print order
            v = (order.strategyId, order.stockcode, order.tradedate, order.price, order.volume)
            # print v
            orderListNew.append(v)

        conn = bt.getConnection()
        cur = conn.cursor()
        cur.executemany(
            'insert into r_order(strategy_id, stockcode, tradedate, price, volume) values(%s, %s, %s, %s, %s)',
            orderListNew)
        conn.commit()
    except Exception,e:
        traceback.print_exc()

'''
保存仓位信息
'''
def savePosition(strategyId, orderList):
    try:
        conn = bt.getConnection()
        cur = conn.cursor()
        # 查询最大日期
        maxTradeDateSql = 'select max(tradedate) from r_position where strategy_id='+str(strategyId)
        cur.execute(maxTradeDateSql)
        maxTradeDate = cur.fetchone()

        positionListSql = 'select * from r_position where  strategy_id=%s and tradedate=%s'
        cur.execute(positionListSql, (strategyId, maxTradeDate[0]))
        positionList = cur.fetchall()
        print positionList
        positionMap = {}
        for p in positionList:
            positionMap[p[1]] = p

        positionList = []
        delPositionIds=[]
        for order in orderList:
            p = StockPosition.StockPosition(order.strategyId, order.stockcode, order.tradedate, order.price, order.volume)
            v = (order.strategyId, order.stockcode, order.tradedate, order.price, order.volume)
            positionList.append(v)
            p = positionMap[order.stockcode]
            if order.volume>0:
                order.volume=p[4]+order.volume
            elif order.volume==0:
                # 清空仓位
                pass
            elif order.volume<0:
                if p.volume>abs(order.volume):
                    order.volume=p.volume+order.volume
                elif p.volume<=abs(order.volume):
                    # 清空仓位
                    pass


        cur.executemany(
            'insert into r_position(strategy_id, stockcode, tradedate, price, volume) values(%s, %s, %s, %s, %s)',
            positionList)

        conn.commit()
    except Exception,e:
        traceback.print_exc()






'''
TODO 更新仓位
1、通过昨日仓位、今日订单生成今日仓位
2、如果今日没有订单，复制昨日仓位
'''
def updatePosition(positionList):
    positionListNew = []
    try:
        for position in positionList:
            # print order
            v = (position.strategyId, position.stockcode, position.tradedate, position.price, position.volume)
            # print v
            positionListNew.append(v)

        conn = bt.getConnection()
        cur = conn.cursor()
        cur.executemany(
            'insert into r_position(strategy_id, stockcode, tradedate, price, volume) values(%s, %s, %s, %s, %s)',
            positionListNew)
        conn.commit()
    except Exception,e:
        traceback.print_exc()


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
#print getPositionList(1, conn)
#print getOrderList(1, conn)

orderList = []
d = datetime.strptime('2017-4-8', '%Y-%m-%d')
o = StockOrder.StockOrder(1, '000001.SZ', d, 10.2, 100)
orderList.append(o)
#order(orderList)
positionList=[]
#p = StockPosition.StockPosition(4, '000001.SZ', d, 10.2, 100)
#positionList.append(p)
#updatePosition(positionList)

#savePosition(1, orderList)

'''
买入、卖出下单

1、查询当前仓位信息，接收卖出的股票列表（包括数量）
   1)查询仓位信息
   2）比较仓位和卖出列表，生成更新的sql

2、查询当前仓位信息，接收买入的股票列表
   1)查询当前仓位信息
   2)比较

'''