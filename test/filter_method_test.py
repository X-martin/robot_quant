import pandas as pd
from datetime import datetime
from datetime import timedelta


def cross(factor_list, stock_list, date, args):
    dt = timedelta(days=1)
    df1 = factor_list[0].get_val(stock_list, date)
    df2 = factor_list[1].get_val(stock_list, date)
    df1_0 = factor_list[0].get_val(stock_list, date - dt)
    df2_0 = factor_list[1].get_val(stock_list, date - dt)
    id = (df1_0['val'] < df2_0['val']) & (df1['val'] > df2['val'])
    df1 = df1[id]
    return df1


def greater(factor_list, stock_list, date, args):
    nf = len(factor_list)
    if nf == 1:
        df = factor_list[0].get_val(stock_list, date)
        df = df[df['val'] > args[0]]
    else:
        df1 = factor_list[0].get_val(stock_list, date)
        df2 = factor_list[1].get_val(stock_list, date)
        df = df1[df1['val'] > df2['val']]
    return df


def sort(factor_list, stock_list, date, args):
    df = factor_list[0].get_val(stock_list, date)
    if args[0] == 'asc':
        df = df.sort_values(["val"], ascending=True)
        nn = args[1]
        if nn < 1:
            nn = int(len(df) * nn)
        df = df.iloc[:nn, :]
    else:
        df = df.sort_values(["val"], ascending=False)
        nn = args[1]
        if nn < 1:
            nn = int(len(df) * nn)
        df = df.iloc[:nn, :]
    return df


__d_filter_method = {'CROSS': cross,
                     'GREATER': greater,
                     'SORT': sort}


def apply_filter_method(method_name, factor_list, stock_list, date, args):
    df = __d_filter_method[method_name](factor_list, stock_list, date, args)
    return df

