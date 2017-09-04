#!/usr/bin/python
#coding=utf-8

'''
因子工具类

'''

import common.TushareBasedata as TushareBasedata
import common.BaseTools as bt

from datetime import datetime
import pandas as pd

'''
获取基本因子的值
'''
def get_basic_factor_val(factorname, date_list, stock_list):
    t = TushareBasedata.TushareBasedata()
    factorDf = pd.DataFrame()
    conn = bt.getConnection()
    if len(date_list) > 1:
        start_date_str = datetime.strftime(date_list[0], '%Y-%m-%d')
        end_date_str = datetime.strftime(date_list[1], '%Y-%m-%d')
        datetimeDf = bt.getTradeDay(conn, start_date_str, end_date_str, type=1)
        # print datetimeDf
        datetimelist = datetimeDf.tradedate.tolist()
        for d in datetimelist:
            trade_date_str = datetime.strftime(d, '%Y-%m-%d')
            #for factorname in factorname_list:
            df = t.get_factor_data_by_stocklist(trade_date_str, stock_list, factorname, [1])

            # df['STOCKCODE']=df.index
            df['date'] = d
            df = df.reset_index(drop = True)
            #print df
            if len(factorDf)==0:
                factorDf = df
            else:
                factorDf = pd.concat([factorDf, df])

    return factorDf

if __name__ == "__main__":
    startdate = datetime.strptime('2017-3-1', '%Y-%m-%d')
    enddate = datetime.strptime('2017-3-2', '%Y-%m-%d')
    print get_basic_factor_val('roe', [startdate, enddate], ['600725.SZ', '600306.SZ'])