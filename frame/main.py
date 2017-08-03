#!/usr/bin/python
#coding=utf-8

'''
策略框架

'''

import common.Constants as c
import common.BaseTools as bt
import shutil

import user.strategy_diy as sd

from jinja2 import Template
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('frame', '.'))
import sys
import my
reload(sys)
sys.setdefaultencoding('utf8')


import traceback


class loader(object):
    def __init__(self):
        pass

    def load(self, path):
        try:
            tmp = {}
            exec open(path).read() in tmp
            return tmp
        except:
            print("Load module [path %s] error: %s"
                  % (path, traceback.format_exc()))
            return None
'''
执行

'''
def run():
    # 初始化
    sd.init()
    conn = bt.getConnection()
    df = bt.getTradeDay(conn, start_date_str=c.startDateStr, end_date_str=c.endDateStr, type=1)
    # 按日期执行策略
    datelist = bt.dateRange(c.startDateStr, c.endDateStr)
    datelist = df['tradedate'].tolist()

    load = loader()
    m = load.load("my.py")
    func = m["handle_data"]

    for d in range(len(datelist)):
        # print d
        #sd.handle_data(datelist[d])
        func(datelist[d])

def generateCode():
    stocklistStr = ''
    #template = Template('Hello {{ name }}!')
    #print template.render(name='John Doe')
    # 股票池
    stocktype_list = ['hs300', 'zz500']
    start_date_list = ['2016-1-1', '2017-1-1']
    end_date_list = ['2017-1-1', '2017-8-1']
    stocklist = [('hs300', '2016-1-1', '2017-1-1'), ('zz500', '2017-1-1', '2017-8-1')]
    # 买入条件
    buycondition_list = [('fin', 'mv', 'asc','percent', 10), ('tec', 'ma', 1,5, 10)]
    # 卖出条件
    sellcondition_list = None


    relationtype_list = [1, 1]
    for index in range(len(stocktype_list)):
        stocktype = stocktype_list[index]
        i = index+1
        stocklistStr += "    stocklist"+str(i)+" = tbd.get_stocklist_by_type(tradedate, '"+stocktype+"')\r\n"

    stocklistStr += "    return "
    for index in range(len(stocktype_list)):
        i = index+1
        stocklistStr += "stocklist"+str(i)
        if i != len(stocktype_list):
            stocklistStr += "+"
    print stocklistStr

    # 判断是否在这个时间段,如果是，调用查询股票池方法
    # stocklist1 = tbd.get_stocklist_by_type('', '000300.SH')

    # 生成买入股票代码
    buylistStr = ''
    for i in range(len(buycondition_list)):
        condition = buycondition_list[i]
        buylistStr = buylistStr + '    # condition-'+str(i)+'\n'
        if condition[0] == 'fin':
            buylistStr = buylistStr + '    df = t.get_factor_data_by_stocklist(trade_date_str, stocklist, \''+condition[1]+'\', 0)\n'
            if condition[2] == 'asc':
                buylistStr = buylistStr + '    df = df.sort_values(by=\'fv\', ascending=True)\n'
            elif condition[2] == 'desc':
                buylistStr = buylistStr + '    df = df.sort_values(by=\'fv\', ascending=False)\n'
            if condition[3] == 'percent':
                buylistStr = buylistStr + '    df = df.head(int(len(df) * '+str(condition[4])+' / 100))\n'
            elif condition[3] == 'num':
                buylistStr = buylistStr + '    df = df.head('+str(condition[4])+')\n'
        elif condition[0] == 'tec':
            if condition[1] == 'ma':
                buylistStr = buylistStr + '    stocklist'+str(i)+' = techFactor.ma(stocklist, \'close\', tradedate, '+str(condition[3])+', '+str(condition[4])+', '+str(condition[4])+')\n'

        buylistStr = buylistStr + '    stocklist'+str(i)+' = df.code.tolist()\r\n'

    buylistStr = buylistStr + '    # buy stocklist\n'
    buylistStr = buylistStr + '    stocklist = '
    for i in range(len(buycondition_list)):
        buylistStr = buylistStr + 'stocklist'+str(i)
        if i != len(buycondition_list)-1:
            buylistStr = buylistStr + '+'

    '''
    # 生成卖出股票代码
    selllistStr = ''
    for i in range(len(sellcondition_list)):
        condition = sellcondition_list[i]
    '''

    template = env.get_template('mytemplate.html')
    codestr = template.render(periodType='D', changePeriod='1', startDateStr='2016-1-1', endDateStr='2017-1-1', initMoney='1000000', buylistStr=buylistStr)
    print codestr
    f = open('my.py', 'w')
    f.write(codestr)
    f.close()
    load = loader()
    m = load.load("my.py")
    print m
    #c = m["getStockList"]
    #print dir(m)
    #func = c
    #c()
    #print c.getStockList()

if __name__ == '__main__':
    #shutil.copyfile('D:\workspace\TestStrategy\common\BaseTools.py', 'D:\workspace\TestStrategy\common\BaseTools1.py')
    #execfile('D:\workspace\TestStrategy\common\BaseTools1.py')
    c.startDateStr='2016-1-1'
    c.endDateStr='2016-2-1'
    #run()
    generateCode()
    #print my.getStockList()