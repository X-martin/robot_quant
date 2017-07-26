#!/usr/bin/python
#coding=utf-8

'''
策略-diy

'''

import common.Constants as cc
import common.Basedata as cb
import common.BaseTools as cbt
import common.StrategyTools as cst
import common.TushareBasedata as TushareBasedata
import common.TechFactorService as TechFactorService

'''
## 初始化函数，设定要操作的股票、基准等等
'''
def init():
    # 周期类型 ：D、天 W、周 M、月
    cc.periodType = 'D'
    cc.changePeriod = 20
    cc.startDateStr='2016-4-1'
    cc.endDateStr='2017-4-1'
    cc.initMoney=1000000


## 股票筛选初始化函数
def getStockList():
    tbd = TushareBasedata.TushareBasedata()
    # 000016.SH：上证50   沪深300：000300.SH 创业板：399006.SZ 中证500：000905.SH
    stocklist1 = tbd.get_stocklist_by_type('', '000300.SH')
    stocklist2 = tbd.get_stocklist_by_type('', '000905.SH')

    '''
    industryDf = tbd.get_stock_data_by_industryname()
    conceptDf = tbd.get_stock_data_by_conceptname()
    areaDf = tbd.get_stock_data_by_areaname()
    '''
    return stocklist1+stocklist2

## 股票筛选排序初始化函数


## 出场初始化函数

## 入场初始化函数

## 风控初始化函数

## 卖出未卖出成功的股票

'''
风控
卖出股票......
'''
def riskcontrol():
    pass

## 股票筛选


## 交易函数
def trade(tradedate):
    '''
    调仓周期
    '''
    # 如果当前没有到调仓周期,跳过
    if cc.currentPeriod!=cc.changePeriod:
        cc.currentPeriod = cc.currentPeriod+1
        return
    cc.currentPeriod = 1
    # 获取票池
    stocklist = getStockList()
    if len(stocklist) == 0:
        return
    price = 0
    positionList = cc.positionList
    '''
    通过买入条件获取买入股票,取并集或者交集
    '''
    techFactor = TechFactorService.TechFactorService()
    # 传入股票池、收盘价标识、交易日期、5日、10日、金叉参数
    stocklist1 = techFactor.ma(stocklist, 'close', tradedate, 5, 10, 1)
    t = TushareBasedata()
    df = t.get_factor_data_by_stocklist(tradedate, stocklist, 'mv', 0)
    # 按因子排序，计算得到前10%的股票代码
    df = df.sort_values()
    stocklist2 = df.code.tolist()
    # 取并集
    stocklist = stocklist1+stocklist2

    '''
    调整仓位：卖出不在票池的股票
    '''
    # 卖出
    for position in positionList:
        code = position.code
        if code in stocklist:
            stocklist.remove(code)
            continue
        cst.order(tradedate, code, price, 0)

    '''
    调整仓位：买入符合条件的股票
    '''
    # 买入
    for code in stocklist:
        cst.order(tradedate, code, price, 100)


    '''
    风控条件
    '''

    # 增加仓位
    # 计算买入的成交价格 （股票仓位中的价格*股票仓位中的数量+股票现价*股票现在购买的数量）/（股票仓位中的数量 + 股票现在购买的数量）
    # 计算佣金、印花税等


    # 计算卖出的成交价（股票价格*100）
    # 如果有1000股，卖掉300股，价格从10元跌倒8元，（10*1000-8*300）/700；价格从10元涨到12元，（12*1000-10*1000）/（1000-300）
    # 计算佣金、印花税等
    # 买空后计算盈亏


##################################  选股函数群 ##################################

###################################  公用函数群 ##################################
## 排序
def check_stocks_sort(context, security_list, input_dick, ascending='desc'):
    pass


## 过滤同一标的继上次卖出N天不再买入
def filter_n_tradeday_not_buy(security, n=0):
    pass


## 是否可重复买入
def holded_filter(context, security_list):
    pass


## 卖出股票加入dict
def selled_security_list_dict(context, security_list):
    pass


## 过滤停股票
def paused_filter(context, security_list):
    return security_list


## 过滤退市股票
def delisted_filter(context, security_list):
    return security_list


## 过滤ST股票
def st_filter(context, security_list):
    return security_list


# 过滤涨停股票
def high_limit_filter(context, security_list):
    pass


'''
日交易
'''
def handle_data(d):
    print d
    trade(d)