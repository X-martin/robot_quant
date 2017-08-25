import pandas as pd
from datetime import datetime
from datetime import timedelta

_DB = pd.read_csv('db_stocks.txt', sep=',').iloc[:, 1:]
_DB['date'] = _DB['date'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d'))


def get_base_factor_val(factor_name, time_list, stock_list):
    df_s = pd.DataFrame(stock_list, columns=['stock_id'])
    df = _DB[['date', factor_name, 'stock_id']]
    if len(time_list) == 1:
        df = df[df['date'] == time_list[0]]
    else:
        df = df[(df['date'] >= time_list[0]) & (df['date'] <= time_list[1])]
    df = pd.merge(df_s, df, how='left', left_on='stock_id', right_on='stock_id')
    df = df[['stock_id', factor_name]]
    df.columns = [['stock_id', 'val']]
    return df

if __name__=='__main__':
    factor_name = 'close'
    stock_list = ['GOOG', 'C', 'IBM', 'F', 'AAPL', 'KO', 'LEN', 'MO', 'AMZN', 'FLS', 'APD']
    t0 = datetime.strptime('2017/08/17', '%Y/%m/%d')
    t1 = datetime.strptime('2017/08/23', '%Y/%m/%d')
    dt = timedelta(days=5)
    t2 = t1 - dt
    time_list = [t2, t1]
    df = get_base_factor_val(factor_name, time_list, stock_list)
    print df