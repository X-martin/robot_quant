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
import common.InitParam as InitParam
import common.StrategyTools as st

from jinja2 import Environment, PackageLoader
import pandas as pd
env = Environment(loader=PackageLoader('frame', '.'))
import sys
import os
import time

reload(sys)
sys.setdefaultencoding('utf8')


import traceback
import common.FormulaUtil as FormulaUtil


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
    load = loader()
    m = load.load("my.py_")
    #my.init()
    func_init = m["init"]
    func_init()
    conn = bt.getConnection()
    #print c.startDateStr
    #print c.endDateStr
    df = bt.getTradeDay(conn, start_date_str=c.startDateStr, end_date_str=c.endDateStr, type=1)
    print df
    # 按日期执行策略
    datelist = df['tradedate'].tolist()


    #load = loader()
    #m = load.load("my.py_")
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
    f = open('my.py_', 'w')
    f.write(codestr)
    f.close()
    load = loader()
    m = load.load("my.py_")
    print m
    c = m["getStockList"]
    print dir(m)
    func = c
    #c()
    # print c.getStockList()

def getSummary(strategyId, benchCode, startDateStr, endDateStr):
    conn = cbt.getConnection()
    t = MysqlBasedata.MysqlBasedata()
    df_bench = t.get_history_index_data_by_date(benchCode, startDateStr, endDateStr, None)
    df_bench = df_bench.sort_values(by='tradedate', ascending=True)
    #sql = "SELECT * from r_position where strategy_id='"+stategyId+"' and tradedate ORDER BY tradedate"
    #df_position = pd.read_sql(sql, conn)
    df_position = st.getPositionListByTradedate(strategyId, startDateStr, endDateStr, conn)
    rsumm = returnSummary.ReturnSummary(df_position, df_bench)
    summ = rsumm.get_summary()
    print summ
    # total asset data
    print rsumm.df_assets
    # rsumm.df_assets = rsumm.df_assets[rsumm.df_assets]
    rsumm.df_assets.to_csv('asserts_.csv', index=False, sep=',')
    print pd.read_csv('asserts_.csv')
    return rsumm, summ

'''
    periodType='D', changePeriod='20', startDateStr='2011-1-1', endDateStr='2017-1-1', initMoney='1000000',
    buyConditionlist = ['asc5']
    sellConditionlist = ['gx', 'asc5']
    (s1Ns2)Us3\"\n
    baseVariableExpression=r'MA5 = MA(trade_closeprice,5)\nMA10 = MA(trade_closeprice, 10)'
    conditionVariableExpression=r'gx = CROSS(MA5, MA10)\nasc5 = SORT(MA5, asc, 5)'
'''
def execute(strategyId, periodType, changePeriod, startDateStr, endDateStr, initMoney, stocktype_list, stocklist, stockExpression,
            baseVariableExpression, conditionVariableExpression, buyConditionlist, sellConditionlist):
    benchCode = '000300.SH'
    stocklistStr = ''
    keywordList = []
    for index in range(len(stocklist)):
        i = index + 1
        stocktype = stocktype_list[index]
        stocklistStr += "    s"+str(i) + " = tbd.get_stocklist_by_type(tradedate, '"+stocktype+"')\n"
        stocklistStr += "    str"+str(i) + " = \"\'\"+'\\',\\''.join(s"+str(i)+")+\"\'\"\n"
        # stocklistStr += "    str"+str(i) + " = str"+str(i) + ".replace('\'', '')\n"
        keywordList.append("str"+str(i))
    stocklistStr += "    stockExpression = \""+stockExpression+"\".replace('s', 'str')\n"
    stocklistStr += "    for str in "+str(keywordList)+":\n"
    stocklistStr += "        stockExpression = stockExpression.replace(str, '\"+'+str+'+\"\')\n"
    stocklistStr += "        print stockExpression\n"
    # stocklistStr += "    stockExpression = stockExpression.replace(str, '"+'\"+str+'+"'\")\n"
    # print stocklistStr
    '''
    str1 = "'"+'\',\''.join(s1)+"'"
    str2 = "'"+'\',\''.join(s2)+"'"
    str3 = "'"+'\',\''.join(s3)+"'"
    s = "(str1Nstr2)Ustr3"
    for str in ['str1', 'str2', 'str3']:
        s = s.replace(str, '"+'+str+'+"')
        print s
    stockExpression = stockExpression.replace('s', 'str') #"(str11Nstr22)Ustr33"
    for str in ['str11', 'str22', 'str33']:
        s = s.replace(str, '"+' + str + '+"')
        print s
    # stocklistStr += "    s = \""+stockExpression+"\"\n"
    '''

    template = env.get_template('mytemplate.html')
    codestr = template.render(stockExpression='', stocklistStr=stocklistStr, baseVariableExpression=baseVariableExpression, \
                              conditionVariableExpression=conditionVariableExpression ,buyConditionlist=buyConditionlist, sellConditionlist=sellConditionlist)
    # print codestr

    #filename = str(int(time.time()))+'.py'
    filename = "my_"+strategyId+".py"
    #os.mknod("test.txt")
    # print filename
    f = file(filename, 'w')
    f.write(codestr)
    f.close()

    load = loader()
    m = load.load(filename)
    conn = bt.getConnection()
    st.deleteByStrategyId(strategyId, conn)
    df = bt.getTradeDay(conn, start_date_str=startDateStr, end_date_str=endDateStr, type=1)
    # 按日期执行策略
    ip = InitParam.InitParam(strategyId, periodType, changePeriod, startDateStr, endDateStr, initMoney)

    datelist = df['tradedate'].tolist()
    func = m["handle_data"]
    for d in datelist:
        # print d
        # print ip
        func(d, ip)

    summary = getSummary(strategyId, benchCode, startDateStr, endDateStr)
    # print summary
    os.remove(filename)
    return summary

