#!/usr/bin/python
#coding=utf-8

from  Basedata import Basedata
import tushare as ts
from datetime import datetime
import os
import pandas as pd

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

'''
基础数据接口---Tushare数据

'''
class TushareBasedata(Basedata):

    '''
        通过时间段行情数据接口
    '''
    def get_history_data_by_date(self, code, start_date_str, end_date_str, frequency, fq):
        print 'tushare get_history_data_by_date start'
        if len(code) != 9:
            return None
        code = code[0:6]
        df1 = ts.get_hist_data(code,start=start_date_str,end=end_date_str, ktype=frequency)
        df1['tradedate']= df1.index
        df1 = df1.reset_index(drop=True)
        df1['date']=df1['tradedate'].map(lambda x:datetime.strptime(x, '%Y-%m-%d'))
        dfNew = df1.set_index('date')
        df = None
        if fq == 'N':
            df = ts.get_h_data(code, start=start_date_str, end=end_date_str, autype=None)
        elif fq == 'B':
            df = ts.get_h_data(code, start=start_date_str, end=end_date_str, autype='hfq')
        elif fq == 'F':
            df = ts.get_h_data(code, start=start_date_str, end=end_date_str)
        #df = df2.copy()
        df['pct_chg'] = dfNew['p_change']
        # del df['amount']
        #print df

        return df

    '''
        通过股票列表查询行情数据接口
    '''
    def get_history_data_by_stocklist(self, trade_date_str, codelist, frequency, fq):
        df = None
        dfChg = None

        for code in codelist:
            if len(code) != 9:
                continue
            code = code[0:6]
            if fq == 'N':
                df1 = ts.get_k_data(code, start=trade_date_str, end=trade_date_str, autype=None)
            elif fq == 'B':
                df1 = ts.get_k_data(code, start=trade_date_str, end=trade_date_str, autype='hfq')
            elif fq == 'F':
                df1 = ts.get_k_data(code, start=trade_date_str, end=trade_date_str)
            df = pd.concat([df, df1])
            df2 = ts.get_hist_data(code, start=trade_date_str, end=trade_date_str, ktype=frequency)
            dfChg = pd.concat([dfChg, df2])
        #print df
        #print dfChg
        df = df.reset_index(drop=True)
        dfChg = dfChg.reset_index(drop=True)
        df['pct_chg'] = dfChg['p_change']
        del df['date']
        return df

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
    '''
    def get_factor_data_by_stocklist(self, trade_date, codelist, tracetype):
        pass

    '''
        通过时间段因子值接口
    '''
    def get_factor_data_by_date(self, code, start_date_str, end_date_str, tracetype):
        pass

    '''
        通过行业名称查询股票代码数据
    '''
    def get_stock_data_by_industryname(self, trade_date, industryname):
        df = ts.get_industry_classified()
        df = df[df.c_name==industryname]
        del df['c_name']
        return df

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

t = TushareBasedata()
#df = t.get_history_data_by_date('000001.SZ', '2016-01-01', '2017-01-01', 'D', 'N')
#print df

#df2 = t.get_stock_data_by_industryname('2016-01-01', '综合行业'.decode("utf-8"))
#print df2

df3 = t.get_history_data_by_stocklist('2017-06-26', ['000001.SZ', '000002.SZ', '000003.SZ'], 'D', 'N')
print df3