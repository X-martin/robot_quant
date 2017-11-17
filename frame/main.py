#!/usr/bin/python
#coding=utf-8

'''
策略框架

'''

import common.Constants as c
import common.BaseTools as bt
import common.BaseTools as cbt
import common.MysqlBasedata as MysqlBasedata
import returnSummary

from jinja2 import Environment, PackageLoader
import pandas as pd
env = Environment(loader=PackageLoader('frame', '.'))
import sys

import frame.my as my
reload(sys)
sys.setdefaultencoding('utf8')


import traceback


class loader(object):
    def __init__(self):
        pass

    def load(self, path):
        try:
            tmp = {}
            print  path
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
    #template = Template('Hello {{ name }}!')
    #print template.render(name='John Doe')
    # 股票池
    stocktype_list = ['300', '500', '50']
    # start_date_list = ['2016-1-1', '2017-1-1']
    # end_date_list = ['2017-1-1', '2017-8-1']
    stocklist = [('300', '2016-1-1', '2017-1-1'), ('500', '2017-1-1', '2017-8-1'), ('50', '2017-1-1', '2017-8-1')]
    # 买入条件
    # buycondition_list = [('fin', 'mv', 'asc','percent', 10), ('tec', 'ma', 1,5, 10)]
    stocklistStr = ''
    # 卖出条件
    sellcondition_list = None
    for index in range(len(stocklist)):
        i = index + 1
        stocktype = stocktype_list[index]
        stocklistStr += "    s"+str(i) + " = str(tbd.get_stocklist_by_type(tradedate, '"+stocktype+"'))\n"
    stocklistStr += "    s = \"(s1Ns2)Us3\"\n"
    buyConditionlist = ['asc5']
    sellConditionlist = ['gx', 'asc5']
    # 判断是否在这个时间段,如果是，调用查询股票池方法
    # stocklist1 = tbd.get_stocklist_by_type('', '000300.SH')

    template = env.get_template('mytemplate.html')
    codestr = template.render(periodType='D', changePeriod='20', startDateStr='2011-1-1', endDateStr='2017-1-1', initMoney='1000000', \
                              stockExpression='', stocklistStr=stocklistStr, baseVariableExpression=r'MA5 = MA(trade_closeprice,5)\nMA10 = MA(trade_closeprice, 10)', \
                              conditionVariableExpression=r'gx = CROSS(MA5, MA10)\nasc5 = SORT(MA5, asc, 5)' ,buyConditionlist=buyConditionlist, sellConditionlist=sellConditionlist)
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

def getSummary(benchCode, startDateStr, endDateStr):
    conn = cbt.getConnection()
    t = MysqlBasedata.MysqlBasedata()
    df_bench = t.get_history_index_data_by_date(benchCode, startDateStr, endDateStr, None)
    df_bench = df_bench.sort_values(by='tradedate', ascending=True)
    sql = "SELECT * from r_position where strategy_id='2' ORDER BY tradedate"
    df_position = pd.read_sql(sql, conn)
    rsumm = returnSummary.ReturnSummary(df_position, df_bench)
    summ = rsumm.get_summary()
    print summ
    # total asset data
    print rsumm.df_assets
    return rsumm, summ

'''
    periodType='D', changePeriod='20', startDateStr='2011-1-1', endDateStr='2017-1-1', initMoney='1000000',
    buyConditionlist = ['asc5']
    sellConditionlist = ['gx', 'asc5']
    (s1Ns2)Us3\"\n
    baseVariableExpression=r'MA5 = MA(trade_closeprice,5)\nMA10 = MA(trade_closeprice, 10)'
    conditionVariableExpression=r'gx = CROSS(MA5, MA10)\nasc5 = SORT(MA5, asc, 5)'
'''
def execute(periodType, changePeriod, startDateStr, endDateStr, initMoney, stocktype_list, stocklist, stockExpression,
            baseVariableExpression, conditionVariableExpression, buyConditionlist, sellConditionlist):
    benchCode = '000300.SH'
    stocklistStr = ''
    # 卖出条件
    sellcondition_list = None
    for index in range(len(stocklist)):
        i = index + 1
        stocktype = stocktype_list[index]
        stocklistStr += "    s"+str(i) + " = str(tbd.get_stocklist_by_type(tradedate, '"+stocktype+"'))\n"
    stocklistStr += "    s = \""+stockExpression+"\"\n"

    template = env.get_template('mytemplate.html')
    codestr = template.render(periodType=periodType, changePeriod=changePeriod, startDateStr=startDateStr, endDateStr=endDateStr, initMoney=initMoney, \
                              stockExpression='', stocklistStr=stocklistStr, baseVariableExpression=baseVariableExpression, \
                              conditionVariableExpression=conditionVariableExpression ,buyConditionlist=buyConditionlist, sellConditionlist=sellConditionlist)
    print codestr
    f = open('frame/my.py', 'w')
    f.write(codestr)
    f.close()
    load = loader()
    m = load.load("frame/my.py")
    func_init = m["init"]
    # 初始化
    func_init()
    conn = bt.getConnection()
    df = bt.getTradeDay(conn, start_date_str=c.startDateStr, end_date_str=c.endDateStr, type=1)
    # 按日期执行策略
    datelist = df['tradedate'].tolist()
    func = m["handle_data"]
    for d in datelist:
        func(d)

    summary = getSummary(benchCode, startDateStr, endDateStr)
    # print summary
    return summary

if __name__ == '__main__':
    #shutil.copyfile('D:\workspace\TestStrategy\common\BaseTools.py', 'D:\workspace\TestStrategy\common\BaseTools1.py')
    #execfile('D:\workspace\TestStrategy\common\BaseTools1.py')
    c.startDateStr='2010-1-1'
    c.endDateStr='2017-1-1'
    # run()
    # generateCode()
    #print my.getStockList()
    # print getSummary()
    periodType = 'D'
    changePeriod = '20'
    startDateStr = '2011-1-1'
    endDateStr = '2017-1-1'
    initMoney = '1000000'
    stocktype_list = ['300', '500', '50']
    stocklist = [('300', '2016-1-1', '2017-1-1'), ('500', '2017-1-1', '2017-8-1'), ('50', '2017-1-1', '2017-8-1')]
    stockExpression = "(s1Ns2)Us3"
    baseVariableExpression = r'MA5 = MA(trade_closeprice,5)\nMA10 = MA(trade_closeprice, 10)'
    conditionVariableExpression = r'gx = CROSS(MA5, MA10)\nasc5 = SORT(MA5, asc, 5)'
    buyConditionlist = ['asc5']
    sellConditionlist = ['gx', 'asc5']

    execute(periodType, changePeriod, startDateStr, endDateStr, initMoney, stocktype_list, stocklist, stockExpression,
            baseVariableExpression, conditionVariableExpression, buyConditionlist, sellConditionlist)