#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/14 下午8:37
# @Author  : 单子叶蚕豆_DzyCd
# @File    : SaYi.py
# @IDE     : PyCharm
import socket
import datetime
import time
import os

# target_list: 名称，方位x， 方位y， 创建时间， 上次访问时间,确认标记（Y代表确认识别，X代表在识别队列中）
target_list = []
up_load_list = []
act_time = time.time()
counter = 0
SaYi_terminate = True


def tell_to_port(msg):
    port = 8080
    pos = "47.100.11.98"
    msg = f"SaYi_SV tell SaYi_998 send({msg}) {time.time()} 127.0.0.1+8080+none"
    socket_client = socket.socket()
    socket_client.connect((pos, port))
    socket_client.send(msg.encode("utf-8"))
    socket_client.close()


def load_clear():
    global up_load_list
    while len(up_load_list) > 10:
        del up_load_list[0]


def up_load(name):
    up_load_list.append(name)
    tell_to_port(name.replace(' ', '_'))


def print_load():
    if len(up_load_list) == 0:
        return None
    msg = ""
    p = 0
    for i in up_load_list:
        p += 1
        msg += f"\033[1;36m{i}\033[0m" + '\n'
        if p >= 10:
            break
    load_clear()
    return msg


def title():
    print("\033[0;35;40mSaYi_997 调度机器人 Version past.1\033[0m")
    print(
        '''
｀ＳＳＳ　　　　　　　　　　Ｙ　　　Ｙ　　　ｉ　　　　　　　　　　　　　　　　ＰＰＰＰ　　　　　　　　　　　　　　　　　　ｔ　　　　　　　　　１
Ｓ　　　Ｓ　　　　　　　　　Ｙ　　　Ｙ　　　　　　　　　　　　　　　　　　　　Ｐ　　　Ｐ　　　　　　　　　　　　　　　　　ｔ　　　　　　　　１１
Ｓ　　　Ｓ　　ａａａａ　　　Ｙ　　　Ｙ　　ｉｉ　　　　　　　　　　　　　　　　Ｐ　　　Ｐ　　ａａａａ　　　　ｓｓｓ　　　ｔｔｔｔ　　　　　　　１
　Ｓ　　　　　　　　　ａ　　　Ｙ　Ｙ　　　　ｉ　　　　　　　　　　　　　　　　Ｐ　　　Ｐ　　　　　　ａ　　ｓ　　　ｓ　　　ｔ　　　　　　　　　１
　　Ｓ　　　　　　　　ａ　　　Ｙ　Ｙ　　　　ｉ　　　　　　　　　　　　　　　　ＰＰＰＰ　　　　　　　ａ　　ｓ　　　　　　　ｔ　　　　　　　　　１
　　　Ｓ　　　　ａａａａ　　　　Ｙ　　　　　ｉ　　　　　　　　　　　　　　　　Ｐ　　　　　　　ａａａａ　　　ｓｓｓ　　　　ｔ　　　　　　　　　１
Ｓ　　　Ｓ　　ａ　　　ａ　　　　Ｙ　　　　　ｉ　　　　　　　　　　　　　　　　Ｐ　　　　　　ａ　　　ａ　　　　　　ｓ　　　ｔ　　　　　　　　　１
Ｓ　　　Ｓ　　ａ　　　ａ　　　　Ｙ　　　　　ｉ　　　　　　　　　　　　　　　　Ｐ　　　　　　ａ　　　ａ　　ｓ　　　ｓ　　　ｔ　　　　　．　　　１
　ＳＳＳ　　　　ａａａａ　　　　Ｙ　　　　ｉｉｉ　　　　　　　　　　　　　　　Ｐ　　　　　　　ａａａａ　　　ｓｓｓ　　　　　ｔｔ　　　．　　　１

　　　　　　　　　　　　　　　　　　　　　ｙｙ
    ''')
    print("time    :" + str(time.strftime('%Y-%m-%d %H:%M:%S')) + "\t运行时间   ：" + time.strftime('%H:%M:%S', time.localtime(time.time()+57600-act_time)))
    print("非none实例接收量   ：" + str(counter))
    print("-------------------------------------------------------------------------------")

def data_clear():
    for target in target_list:
        if time.time() - target[4] > 5:
            target[5] = 'D'
    target_list.sort(key=lambda x: x[5])
    while len(target_list) and target_list[0][5] == 'D':
        del target_list[0]


def data_process(name, x: float, y: float):
    for target in target_list:
        if target[0] == name and target[1]-0.06 <= x <= target[1]+0.06 and target[2]-0.06 <= y <= target[2]+0.06:
            target[1] = (target[1] + x) / 2
            target[2] = (target[2] + y) / 2
            target[4] = time.time()
            if time.time() - target[3] > 20 and  target[5] != 'Y':
                target[5] = 'Y'
                dateArray = datetime.datetime.fromtimestamp(target[4])
                # 格式化日期
                otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")

                up_load(f"{otherStyleTime}的时候检测到物体{target[0]} [{round(target[1],2)}, {round(target[2],2)}]")
            return
    target_list.append([name, x, y, time.time(), time.time(), 'X'])


start_time = time.time()
msg = "最近的十条检测结果：\n"


def data_show():
    global start_time, msg
    os.system('cls')
    title()
    print("待确认点位：")
    for target in target_list:
        if target[5] == 'X':
            print(f"\033[0;31;40m{target[0]} [{target[1]}, {target[2]}] 上次访问时间: {time.time() - target[4]} 持续时间：{time.time() - target[3]}\033[0m")
        else:
            break
    print("已确认点位：")
    for target in target_list:
        if target[5] == 'Y':
            print(f"\033[0;32;40m{target[0]} [{target[1]}, {target[2]}] 上次访问时间: {time.time() - target[4]} 持续时间：{time.time() - target[3]}\033[0m")

    print("\n\n\n\n\n")

    if time.time() - start_time > 1:
        start_time = time.time()
        msg = "最近的十条检测结果：\n" + print_load()

    print(msg)


def SaYi_open(ip, port):
    global counter, SaYi_terminate
    title()
    print("\033[5;33m等待接收数据\033[0m")
    # 默认tcp方式传输
    sk = socket.socket()
    # 绑定IP与端口
    ip_port = (ip, port)
    # 绑定监听
    sk.bind(ip_port)
    # 最大连接数
    sk.listen(5)
    # 不断循环接收数据
    while True:
        conn, address = sk.accept()
        if SaYi_terminate:
            return
        print("\033[0;32m链接发生，开始接收数据\033[0m")
        act_time = time.time()
        while True:
            if SaYi_terminate:
                return
            data = conn.recv(1024)
            data = data.decode()
            # print(data)
            data_clear()

            try:
                name, x, y, return_time = data.split('|')
                if name != 'none':
                    counter += 1
                    data_process(name, float(x), float(y))
                data_show()
            except:
                pass


def SV_open_SaYi():
    SaYi_open('127.0.0.1',  8888)


def SaYi_terminal(arg):
    global SaYi_terminate
    SaYi_terminate = arg
