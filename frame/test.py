import factor_filter as ff
import interp as intp
from datetime import datetime

if __name__ == '__main__':
    # ----user's input-------
    t1 = datetime.strptime('2017/08/03', '%Y/%m/%d')
    stock_list = ['600725.SZ', '600306.SZ', '600000.SH', '600004.SH', '600006.SH',
                  '600007.SH', '600008.SH', '600009.SH', '600010.SH', '600011.SH',
                  '600012.SH', '600015.SH', '600016.SH']
    factor_txt = 'MA5 = MA(trade_closeprice,5)\nMA10 = MA(trade_closeprice, 10)'
    filter_txt = 'gx = CROSS(MA5, MA10)\nasc5 = SORT(MA5, asc, 5)'

    # ----interp user's input----
    d1, d2 = intp.interp(factor_txt, filter_txt)

    # ----get daily stock list on day t1-----
    for key in d2.keys():
        # print key, d2[key].factor_list, d2[key].method
        stocks = d2[key].filter(stock_list, t1)
        print 'Stock list by applying filter', key, ':', stocks
