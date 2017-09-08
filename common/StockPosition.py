#!/usr/bin/python
#coding=utf-8

'''
股票仓位类

'''


class StockPosition(object):

    def __init__(self, strategyId, stockcode, tradedate, current_price, price, volume):
        self.strategyId = strategyId
        self.stockcode = stockcode
        self.tradedate = tradedate
        self.current_price = current_price
        self.price = price
        self.volume = volume