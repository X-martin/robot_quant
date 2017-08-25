#!/usr/bin/python
#coding=utf-8

'''
因子工具类

'''

import common.TushareBasedata as TushareBasedata

'''
获取基本因子的值
'''
def get_basic_factor_val(factor_name, time, stock_list):
    t = TushareBasedata()
    trade_date_str = time
    df = None
    if len(time) == 1:
        df = t.get_factor_data_by_stocklist(trade_date_str, stock_list, factor_name, [1])
    elif len(time) == 2:
        start_date_str = time[0]
        end_date_str = time[1]
        df = t.get_factor_data_by_date(stock_list[0], start_date_str, end_date_str, factor_name, [1])
    return df