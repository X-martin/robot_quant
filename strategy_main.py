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

'''
选项界面
'''
@app.route('/choice_index')
def choice_index():
    #return redirect(url_for('strategy_choice'))
    return render_template('strategy_choice.html')

'''
编码界面
'''
@app.route('/code_index', methods=['POST', 'GET'])
def code_index():
    pass

'''
结果展示界面
'''
@app.route('/result_index', methods=['POST', 'GET'])
def result_index():
    pass


if __name__ == "__main__":
    app.debug = app.config["DEBUG"]
    #app.run('192.168.1.104')
    app.run()