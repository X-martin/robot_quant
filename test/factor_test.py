import factor_method_test as fmt
import pandas as pd
from datetime import datetime
from datetime import timedelta


class FactorT(object):
    def __init__(self, name, method=None):
        self.name = name
        self.method = method

    def get_val(self, stock_list, date):
        df_stocks = pd.DataFrame(stock_list, columns=["stock_id"])
        df = fmt.apply_factor_method(self.method[0], self.name, stock_list, date, self.method[1])
        df_stocks = pd.merge(df_stocks, df, how='left', left_on='stock_id', right_on='stock_id')
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
        if self.method[0] == 'asc':
            df = df.sort_values(["val"], ascending=True)
            nn = self.method[1]
            if nn < 1:
                nn = int(len(df) * nn)
            df = df.iloc[:nn, :]
        if self.method[0] == 'desc':
            df = df.sort_values(["val"], ascending=False)
            nn = self.method[1]
            if nn < 1:
                nn = int(len(df) * nn)
            df = df.iloc[:nn, :]
        return list(df['stock_id'])

    def double_filter(self, stock_list, date):
        df1 = self.factors[0].get_val(stock_list, date)
        df2 = self.factors[1].get_val(stock_list, date)
        if self.method[0] == 'cross_up':
            dt = timedelta(days=1)
            df1_0 = self.factors[0].get_val(stock_list, date - dt)
            df2_0 = self.factors[1].get_val(stock_list, date - dt)
            id = (df1_0['val'] < df2_0['val']) & (df1['val'] > df2['val'])
            df1 = df1[id]
        elif self.method[0] == 'cross_down':
            dt = timedelta(days=1)
            df1_0 = self.factors[0].get_val(stock_list, date - dt)
            df2_0 = self.factors[1].get_val(stock_list, date - dt)
            id = (df1_0['val'] > df2_0['val']) & (df1['val'] < df2['val'])
            df1 = df1[id]
        elif self.method[0] == 'greater_than':
            df1 = df1[df1['val'] > df2['val']]
        elif self.method[0] == 'less_than':
            df1 = df1[df1['val'] < df2['val']]
        return list(df1['stock_id'])

if __name__ == '__main__':
    d_factors = {}
    d_filters = {}

    # ----user's input-------
    t1 = datetime.strptime('2017/08/03', '%Y/%m/%d')
    stock_list = ['GOOG', 'C', 'IBM', 'F', 'AAPL', 'KO', 'LEN', 'MO', 'AMZN', 'FLS', 'APD']

    input_factors = ['ma5 is close 5 MA',
                     'ma10 is close 10 MA']

    input_filters = ['golden_cross is ma5 cross_up ma10',
                     'ma5gma10 is ma5 greater_than ma10']

    # ----create factors------
    for l in input_factors:
        l = l.split(' is ')
        factor_name = l[0]
        l_right = l[1].split()
        name = l_right[0]
        method = [l_right[2], [float(l_right[1])]]
        d_factors[factor_name] = FactorT(name, method)

    # ----create filters------
    for l in input_filters:
        l = l.split(' is ')
        filter_name = l[0]
        l_right = l[1].split()
        factors = []
        w_float = 0
        for w in l_right:
            try:
                w_float = float(w)
                l_right.remove(w)
            except:
                if w in d_factors.keys():
                    factors += [d_factors[w]]
                    l_right.remove(w)
        method = [l_right[0], w_float]
        d_filters[filter_name] = FilterT(factors, method)

    # ----get daily stock list-----
    for key in d_filters.keys():
        stocks = d_filters[key].filter(stock_list, t1)
        print key
        print stocks
