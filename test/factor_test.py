import db_stocks_test as dbst
import pandas as pd
from datetime import datetime
from datetime import timedelta


class FactorT(object):
    def __init__(self, name, method=None):
        self.name = name
        self.method = method

    def get_val(self, stock_list, date):
        df_stocks = pd.DataFrame(stock_list, columns=["stock_id"])

        if self.method is None:
            time_list = [date]
            df_temp = dbst.get_base_factor_val(self.name, time_list, stock_list)
        elif self.method[0] == 'MA':
            dt = timedelta(days=self.method[1])
            time_list = [date - dt, date]
            df_temp = dbst.get_base_factor_val(self.name, time_list, stock_list)
            df_temp = df_temp.groupby('stock_id').mean()
            df_temp = df_temp.reset_index()
        elif self.method[0] == 'Lag':
            dt = timedelta(days=self.method[1])
            time_list = [date - dt]
            df_temp = dbst.get_base_factor_val(self.name, time_list, stock_list)
        else:
            df_temp = pd.DataFrame([stock_list], columns=["stock_id"])
            df_temp['val'] = [float('nan')] * len(stock_list)

        df_stocks = pd.merge(df_stocks, df_temp, how='left', left_on='stock_id', right_on='stock_id')
        return df_stocks


class FilterT(object):
    def __init__(self, factors, method):
        self.factors = factors
        self.method = method

    def filter(self, stock_list, date):
        if len(self.factors) == 1:
            return self.single_filter(stock_list, date)
        else:
            return self.double_filter(stock_list, date)

    def single_filter(self, stock_list, date):
        df = self.factors[0].get_val(stock_list, date)
        return df['stock_id']

    def double_filter(self, stock_list, date):
        df1 = self.factors[0].get_val(stock_list, date)
        df2 = self.factors[0].get_val(stock_list, date)

if __name__=='__main__':
    name = 'close'
    ma5 = FactorT(name, ['MA', 5])
    ma10 = FactorT(name, ['MA', 10])

    t1 = datetime.strptime('2017/08/23', '%Y/%m/%d')
    stock_list = ['GOOG', 'C', 'IBM', 'F', 'AAPL', 'KO', 'LEN', 'MO', 'AMZN', 'FLS', 'APD']
    dfma5 = ma5.get_val(stock_list, t1)
    dfma10 = ma10.get_val(stock_list, t1)
    print dfma5
    print dfma10