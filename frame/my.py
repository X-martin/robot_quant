#!/usr/bin/python
#coding=utf-8

'''
策略-diy

'''

import common.Constants as cc
import common.BaseTools as cbt
import common.StrategyTools as cst
import common.MysqlBasedata as MysqlBasedata
import common.StockOrder as StockOrder
import common.FormulaUtil as FormulaUtil

import frame.interp as intp

from datetime import datetime

'''
## 初始化函数，设定要操作的股票、基准等等
'''
def init():
    # 周期类型 ：D、天 W、周 M、月
    cc.periodType = 'D'
    cc.changePeriod = 20
    cc.startDateStr='2010-1-1'
    cc.endDateStr='2012-1-1'
    cc.initMoney=1000000


## 股票筛选初始化函数
def getStockList(tradedate):
    tbd = MysqlBasedata.MysqlBasedata()
    s1 = str(tbd.get_stocklist_by_type(tradedate, '300'))
    s2 = str(tbd.get_stocklist_by_type(tradedate, '500'))
    s3 = str(tbd.get_stocklist_by_type(tradedate, '50'))
    s = "(s1Ns2)Us3"

    return tbd.get_stocklist_by_type(tradedate, '300')


def tradeNew(tradedate):
    # 数据库操作类初始化
    t = MysqlBasedata.MysqlBasedata()
    # 连接池初始化
    conn = cbt.getConnection()
    # 日期格式转换
    trade_date_str = datetime.strftime(tradedate, '%Y-%m-%d')
    # 查询股票行情接口
    stockPriceDf = t.get_history_data_by_stocklist(trade_date_str, None, 'D', 'B')
    # 验证调仓日期：验证是否到达调仓日期
    # 如果当前不是到调仓日期，新增资金账户信息
    # 查询前一天是否存在仓位，如果存在，拷贝前一天仓位信息
    if cc.currentPeriod % cc.changePeriod != 1:
        # 如果是第一天，记录账户资金信息
        # todo 否则，判断是否
        # 拷贝前一天的仓位信息，更新仓位中的股票价格
        updatePosition(tradedate, stockPriceDf, conn)
        #updatePositionAccount(tradedate)
        cc.currentPeriod = cc.currentPeriod + 1
        return
    cc.currentPeriod = cc.currentPeriod + 1
    # 如果是调仓日期，进入策略逻辑
    # 获取票池
    stocklist = getStockList(tradedate)
    print stocklist
    # 如果股票池为0
    if len(stocklist) == 0:
        # 新增资金账户信息，拷贝前一天仓位信息
        updatePosition(tradedate, stockPriceDf, conn)
        return
    # 定义买入股票列表、卖出股票列表
    buystocklist = stocklist
    # 计算得出中间条件、筛选股票的条件
    factor_txt = 'MA5 = MA(trade_closeprice,5)\nMA10 = MA(trade_closeprice, 10)'
    filter_txt = 'gx = CROSS(MA5, MA10)\nasc5 = SORT(MA5, asc, 5)'
    d1, d2 = intp.interp(factor_txt, filter_txt)
    # 通过买入条件得出买入股票列表
    for key in ['asc5']:
        buystocklist = d2[key].filter(buystocklist, tradedate)
        # print 'Stock list by applying filter', key, ':', buystocklist
    # 当前订单列表
    currentOrderlist = []

    lastAccountDateStr = cst.getLastAccountDate(cc.strategyId, conn)
    positionList = []
    # 如果仓位交易日不为空，查询仓位信息，复制仓位信息到新的交易日
    if lastAccountDateStr != None:
        positionDf = cst.getPositionList(cc.strategyId, lastAccountDateStr, conn)
        positionList = positionDf.values

    # 通过卖出条件得出卖出股票列表,并将卖出股票列表放入订单
    for position in positionList:
        code = position[1]
        if code in buystocklist:
            buystocklist.remove(code)
            continue
        print code
        print stockPriceDf.loc[code, 'FACTOR_VALUE']
        o = StockOrder.StockOrder(cc.strategyId, code, tradedate, stockPriceDf.loc[code, 'FACTOR_VALUE'], 0)
        print o
        currentOrderlist.append(o)
    # 买入,并将买入股票列表放入订单
    for code in buystocklist:
        o = StockOrder.StockOrder(cc.strategyId, code, tradedate, stockPriceDf.loc[code, 'FACTOR_VALUE'], 100)
        currentOrderlist.append(o)
    print currentOrderlist
    # 订单入库，并更新仓位
    cst.order(currentOrderlist, stockPriceDf, conn)


'''
交易前
'''
def startTrade(d):
    pass


'''
交易后
1、初始化或记录当日资金账户信息
2、如果没有订单，查询最新的仓位交易日, 如果仓位交易日为空，初始化资金账户,
   如果仓位交易日不为空，查询仓位信息，复制仓位信息到新的交易日

'''
def endTrade(d):
    updatePositionAccount(d)

def updatePosition(tradedate, stockPriceDf, conn):
    lastAccountDateStr = cst.getLastAccountDate(cc.strategyId, conn)
    # 如果仓位交易日不为空，查询仓位信息，复制仓位信息到新的交易日
    if lastAccountDateStr != None:
        lastPositionDf = cst.getPositionList(cc.strategyId, lastAccountDateStr, conn)
        if len(lastPositionDf) > 0:
            positionDf = lastPositionDf.copy()
            # 更新仓位日期
            positionDf['TRADEDATE'] = tradedate
            positionList = [tuple(x) for x in positionDf.values]
            print positionList
            positionListNew = []
            # 更新当前实时价格
            for p in positionList:
                pNew = (p[0], p[1], tradedate, stockPriceDf.loc[p[1], 'FACTOR_VALUE'], p[4], p[5])
                positionListNew.append(pNew)
            cst.savePosition(positionListNew, conn)

def updatePositionAccount(tradedate):
    conn = cbt.getConnection()
    print cc.initMoney
    print cc.tradeMoney
    # 记录资金账户信息
    money = cc.initMoney + cc.tradeMoney
    cst.saveAccount(cc.strategyId, tradedate, money, conn)
    cc.tradeMoney=0
    cc.initMoney = money

'''
日交易
'''
def handle_data(d):
    print d
    startTrade(d)
    # trade(d)
    tradeNew(d)
    endTrade(d)