#!/usr/bin/python
#coding=utf-8

'''
策略框架

'''

import common.Constants as c
import common.BaseTools as bt

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
    my.init()
    conn = bt.getConnection()
    print c.startDateStr
    print c.endDateStr
    df = bt.getTradeDay(conn, start_date_str=c.startDateStr, end_date_str=c.endDateStr, type=1)
    print df
    # 按日期执行策略
    datelist = df['tradedate'].tolist()


    load = loader()
    m = load.load("my.py")
    func = m["handle_data"]

    for d in datelist:
        # print d
        #sd.handle_data(datelist[d])
        func(d)

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
    buylist = ['gx', 'asc5']
    selllist = ['gx', 'asc5']
    # 判断是否在这个时间段,如果是，调用查询股票池方法
    # stocklist1 = tbd.get_stocklist_by_type('', '000300.SH')

    template = env.get_template('mytemplate.html')
    codestr = template.render(periodType='D', changePeriod='1', startDateStr='2007-1-1', endDateStr='2017-1-1', initMoney='1000000', \
                              stockExpression='', baseVariableExpression=r'MA5 = MA(trade_closeprice,5)\nMA10 = MA(trade_closeprice, 10)', \
                              conditionVariableExpression=r'gx = CROSS(MA5, MA10)\nasc5 = SORT(MA5, asc, 5)' ,buylist=buylist, selllist=selllist)
    print codestr
    f = open('my.py', 'w')
    f.write(codestr)
    f.close()
    load = loader()
    m = load.load("my.py")
    print m
    c = m["getStockList"]
    print dir(m)
    func = c
    #c()
    # print c.getStockList()

if __name__ == '__main__':
    #shutil.copyfile('D:\workspace\TestStrategy\common\BaseTools.py', 'D:\workspace\TestStrategy\common\BaseTools1.py')
    #execfile('D:\workspace\TestStrategy\common\BaseTools1.py')
    c.startDateStr='2010-1-1'
    c.endDateStr='2017-1-1'
    run()
    #generateCode()
    #print my.getStockList()