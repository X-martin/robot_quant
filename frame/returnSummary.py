#!/usr/bin/python
#coding=utf-8

import pandas as pd
import numpy as np
from datetime import datetime
import sys

import common.BaseTools as cbt
reload(sys)
sys.setdefaultencoding('utf8')

class ReturnSummary(object):
    def __init__(self, df_position, df_bench):
        self.df_position = df_position
        self.df_bench = df_bench

        self.dates = []
        self.df_assets = 0
        self.df_returns = 0
        self.df_bench_returns = 0
        self.retrn = 0
        self.retrn_annual = 0
        self.retrn_bench = 0
        self.retrn_bench_annual = 0
        self.alpha = 0
        self.beta = 0
        self.sharpe = 0
        self.vol = 0
        self.vol_bench = 0
        self.win_daily = 0
        self.max_loss_daily = 0

    def sort_date(self):
        dates = list(set(self.df_position["tradedate"]))
        dates.sort()
        self.dates = dates

    def get_assets(self):
        df_assets = pd.DataFrame(columns=["date", "asset"])
        for date in self.dates:
            df_date = self.df_position.loc[self.df_position["tradedate"] == date]
            asset = float((df_date["current_price"].astype('float') * df_date["volume"].astype('float')).sum())
            # df_temp = pd.DataFrame([[date, asset]], columns=["date", "asset"])
            # df_assets = df_assets.append(df_temp, ignore_index=True)
            df_assets.loc[len(df_assets)] = [date, asset]
        self.df_assets = df_assets

    def get_returns(self, df_assets):
        df_returns = pd.DataFrame(columns=['date', 'return'])
        arr_returns = np.array(df_assets.iloc[:, 1])
        arr_returns = arr_returns[1:]/arr_returns[:-1] - 1
        arr_returns = np.insert(arr_returns, 0, 0)
        df_returns['date'] = list(df_assets.iloc[:, 0])
        df_returns["return"] = arr_returns
        return df_returns

    def summary(self):
        df_merge = self.df_returns.merge(self.df_bench_returns, how="inner", left_on='date',
                                         right_on='date')
        arr = np.array(df_merge.iloc[:, 1:])
        retrns = np.cumprod(arr,axis=0)
        mat_cov = np.cov(arr.transpose())
        vec_mean = arr.mean(axis=0)
        dates = list(set(df_merge["date"]))
        dates.sort()
        day0 = dates[0]
        day1 = dates[-1]
        print day0, day1
        difference = day1 - day0
        len_year = (difference.days + difference.seconds / 86400) / 365.2425
        print len_year

        self.vol = np.sqrt(mat_cov[0, 0])
        self.vol_bench = np.sqrt(mat_cov[1, 1])
        self.retrn = retrns[-1, 0] - 1
        self.retrn_bench = retrns[-1, 1] - 1
        self.retrn_annual = retrns[-1, 0]**(1.0/len_year) - 1
        self.retrn_bench_annual = retrns[-1, 1]**(1.0/len_year) - 1
        self.beta = mat_cov[0, 1]/mat_cov[1, 1]
        self.alpha = vec_mean[0] - vec_mean[1] * self.beta
        self.sharpe = self.alpha/np.sqrt(mat_cov[0, 0])
        self.win_daily = float((arr[:, 0]>arr[:, 1]).sum())/len(arr)
        self.max_loss_daily = max([0, arr[:, 0].min()])

    def get_summary(self):
        self.sort_date()
        self.get_assets()
        self.df_returns = self.get_returns(self.df_assets)
        self.df_bench_returns = self.get_returns(self.df_bench)
        self.summary()
        df_summary = pd.DataFrame(columns=['FieldName', 'FieldValue'])
        names = ["Strategy Return", "Strategy Ann Return", "Bench Return", "Bench Ann Return",
                 "Alpha", "Beta", "Sharpe", "Strategy Vol", "Bench Vol",
                 "Win(Daily)", "Max Loss(Daily)"]
        values = [self.retrn, self.retrn_annual, self.retrn_bench, self.retrn_bench_annual,
                  self.alpha, self.beta, self.sharpe, self. vol, self.vol_bench,
                  self.win_daily, self.max_loss_daily]
        df_summary['FieldName'] = names
        df_summary["FieldValue"] = values
        return df_summary

if __name__ == "__main__":
    # 连接池初始化
    # conn = cbt.getConnection()
    # sql = "SELECT * from r_position where strategy_id='2' ORDER BY tradedate"
    # df = pd.read_sql(sql, conn)
    # print df

    df_bench = pd.read_pickle('test_bench_returnSummary.pkl')
    df_position = pd.read_pickle('test_data_returnSummary.pkl')
    rsumm = ReturnSummary(df_position, df_bench)
    summ = rsumm.get_summary()
    print summ
