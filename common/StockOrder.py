#!/usr/bin/python
#coding=utf-8

'''
股票下单类

'''


class StockOrder(object):

    def __init__(self, strategyId, stockcode, tradedate, price, volume):
        self.strategyId = strategyId
        self.stockcode = stockcode
        self.tradedate = tradedate
        self.price = price
        self.volume = volume