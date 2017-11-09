#!/usr/bin/python
#coding=utf-8

'''
因子工具类

'''

# import common.TushareBasedata as TushareBasedata
import common.MysqlBasedata as MysqlBasedata
import common.BaseTools as bt

from datetime import datetime
import pandas as pd

'''
获取基本因子的值
'''
def get_basic_factor_val(factorname, date_list, stock_list):
    #t = TushareBasedata.TushareBasedata()
    #print factorname
    #print date_list
    #print stock_list
    t = MysqlBasedata.MysqlBasedata()
    if len(date_list) > 1:
        start_date_str = datetime.strftime(date_list[0], '%Y-%m-%d')
        end_date_str = datetime.strftime(date_list[1], '%Y-%m-%d')
        if factorname == 'trade_closeprice':
            factorDf = t.get_factor_data_by_datecode(stock_list, start_date_str, end_date_str, factorname, 0)
        else:
            factorDf = t.get_factor_data_by_datecode(stock_list, start_date_str, end_date_str, factorname, -1)
    else:
        start_date_str = datetime.strftime(date_list[0], '%Y-%m-%d')
        factorDf = t.get_factor_data_by_datecode(stock_list, start_date_str, start_date_str, factorname, -1)

    factorDf['FACTOR_VALUE'] = factorDf['FACTOR_VALUE'].map(lambda x: float(x))
    return factorDf

if __name__ == "__main__":
    startdate = datetime.strptime('2017-3-1', '%Y-%m-%d')
    enddate = datetime.strptime('2017-3-2', '%Y-%m-%d')
    #print get_basic_factor_val('trade_closeprice', [startdate, enddate], ['000001.SZ', '000002.SZ'])
    #print get_basic_factor_val('free_share_hold_num', [startdate], ['000001.SZ', '600306.SZ'])