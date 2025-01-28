#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/18 下午7:08
# @Author  : 单子叶蚕豆_DzyCd
# @File    : method.py
# @IDE     : PyCharm

import datetime
import os
import subprocess
from flask import Flask, render_template

process_list = []
running_check = False

def execCmd(cmd):
    try:
        print("命令%s开始运行%s" % (cmd, datetime.datetime.now()))
        os.system(cmd)
        print("命令%s结束运行%s" % (cmd, datetime.datetime.now()))
    except:
        print('%s\t 运行失败' % cmd)


def execute_command_in_terminal(cmd):
    process_list.append(subprocess.Popen(f'start cmd /k {cmd}', shell=True))


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    with open(img_local_path, "rb") as f:
        img_stream = base64.b64encode(f.read())
    img_stream = str(img_stream).split("'")[1]
    return img_stream


def run_SaYi_Skaye():
    function_list = ['SaYi.py', 'Skaye.py']
    commands = ['python ' + i for i in function_list]

    for command in commands:
        execute_command_in_terminal(command)


def menu():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        if running_check:
            return
        commands = ['python SaYi_SV.py']
        for command in commands:
            execute_command_in_terminal(command)
        return render_template('main.html')

    @app.route("/SaYi_the_SV")
    def run():
        if running_check:
            return
        run_SaYi_Skaye()
        return render_template('SaYi_the_SV.html')

    app.run(host='0.0.0.0', port=5000, debug=True)


def SaYi_terminal(arg):
    global running_check
    running_check = arg
