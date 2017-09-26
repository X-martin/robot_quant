#!/usr/bin/python
#coding=utf-8

'''
基础数据接口

'''
class Basedata(object):

    '''
        通过时间段行情数据接口
    '''
    def get_history_data_by_date(self, code, start_date_str, end_date_str, frequency, fq):
        pass

    '''
        通过股票列表查询行情数据接口
    '''
    def get_history_data_by_stocklist(self, trade_date, codelist, frequency, fq):
        pass

    '''
        通过时间段指数行情数据接口
    '''
    def get_history_index_data_by_date(self, code, start_date_str, end_date_str, frequency):
        pass

    '''
        通过指数代码列表查询指数行情数据接口
    '''
    def get_history_index_data_by_stocklist(self, trade_date, codelist, frequency):
        pass

    '''
        通过股票列表查询因子值数据
        tracetype:追溯期  0、半年 1、追溯到底 2、不追溯
    '''
    def get_factor_data_by_stocklist(self, trade_date, codelist, factorenname, tracetype):
        pass

    '''
        通过时间段因子值接口
    '''
    def get_factor_data_by_date(self, code, start_date_str, end_date_str, factorenname, tracetype):
        pass

    '''
        通过时间段因子值接口
    '''
    def get_factor_data_by_datecode(self, codelist, start_date_str, end_date_str, factorenname, tracetype):
        pass

    '''
        通过行业名称查询股票代码数据
    '''
    def get_stock_data_by_industryname(self, trade_date, industryname):
        pass

    '''
        通过概念名称查询股票代码数据
    '''
    def get_stock_data_by_conceptname(self, trade_date, conceptname):
        pass

    '''
        通过地域名称查询股票代码数据
    '''
    def get_stock_data_by_areaname(self, trade_date, areaname):
        pass

    '''
        通过日期、类型查询权重股；如：创业板、沪深300、中小板等
    '''
    def get_stocklist_by_type(self, trade_date, type):
        pass


