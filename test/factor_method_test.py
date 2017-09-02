import db_stocks_test as dbst
from datetime import datetime
from datetime import timedelta
import pandas as pd


def base(base_factor_name, stock_list, date):
    time_list = [date]
    dbst.get_base_factor_val(base_factor_name, time_list, stock_list)


def ma(base_factor_name, stock_list, date, n):
    dt = timedelta(days=n)
    time_list = [date - dt, date]
    df = dbst.get_base_factor_val(base_factor_name, time_list, stock_list)
    df = df.groupby('stock_id').mean()
    df = df.reset_index()
    return df


def ref(base_factor_name, stock_list, date, n):
    dt = timedelta(days=n)
    time_list = [date - dt]
    df = dbst.get_base_factor_val(base_factor_name, time_list, stock_list)
    return df

d = {'MA': ma,
     'REF': ref,
     'CLOSE': base}