if __name__ == '__main__':
    #shutil.copyfile('D:\workspace\TestStrategy\common\BaseTools.py', 'D:\workspace\TestStrategy\common\BaseTools1.py')
    #execfile('D:\workspace\TestStrategy\common\BaseTools1.py')
    c.startDateStr='2010-1-1'
    c.endDateStr='2010-6-1'
    # run()
    #generateCode()
    #print my.getStockList()
    # print getSummary()
    periodType = 'D'
    changePeriod = 20
    startDateStr = '2011-1-1'
    endDateStr = '2011-6-1'
    initMoney = 1000000
    stocktype_list = ['300', '500', '50']
    stocklist = [('300', '2016-1-1', '2016-3-1'), ('500', '2017-1-1', '2017-8-1'), ('50', '2017-1-1', '2017-8-1')]
    stockExpression = "(s1Ns2)Us3"
    baseVariableExpression = r'MA5 = MA(trade_closeprice,5)\nMA10 = MA(trade_closeprice, 10)'
    conditionVariableExpression = r'gx = CROSS(MA5, MA10)\nasc5 = SORT(MA5, asc, 5)'
    buyConditionlist = ['asc5']
    sellConditionlist = ['gx', 'asc5']

    #execute('3', periodType, changePeriod, startDateStr, endDateStr, initMoney, stocktype_list, stocklist, stockExpression,
    #        baseVariableExpression, conditionVariableExpression, buyConditionlist, sellConditionlist)
    #everyStockCash = 10000
    #print everyStockCash / 5.6
    #print int(everyStockCash / (5.6 * 100))
    # print 'a,b,dccc,d'.split(",")
    '''
    s1 = ['000001.SZ', '000002.SZ', '000003.SZ']
    s2 = ['000003.SZ', '000004.SZ', '000005.SZ']
    s3 = ['000006.SZ', '000007.SZ', '000008.SZ']
    str1 = "'"+'\',\''.join(s1)+"'"
    str2 = "'"+'\',\''.join(s2)+"'"
    str3 = "'"+'\',\''.join(s3)+"'"
    s = "(str1Nstr2)Ustr3"
    for str in ['str1', 'str2', 'str3']:
        s = s.replace(str, '"+'+str+'+"')
        print s

    stockExpression = "s1Us2".replace('s', 'str')
    for str in ['str1', 'str2']:
        stockExpression = stockExpression.replace(str, '"+'+str+'+"')
        print stockExpression

    exec s
    sss = "FormulaUtil.l1_analysis(\""+s+"\")"
    exec sss
    s = eval(sss)
    print s
    sss = "print FormulaUtil.l1_analysis(\"(" + str1 + "N" + str2 + ")U"+str3+"\")"
    exec sss
    #print FormulaUtil.l1_analysis("('000001.SZ','000002.SZ','000003.SZ'U'000003.SZ','000004.SZ','000005.SZ')U'000006.SZ','000007.SZ','000008.SZ')"

    #print "    stockExpression = stockExpression.replace(str, '\"+'+str+'+\"\')\n"
    #s = s.replace(str, '"+' + str + '+"')'''
