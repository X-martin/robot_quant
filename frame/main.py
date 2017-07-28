#!/usr/bin/python
#coding=utf-8

'''
策略框架

'''

import common.Constants as c
import common.BaseTools as bt
import shutil

import user.strategy_diy as sd

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

    for d in range(len(datelist)):
        # print d
        sd.handle_data(datelist[d])

if __name__ == '__main__':
    #shutil.copyfile('D:\workspace\TestStrategy\common\BaseTools.py', 'D:\workspace\TestStrategy\common\BaseTools1.py')
    #execfile('D:\workspace\TestStrategy\common\BaseTools1.py')
    c.startDateStr='2016-1-1'
    c.endDateStr='2016-2-1'
    run()