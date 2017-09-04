import db_stocks_test as dbst
from datetime import datetime
from datetime import timedelta
import pandas as pd


def base(base_factor_name, stock_list, date, args):
    time_list = [date]
    dbst.get_base_factor_val(base_factor_name, time_list, stock_list)


def ma(base_factor_name, stock_list, date, args):
    dt = timedelta(days=args[0])
    time_list = [date - dt, date]
    df = dbst.get_base_factor_val(base_factor_name, time_list, stock_list)
    df = df.groupby('stock_id').mean()
    df = df.reset_index()
    return df


def ref(base_factor_name, stock_list, date, args):
    dt = timedelta(days=args[0])
    time_list = [date - dt]
    df = dbst.get_base_factor_val(base_factor_name, time_list, stock_list)
    return df


def test(base_factor_name, stock_list, date, args):
    return 'This is test:', base_factor_name, stock_list, date, args


__d_factor_method = {'MA': ma,
                     'REF': ref,
                     'CLOSE': base,
                     'test': test}


def apply_factor_method(method_name, base_factor_name, stock_list, date, args):
    df = __d_factor_method[method_name](base_factor_name, stock_list, date, args)
    return df

if __name__ == '__main__':
    apply_factor_method('test', 'over', 'HX', '2017-01-01', ['hah'])

