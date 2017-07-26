#!/usr/bin/python
#coding=utf-8

'''
技术因子接口

'''

import TushareBasedata as TushareBasedata

class TechFactorService(object):
    '''
    ma　
    行情列:如：收盘价\最高价\最低价
    n1上穿n2，金叉
    n2上穿n1，死叉

    type : 1、金叉 2、死叉
    '''

    def ma(self, codelist, col, tradedate, n1, n2, type):
        stocklist = []
        tbd = TushareBasedata.TushareBasedata()
        # 通过tradedate\n1\n2计算出ｍａ用到的数据的开始日期和结束日期
        start_date_str = None
        end_date_str = None
        # 循环codelist,分别判断是否符合条件
        for code in codelist:
            print code
            # 获取单只股票的数据
            col_data = tbd.get_history_data_by_date(code, start_date_str, end_date_str, 'D', 'B')
            if col_data == None:
                continue
            # 取得过去五天的平均价格
            man1 = col_data['close'][-1 * n1:].mean()
            # 取得过去10天的平均价格
            man2 = col_data['close'][-1 * n2:].mean()

            if type == 1:
                if man1 > man2:
                    stocklist.append(code)
            elif type == 2:
                if man1 < man2:
                    stocklist.append(code)
        return stocklist