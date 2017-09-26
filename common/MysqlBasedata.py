#!/usr/bin/python
#coding=utf-8

import BaseTools as bt
from  Basedata import Basedata
import tushare as ts
from datetime import datetime
from datetime import timedelta
import os
import pandas as pd
import numpy as np
import traceback

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

'''
基础数据接口---Mysql数据


'''

class MysqlBasedata(Basedata):
    '''
        通过时间段行情数据接口
        frequency:D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
        fq:N、没有复权 B、后复权 F、前复权
    '''
    def get_history_data_by_date(self, code, start_date_str, end_date_str, frequency, fq):
        # todo 待完成
        pass

    '''
        通过股票列表查询行情数据接口
    '''
    def get_history_data_by_stocklist(self, trade_date_str, codelist, frequency, fq):
        # todo 待完成
        pass

    '''
        通过时间段指数行情数据接口
    '''
    def get_history_index_data_by_date(self, code, start_date_str, end_date_str, frequency):
        # todo 待完成
        pass

    '''
        通过指数代码列表查询指数行情数据接口

    '''
    def get_history_index_data_by_stocklist(self, trade_date_str, codelist, frequency):
        # todo 待完成
        pass

    '''
        通过股票列表查询因子值数据

        roe,净资产收益率(%)
    '''
    def get_factor_data_by_stocklist(self, trade_date_str, codelist, factorenname, tracetype):
        # todo 待完成
        pass
        conn = bt.getConnection()
        factorIdSql = "select factor_id from ST_FACTOR where factor_enname = '"+factorenname+"'"
        factorIdDf = pd.read_sql(factorIdSql, conn)

        factorIdList = factorIdDf.factor_id.tolist()
        print factorIdDf
        factorIdStr = ''
        for index in range(len(factorIdList)):
            id = factorIdList[index]
            factorIdStr += str(id)
            if index != len(factorIdList)-1:
                factorIdStr += ','


        # factorSql = "select * from st_factor where factor_id in ("+factorIdStr+") and "
        factorSql = "SELECT FACTOR_ID, STOCKCODE, FACTOR_DATE, FACTOR_VALUE, REPORT_DATE from ST_FACTOR_VALUE where " \
                    "factor_date>=str_to_date('"+trade_date_str+"', '%Y-%m-%d') \
                    and FACTOR_ID = "

        stockSql = ""
        stockDf = ___getStockDF___(conn)
        if codelist and len(codelist) > 0:
            # 获取股票代码Sql
            stockDf = stockDf[stockDf.STOCKCODE.isin(codelist)]
            if len(codelist) < 50:
                stockSql = ___getSecuritySql___(codelist)
        print stockDf
        print stockSql
        factorSql += stockSql
        factorDf = pd.read_sql(factorSql, conn)
        print factorDf


    '''
        通过时间段因子值接口
    '''
    def get_factor_data_by_date(self, code, start_date_str, end_date_str, factorenname, tracetype):
        # todo 待完成
        pass


        #
        factorSql = "SELECT FACTOR_ID, STOCKCODE, FACTOR_DATE, FACTOR_VALUE, REPORT_DATE from ST_FACTOR_VALUE where " \
                    "factor_date>=str_to_date('2017-5-04', '%Y-%m-%d') and factor_date<=str_to_date('2017-8-04', '%Y-%m-%d') \
                    and FACTOR_ID in (1,2,3,4,5,6,7,8)"

    '''
        通过时间段因子值接口
    '''
    def get_factor_data_by_datecode(self, codelist, start_date_str, end_date_str, factorenname, tracetype):
        startdate = None
        end_date = None
        start_date_str_new = None
        end_date_str_new = None

        factorDateSql = ""
        stockSql = ""
        factorId = ""
        conn = bt.getConnection()
        c = conn.cursor()
        factorIdSql = "select factor_id from ST_FACTOR where factor_enname = '" + factorenname + "'"
        c.execute(factorIdSql)
        factorIdResult = c.fetchone()
        factorId=factorIdResult[0]

        # 获取股票代码Sql
        if codelist and len(codelist) > 0 and len(codelist) < 50:
            stockSql = ___getSecuritySql___(codelist)
        print stockSql

        if tracetype == 0: # 不追溯
            if start_date_str!=None and end_date_str!=None:
                start_date_str_new = start_date_str
                end_date_str_new = end_date_str
                factorDateSql = "factor_date>=str_to_date('"+start_date_str_new+"', '%Y-%m-%d') and factor_date<=str_to_date('"+end_date_str_new+"', '%Y-%m-%d')"

            factorSql = "SELECT FACTOR_ID, STOCKCODE, FACTOR_DATE, FACTOR_VALUE, REPORT_DATE from ST_FACTOR_VALUE where " \
                         + factorDateSql + " and FACTOR_ID = "+str(factorId) + stockSql
            factorDf = pd.read_sql(factorSql, conn)
        elif tracetype == -1: # 追溯到底
            if start_date_str!=None and end_date_str!=None:
                start_date_str_new = start_date_str
                end_date_str_new = end_date_str
                factorDateSql = "factor_date>=str_to_date('"+start_date_str_new+"', '%Y-%m-%d') and factor_date<=str_to_date('"+end_date_str_new+"', '%Y-%m-%d')"
            #
            factorSql = "SELECT FACTOR_ID, STOCKCODE, FACTOR_DATE, FACTOR_VALUE, REPORT_DATE from ST_FACTOR_VALUE where " \
                        + factorDateSql + " and FACTOR_ID = " + str(factorId) + stockSql
            factorSql = factorSql + " union all " + " SELECT FACTOR_ID, STOCKCODE, FACTOR_DATE, FACTOR_VALUE, REPORT_DATE from (SELECT FACTOR_ID, STOCKCODE, FACTOR_DATE, FACTOR_VALUE, REPORT_DATE from ST_FACTOR_VALUE where \
                        FACTOR_ID = " + str(factorId) + stockSql+" order by FACTOR_DATE desc) new group by STOCKCODE, FACTOR_DATE"
            print factorSql
            factorDf = pd.read_sql(factorSql, conn)
        elif tracetype > 0: # 追溯某段时长
            if start_date_str!=None and end_date_str!=None:
                startdate = datetime.strptime(start_date_str, "%Y-%m-%d") + timedelta(days=-365*tracetype)
                start_date_str_new = startdate.strftime('%Y-%m-%d')
                end_date_str_new = end_date_str
                factorDateSql = "factor_date>=str_to_date('"+start_date_str_new+"', '%Y-%m-%d') and factor_date<=str_to_date('"+end_date_str_new+"', '%Y-%m-%d')"
            factorSql = "SELECT FACTOR_ID, STOCKCODE, FACTOR_DATE, FACTOR_VALUE, REPORT_DATE from ST_FACTOR_VALUE where " \
                        + factorDateSql + " and FACTOR_ID = " + str(factorId) + stockSql
            factorDf = pd.read_sql(factorSql, conn)
        # 过滤获取股票
        if codelist and len(codelist) >= 50:
            factorDf = factorDf[factorDf.STOCKCODE.isin(codelist)]
        return factorDf

    '''
        通过行业名称查询股票代码数据
    '''
    def get_stock_data_by_industryname(self, trade_date, industryname):
        # todo 待完成
        pass

    '''
        通过概念名称查询股票代码数据
    '''

    def get_stock_data_by_conceptname(self, trade_date, conceptname):
        # todo 待完成
        pass

    '''
        通过地域名称查询股票代码数据
    '''

    def get_stock_data_by_areaname(self, trade_date, areaname):
        # todo 待完成
        pass

    '''
        通过日期、类型查询权重股；如：创业板、沪深300、中小板等
        000016.SH：上证50   沪深300：000300.SH 创业板：399006.SZ 中证500：000905.SH
    '''

    def get_stocklist_by_type(self, trade_date, type):
        # todo 待完成
        pass



