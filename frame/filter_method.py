import pandas as pd
from datetime import datetime
from datetime import timedelta


def cross(factor_list, stock_list, date, args):
    dt = timedelta(days=1)
    df1 = factor_list[0].get_val(stock_list, date)
    df2 = factor_list[1].get_val(stock_list, date)
    df1_0 = factor_list[0].get_val(stock_list, date - dt)
    df2_0 = factor_list[1].get_val(stock_list, date - dt)
    id = (df1_0['FACTOR_VALUE'] < df2_0['FACTOR_VALUE']) & (df1['FACTOR_VALUE'] > df2['FACTOR_VALUE'])
    df1 = df1[id]
    return df1


def greater(factor_list, stock_list, date, args):
    nf = len(factor_list)
    if nf == 1:
        df = factor_list[0].get_val(stock_list, date)
        df = df[df['FACTOR_VALUE'] > args[0]]
    else:
        df1 = factor_list[0].get_val(stock_list, date)
        df2 = factor_list[1].get_val(stock_list, date)
        df = df1[df1['FACTOR_VALUE'] > df2['FACTOR_VALUE']]
    return df


def sort(factor_list, stock_list, date, args):
    args = args[0]
    df = factor_list[0].get_val(stock_list, date)
    if args[0] == 'asc':
        df = df.sort_values(['FACTOR_VALUE'], ascending=True)
        nn = float(args[1])
        if nn < 1:
            nn = int(len(df) * nn)
        nn = int(nn)
        df = df.iloc[:nn, :]
    else:
        df = df.sort_values(['FACTOR_VALUE'], ascending=False)
        nn = float(args[1])
        if nn < 1:
            nn = int(len(df) * nn)
        nn = int(nn)
        df = df.iloc[:nn, :]
    return df


__d_filter_method = {'CROSS': cross,
                     'GREATER': greater,
                     'SORT': sort}


def apply_filter_method(method_name, factor_list, stock_list, date, args):
    df = __d_filter_method[method_name](factor_list, stock_list, date, args)
    return df

