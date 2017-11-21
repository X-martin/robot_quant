#!/usr/bin/env python
#  _*_ coding:utf-8 _*_

'''
初始化參數对象，用于记录每次回测策略的参数

'''

class InitParam(object):
    def __init__(self, strategyId, periodType, changePeriod, startDateStr, endDateStr, initMoney, tradeMoney=0, currentPeriod=1, orderList=None, positionList=None):
        self.strategyId = strategyId
        self.periodType = periodType
        self.changePeriod = changePeriod
        self.startDateStr = startDateStr
        self.endDateStr = endDateStr
        self.initMoney = initMoney
        self.tradeMoney = tradeMoney
        self.orderList = orderList
        self.positionList = positionList
        self.currentPeriod = currentPeriod


if __name__ == '__main__':
    ip = InitParam('1', 'D', 20, '2016-1-1', '2017-1-1', 1000000)
    print ip.strategyId
    print ip.periodType
    print ip.changePeriod
    print ip.startDateStr
    print ip.endDateStr
    print ip