'''
获取股票代码列表
'''
def ___getStockDF___(conn):
    # 股票代码
    stockSql = "select DISTINCT STOCKCODE from ST_FACTOR_VALUE where STOCKCODE LIKE '0%' \
               OR STOCKCODE LIKE '6%' OR STOCKCODE LIKE '3%'"

    df = pd.read_sql(stockSql, conn)
    return df

'''
获取股票代码拼接的Sql
'''
def ___getSecuritySql___(security) :
    stockSql = ''
    if security and len(security)>0:
        stockSql += " AND STOCKCODE IN("
        for i in range(len(security)):
            if security[i].startswith("A"):continue
            stockSql+="'"
            stockSql+=security[i]
            stockSql+="'"
            if i!=len(security)-1:
                stockSql += ","
        stockSql += ")"
    return stockSql

t = MysqlBasedata()
# print t.get_factor_data_by_stocklist('2017-05-16', None, ['free_share_hold_num', 'trade_closeprice', 'trade_closeprice_after'], 0)
# print t.get_factor_data_by_stocklist('2017-05-16', ['000563.SZ', '002765.SZ', '002607.SZ'], ['free_share_hold_num', 'trade_closeprice', 'trade_closeprice_after'], 0)

# print t.get_factor_data_by_datecode(None, '1989-01-16', '2017-05-15', 'free_share_hold_num', 0)
print t.get_factor_data_by_datecode(None, '2017-01-16', '2017-05-15', 'free_share_hold_num', -1)