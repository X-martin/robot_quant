import factor_method as faMethod
import filter_method as fiMethod
import pandas as pd
from datetime import datetime
from datetime import timedelta


class FactorT(object):
    def __init__(self, bfname, method=None):
        self.bfname = bfname
        self.method = method

    def get_val(self, stock_list, date):
        df_stocks = pd.DataFrame(stock_list, columns=["stock_id"])
        df = faMethod.apply_factor_method(self.method[0], self.bfname, stock_list, date, self.method[1])
        df_stocks = pd.merge(df_stocks, df, how='left', left_on='stock_id', right_on='stock_id')
        return df_stocks


class FilterT(object):
    def __init__(self, factor_list, method):
        self.factor_list = factor_list
        self.method = method

    def filter(self, stock_list, date):
        df = fiMethod.apply_filter_method(self.method[0], self.factor_list, stock_list, date, self.method[1])
        return list(df['stock_id'])


if __name__ == '__main__':
    factor1 = FactorT('close', ['MA',[2]])
    factor2 = FactorT('close', ['MA', [3]])
    d_factors = {'ma5': factor1, 'ma10': factor2}

    filter1 = FilterT([factor1, factor2], ['CROSS', []])
    filter2 = FilterT([factor1], ['SORT', ['asc', 0.3]])
    d_filters = {'gx': filter1, 'asc5': filter2}

    # ----user's input-------
    t1 = datetime.strptime('2017/08/03', '%Y/%m/%d')
    stock_list = ['600725.SZ', '600306.SZ', '600000.SH', '600004.SH', '600006.SH',
                  '600007.SH', '600008.SH', '600009.SH', '600010.SH', '600011.SH',
                  '600012.SH', '600015.SH', '600016.SH']

    input_factors = ['ma5 is close 5 MA',
                     'ma10 is close 10 MA']

    input_filters = ['golden_cross is ma5 cross_up ma10',
                     'ma5gma10 is ma5 greater_than ma10']


    # ----get daily stock list-----
    for key in d_filters.keys():
        stocks = d_filters[key].filter(stock_list, t1)
        print key
        print stocks
