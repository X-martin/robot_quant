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

买入、卖出

1）买入
   查询是否存在仓位
   如果不存在，新增仓位

   否则，更新仓位，增加仓位数量,修改价格
   （仓位价格*仓位数量+订单价格*订单数量）/（仓位数量+订单数量）
2）卖出
   查询是否存在仓位
   如果不存在，跳过
   否则，判断仓位数量是否与卖出的一样，
       如果仓位大于等于卖出数量，删除仓位
       否则，更新仓位，减去仓位数量,修改价格
       （仓位价格*仓位数量+订单价格*订单数量）/（仓位数量+订单数量）


    不是每天都会有订单，每天都要有仓位

    买入金额:

    卖出金额:
    当前价
    仓位均价
    仓位数量
    卖出数量

    如果当前价大于仓位均价,上涨

    87.88

    69.26-----------------64.63

    1000

    200

    总资产:774464.23
    可用资金:53189.53--------------70746

    卖出价为87.88--当前价

    卖出后重新计算成本价

    总资产:774316.55
    可用资金:70746.95

    当前市值:70096---52578

    平均成本:64.63----57.01

    现价:87.62

    800股

    成本:10元 1000
    涨到12元

    卖出200,成交价12

    账户多出12*200,成本

    12

    如果不降低成本，卖出时按当前价



    处理完订单，通过前一天
    记录一条每日可用资产，总资产--------------仓位信息
    1,000000,tradedate,1000000,1000000


    查询最新的仓位日期
    通过日期查询当前仓位


'''
def order(orderList, conn):
    orderListNew = []
    try:
        if len(orderList) == 0:
            return
        # 记录订单到数据库
        orderFirst = orderList[0]
        tradedate = orderFirst.tradedate
        tradedateStr = datetime.strftime(tradedate, '%Y-%m-%d')
        for order in orderList:
            v = (order.strategyId, order.stockcode, order.tradedate, order.price, order.volume)
            # print v
            orderListNew.append(v)
        orderToDb(orderListNew, conn)

        # 初始化返还金额  （卖出股票为正，买入股票为负）
        tradeMoney = 0

        lastAccountDateStr = getLastAccountDate(c.strategyId, conn)
        # 查询上一个交易日全部仓位
        lastPositionDf = getPositionList(c.strategyId, lastAccountDateStr, conn)
        positionDf = lastPositionDf.copy()
        # 更新仓位日期
        positionDf['TRADEDATE'] = tradedate
        # 获取仓位中的股票代码
        positionStocklist = positionDf.STOCKCODE.tolist()
        # 初始化待新增仓位、待更新的仓位、待删除的仓位
        positionInsertList = []
        positionUpdateList = []
        positionDeleteList = []
        positionList = [tuple(x) for x in positionDf.values]
        # 仓位查询
        positionMap = {}
        for p in positionList:
            key = p[0]+'_'+str(p[2])
            positionMap[key] = p

        # 遍历订单
        for order in orderList:
            key = order.strategyId+'_'+str(order.tradedate)
            if order.volume > 0: # 如果订单中的量大于0，该订单为买入
                tradeMoney = tradeMoney - order.price * order.volume
                if order.stockcode not in positionStocklist:
                    v = (order.strategyId, order.stockcode, order.tradedate, order.price, order.volume)
                    positionInsertList.append(v)
                else:
                    p = positionMap[key]
                    price = (p[3]*p[4]+order.price*order.volume) / (p[4]+order.volume)
                    u = (order.strategyId, order.stockcode, order.tradedate, price, order.volume)
                    positionUpdateList.append(u)
            elif order.volume < 0: # 如果订单中的量小于0，该订单为卖出
                if order.stockcode not in positionStocklist:
                    continue
                elif p.volume <= -1*order.volume:
                    p = positionMap[key]
                    d = (order.strategyId, order.stockcode, order.tradedate, p.price, p.volume)
                    positionDeleteList.append(d)
                else:
                    p = positionMap[key]
                    # 计算卖出后的成本价
                    # （仓位价*仓位数量-当前价*（仓位数量-卖出数量））/（仓位数量-卖出数量）
                    # （当前价*（仓位数量-卖出数量）-仓位价*仓位数量）/（仓位数量-卖出数量）
                    # 10元钱买入1000股，涨价20元钱，卖出500
                    # （（10*1000）-20*（1000-500）
                    # price = (p[3]*p[4]+order.price*order.volume) / (p[4]+order.volume)
                    v = (order.strategyId, order.stockcode, order.tradedate, order.price, order.volume)
                    positionUpdateList.append(v)
                tradeMoney = tradeMoney - order.price * order.volume
            elif order.volume == 0: # 如果订单中的量等于0，该订单为卖出全部
                p = positionMap[key]
                d = (order.strategyId, order.stockcode, order.tradedate, p.price, p.volume)
                positionDeleteList.append(d)
                # 如果订单的数量为0，全仓卖出，使用仓位数量，加钱
                tradeMoney = tradeMoney + order.price * p.volume

        # 新增
        for p in positionInsertList:
            key = p[0]+'_'+str(p[2])
            positionMap[key] = p

        # 修改
        for p in positionUpdateList:
            key = p[0]+'_'+str(p[2])
            positionMap[key] = p

        # 删除
        for p in positionDeleteList:
            key = p[0]+'_'+str(p[2])
            del positionMap[key]

        positionList = positionMap.values()

        savePosition(positionList, conn)

        # 更新全局返回金额
        c.tradeMoney = tradeMoney

        conn.commit()
    except Exception,e:
        traceback.print_exc()

'''

