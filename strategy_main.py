#!/usr/bin/python
#coding=utf-8


'''
策略入口

'''

import common.Constants as c

from flask import Flask, redirect, render_template, \
    request, url_for, session, jsonify

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'some_secret'
fileroot = app.config["FILE_ROOT"]
imageurl_prefix = app.config['IMAGEURL_PREFIX']
lineBreak = app.config['LINE_BREAK']

'''
选项界面
'''
@app.route('/quant_index')
def quant_index():
    return render_template('quant_form.html')

@app.route('/quant_post', methods=['POST', 'GET'])
def quant_post():
    # 策略参数
    startDate = request.form['startDate'];
    endDate = request.form['endDate'];
    interval = request.form['interval'];
    period = request.form['period'];
    initMoney = request.form['initMoney'];
    fee = request.form['fee'];
    print startDate
    print endDate
    print interval
    print period
    print initMoney
    print fee
    # 股票筛选条件
    constituentStockStr = request.form['constituentStockStr'];
    print constituentStockStr
    areaStr = request.form['areaStr'];
    conceptStr = request.form['conceptStr'];
    industryStr = request.form['industryStr'];
    print constituentStockStr
    print areaStr
    print conceptStr
    print industryStr
    # 票池表达式、变量表达式
    stockExpression = request.form['stockExpression'];
    variableExpression = request.form['variableExpression'];
    print stockExpression
    print variableExpression

    # 买入条件、卖出条件
    buyConditionStr = request.form['buyConditionStr'];
    buyFundPercentStr = request.form['buyFundPercentStr'];
    buyWeightTypeStr = request.form['buyWeightTypeStr'];
    sellConditionStr = request.form['sellConditionStr'];
    sellFundPercentStr = request.form['sellFundPercentStr'];
    print buyConditionStr
    print buyFundPercentStr
    print buyWeightTypeStr
    print sellConditionStr
    print sellFundPercentStr


    return render_template('quant_form.html')

'''
选项界面
'''
@app.route('/choice_index')
def choice_index():
    #return redirect(url_for('strategy_choice'))
    stocktype_list = ['hs300', 'zz500']
    start_date_list = ['2016-1-1', '2017-1-1']
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
    print formula
    formulastr = formula.split(lineBreak)
    print formulastr
    factorlist = []
    for f in formulastr:
        fArr = f.split(":=")
        if len(fArr) == 2:
            factorlist.append(fArr[0])
    # factorlist.append(formula)
    print factorlist
    print jsonify(result=factorlist)
    return jsonify(result=factorlist)


if __name__ == "__main__":
    app.debug = app.config["DEBUG"]
    app.run('192.168.1.104')
    #app.run()