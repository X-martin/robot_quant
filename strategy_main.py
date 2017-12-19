#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
策略入口

'''

import common.StrategyTools as st
import common.BaseTools as bt
import frame.main as frameM

from datetime import *
import json
import time
import pandas as pd
import traceback
from flask import Flask, redirect, render_template, \
    request, url_for, session, jsonify, Response
from functools import wraps

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'some_secret'
fileroot = app.config["FILE_ROOT"]
imageurl_prefix = app.config['IMAGEURL_PREFIX']
lineBreak = app.config['LINE_BREAK']

'''
选项界面
'''
@app.route('/')
def quant_index():
    return render_template('quant_form.html')

@app.route('/quant_post', methods=['POST', 'GET'])
def quant_post():
    print "start:",datetime.now()
    start = datetime.now()

    summaryList = []
    orderList = []
    positionList = []
    # accountList = []
    strategyId = None
    try:
        # 策略参数
        startDateStr = request.form['startDate']
        endDateStr = request.form['endDate']
        changePeriod = int(request.form['interval'])
        period = request.form['period']
        initMoney = float(request.form['initMoney'])
        fee = request.form['fee']
        print startDateStr
        print endDateStr
        print changePeriod
        print period
        print initMoney
        print fee
        # 股票筛选条件
        constituentStockStr = request.form['constituentStockStr'];
        print constituentStockStr
        areaStr = request.form['areaStr']
        conceptStr = request.form['conceptStr']
        industryStr = request.form['industryStr']
        print constituentStockStr
        print areaStr
        print conceptStr
        print industryStr
        # 票池表达式、变量表达式
        stockExpression = request.form['stockExpression']
        baseVariableExpression = request.form['baseVariableExpression']
        conditionVariableExpression = request.form['conditionVariableExpression']
        print stockExpression
        print baseVariableExpression
        print conditionVariableExpression
        formulastr = baseVariableExpression.split("\r\n")
        print formulastr
        factorlist = []
        baseVariableExpressionStr = ''
        for f in formulastr:
            baseVariableExpressionStr +=f+r"\n"
        baseVariableExpression = baseVariableExpressionStr[:-2]

        conditionVariableExpressionStr = ''
        formulastr = conditionVariableExpression.split("\r\n")
        print formulastr
        for f in formulastr:
            conditionVariableExpressionStr +=f+r"\n"
        conditionVariableExpression = conditionVariableExpressionStr[:-2]
        print baseVariableExpression
        print conditionVariableExpression

        # 买入条件、卖出条件
        buyConditionStr = request.form['buyConditionStr']
        buyFundPercentStr = request.form['buyFundPercentStr']
        buyWeightTypeStr = request.form['buyWeightTypeStr']
        sellConditionStr = request.form['sellConditionStr']
        sellFundPercentStr = request.form['sellFundPercentStr']
        print buyConditionStr
        print buyFundPercentStr
        print buyWeightTypeStr
        print sellConditionStr
        print sellFundPercentStr
        buyConditionlist = buyConditionStr.split(",")
        sellConditionlist = sellConditionStr.split(",")

        # todo 待完成
        periodType = 'D' # period
        #changePeriod = 20
        #startDateStr = '2011-1-1'
        #endDateStr = '2013-1-1'
        #initMoney = 1000000
        stocktype_list = constituentStockStr.split(",")
        stocklist = constituentStockStr.split(",")#[('300', '2010-1-1', '2012-1-1'), ('500', '2017-1-1', '2017-8-1'), ('50', '2017-1-1', '2017-8-1')]
        #stockExpression = "(s1Ns2)Us3"
        #baseVariableExpression = r'MA5 = MA(trade_closeprice,5)\nMA10 = MA(trade_closeprice, 10)'
        #conditionVariableExpression = r'gx = CROSS(MA5, MA10)\nasc5 = SORT(MA5, desc, 5)'
        #buyConditionlist = ['asc5']
        #sellConditionlist = ['gx', 'asc5']
        conn = bt.getConnection()
        # todo 获取最大的策略id，加1
        strategyId = str(st.getMaxStrategyId(conn) + 1)
        print "strategyId start:"+strategyId

        # todo 返回策略收益率结果，，策略曲线
        result = frameM.execute(strategyId, periodType, changePeriod, startDateStr, endDateStr, initMoney, stocktype_list,
                                stocklist, stockExpression,
                                baseVariableExpression, conditionVariableExpression, buyConditionlist,
                                sellConditionlist)

        summaryDf = result[1].T
        asserts = result[0].df_assets
        asserts['date_new'] = asserts['date'].map(lambda x: time.mktime(x.timetuple())*1000)
        assetsDf = asserts[['date_new', 'asset']]
        assetsDf.to_csv('asserts_'+strategyId+'.csv', index=False, sep=',')

        # 基准指数
        indexDf = st.getIndexListByTradedate('000300.SH', startDateStr, endDateStr, conn)
        indexDf['date_new'] = indexDf['TRADEDATE'].map(lambda x: time.mktime(x.timetuple()) * 1000)
        indexDf['CLOSEPRICE'] = indexDf['CLOSEPRICE'].map(lambda x: 3000/x*initMoney)
        indexDf = indexDf[['date_new', 'CLOSEPRICE']]
        indexDf.to_csv('baseline_'+strategyId+'.csv', index=False, sep=',')
        print indexDf

        conn = bt.getConnection()
        # 查询订单信息
        orderDf = st.getOrderList(strategyId, conn)
        # 查询仓位信息
        positionDf = st.getPositionListByStrategyId(strategyId, conn)
        # 查询资金信息
        # accountDf = st.getAccountListByStrategyId(strategyId, conn)
        summaryList = [tuple(x) for x in summaryDf.values]
        orderList = [tuple(x) for x in orderDf.values]
        positionList = [tuple(x) for x in positionDf.values]

        # accountList = [tuple(x) for x in accountDf.values]
    except Exception, e:
        traceback.print_exc()
    finish = datetime.now()
    print "耗时：" , finish - start

    return render_template('quant_result.html', orderList=orderList, positionList=positionList, summaryList=summaryList, strategyId=strategyId)

'''
jsonp修饰
'''
def support_jsonp(f):
    """Wraps JSONified output for JSONP"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args, **kwargs).data) + ')'
            return app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)

    return decorated_function

@app.route('/json_index', methods=['POST', 'GET'])
@support_jsonp
def json_index():
    conn = bt.getConnection()
    # print request
    print request.args.get('strategyId')
    print request.args.get('filename')
    strategyId = request.args.get('strategyId')
    filename = request.args.get('filename')
    assetsList = []
    if filename == 'current':
        assetsDf = pd.read_csv('asserts_' + strategyId + '.csv')
        assetsList = [list(x) for x in assetsDf.values]
    else:
        assetsDf = pd.read_csv('baseline_' + strategyId + '.csv')
        assetsList = [list(x) for x in assetsDf.values]
    #print st.getPositionListByStrategyId(strategyId, conn)
    #print assetsList
    return Response(json.dumps(assetsList), mimetype='application/json')


'''
选项界面
'''
@app.route('/choice_index')
def choice_index():
    #return redirect(url_for('strategy_choice'))
    stocktype_list = ['hs300', 'zz500']
    start_date_list = ['2016-1-1', '2017-1-1']
    #
    end_date_list = ['2017-1-1', '2017-8-1']
    stocklist = [('hs300', '2016-1-1', '2017-1-1'), ('zz500', '2017-1-1', '2017-8-1')]

    return render_template('strategy_choice.html')

'''
编码界面
'''
@app.route('/code_index', methods=['POST', 'GET'])
def code_index():
    return render_template('strategy_code.html')

'''
结果展示界面
'''
@app.route('/result_index', methods=['POST', 'GET'])
def result_index():
    return render_template('strategy_result.html')

@app.route('/getfactorlist')
def getfactorlist():
    formula = request.args.get('formula', 0, type=str)
    #print formula
    formulastr = formula.split(lineBreak)
    #print formulastr
    factorlist = []
    for f in formulastr:
        #print f
        fArr = f.split("=")
        if len(fArr) == 2:
            factorlist.append(fArr[0])
    # factorlist.append(formula)
    #print factorlist
    #print jsonify(result=factorlist)
    return jsonify(result=factorlist)


if __name__ == "__main__":
    app.debug = app.config["DEBUG"]
    app.run('localhost')
    #app.run()