订单入库
'''
def orderToDb(orderlist, conn):
    cur = conn.cursor()
    cur.executemany(
            'insert into r_order(strategy_id, stockcode, tradedate, price, volume) values(%s, %s, %s, %s, %s)',
            orderlist)

'''
查询上一个交易日
'''
def getLastAccountDate(strategyId, conn):
    cur = conn.cursor()
    # 查询最大日期
    lastAccountDateSql = 'select max(tradedate) from r_position where strategy_id=' + strategyId
    cur.execute(lastAccountDateSql)
    lastAccountDate = cur.fetchone()
    if lastAccountDate[0] == None:
        return None
    lastAccountDateStr = datetime.strftime(lastAccountDate[0], '%Y-%m-%d')
    return lastAccountDateStr


'''
保存仓位信息
'''
def savePosition(positionList, conn):
    try:
        cur = conn.cursor()
        '''
        # 查询最大日期
        maxTradeDateSql = 'select max(tradedate) from r_position where strategy_id='+str(strategyId)
        cur.execute(maxTradeDateSql)
        maxTradeDate = cur.fetchone()
        maxTradeDateStr = datetime.strftime(maxTradeDate[0], '%Y-%m-%d')

        positionListSql = 'select * from r_position where strategy_id=%s and tradedate=DATE_FORMAT(\'%s\', \'%Y-%m-%d\')'
        cur.execute(positionListSql, (strategyId, maxTradeDateStr))
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
        '''


        cur.executemany(
            'insert into r_position(strategy_id, stockcode, tradedate, price, volume) values(%s, %s, %s, %s, %s)',
            positionList)

        conn.commit()
    except Exception,e:
        traceback.print_exc()

'''
保存账户资金
'''
def saveAccount(strategyId, tradedate, accountMoney, conn):
    cur = conn.cursor()
    p = (strategyId, '000000', tradedate, accountMoney, accountMoney)
    positionList = [p]
    cur.executemany(
        'insert into r_position(strategy_id, stockcode, tradedate, price, volume) values(%s, %s, %s, %s, %s)',
        positionList)


'''
TODO 更新仓位
1、通过昨日仓位、今日订单生成今日仓位
2、如果今日没有订单，复制昨日仓位
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

'''
获取账户信息
'''
def getAccountInfo(strategyId, tradedate, conn):
    sql = "select * from r_position where strategy_id="+str(strategyId) + " and stockcode='000000' and tradedate=DATE_FORMAT('"+tradedate+"', '%Y-%m-%d')"
    #print sql
    positionDf = pd.read_sql(sql, conn)
    return positionDf

'''
获取仓位列表
'''
def getPositionList(strategyId, tradedate, conn):
    sql = "select * from r_position where strategy_id="+str(strategyId)+" and stockcode!='000000' and tradedate=DATE_FORMAT('"+tradedate+"', '%Y-%m-%d')"
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
#getLastAccountDate(None, conn)
'''
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