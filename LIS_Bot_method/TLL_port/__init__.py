#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/12/17 下午6:51
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm

# 提供给SaYi_991的TTL接口
# TTL_port会持续打开并接受来自他人的指令

import socket
import json
import time
import os


class TLL_Port:
    def __init__(self):
        self.name = None
        self.tll_port = None  # 端口值
        self.tsk_port = None
        self.nlp_port = None
        self.access_list = {"DzyCd": {"level": 0, "cyber_pos": 0, "real_pos": 0, "tll_port": 0},
                            "SaYi_SV": {"level": 2, "cyber_pos": '127.0.0.1', "real_pos": 0, "tll_port": 8040}
                            }  # 机器人权限表
        self.command_list = {}
        self.permission_list = {}
        self.translate_list = {}
        self.socket = None
        self.log = '/asset/output_log.json'
        self.run_time = 0
        self.real_pos = None
        self.cyber_pos = None
        self.th1 = None
        self.th2 = None
        self.th3 = None
        self.process_check = {}

    def send(self, args):
        target, function = args
        self.request("tips", target, f"dec_({function})")

    def nlp_check(self, msg):
        socket_client = socket.socket()
        socket_client.connect((self.cyber_pos, self.nlp_port))
        socket_client.send(msg.encode("utf-8"))
        socket_client.close()

    def request(self, command, name, function):
        pos, port = self.access_list[name]["cyber_pos"], self.access_list[name]["tll_port"]
        text = f"{self.name} {command} {name} {function} {time.time()} {self.cyber_pos}+{self.tll_port}+{self.real_pos}"
        print(f"\033[0;34;40m send to {pos}, {port} :{text}\033[0m")
        socket_client = socket.socket()
        socket_client.connect((pos, port))
        socket_client.send(text.encode("utf-8"))
        socket_client.close()

    def access_update(self, arg):
        self.access_list = json.loads(arg.replace("'", '"'))

    def write(self, key, arg, form):
        with open(os.getcwd() + '/' + self.name + self.log, 'r') as f:
            msg = f.read()
            p = json.loads(msg)
            if form == 'cover':  # 直接覆盖
                p['data'][key] = arg
            if form == 'add':  # 追加
                p['data'][key].append(arg)
        with open(os.getcwd() + '/' + self.name + self.log, 'w') as f:
            f.write(json.dumps(p))

    def Natual(self, arg):
        pass

    def give_output(self, arg):
        self.nlp_check(arg[0])

    def get_msg(self, key=None, arg=None):
        with open(os.getcwd() + '/' + self.name + self.log, 'r') as f:
            msg = f.read()
            p = json.loads(msg)
            if key is None:
                return str(p)
            if arg is None:
                return p[key]
            return p[key][arg]

    def blocked_check(self, arg):
        try:
            if self.process_check[arg] == 'f':
                return False
            else:
                t = self.process_check[arg]
                self.process_check[arg] = 'f'
                return t
        except:
            return False

    def decode_msg(self, msg:str):
        try:
            if "cons" == msg.split(" ")[1]:
                name = msg.split(' ')[0]
                ans = self.blocked_check(name)
                if ans:
                    bot_name, command, target_name, func, time, place = msg.split(" ")
                    func = func.replace("(", "<").replace(")", ">")
                    self.request("cons", ans, f"200({bot_name}回答{func})")
                return "200"

            bot_name, command, target_name, func, time, place = msg.split(" ")

            if float(time) < self.run_time:
                return f"cons {bot_name} 402(Arrived_too_late)"

            self.run_time = float(time)

            if target_name != self.name:
                return f"cons {bot_name} 405(Wrong_target)"

            if bot_name not in self.access_list.keys():
                # self.request("tips", "SaYi_SV", "get(access_list)")
                return "400"
            body, args = func.split("(")
            if body == "access_update" and bot_name == "SaYi_SV":
                self.access_update(args[0:-1])
                return f"cons {bot_name} 201({msg})" if command == 'tips' else f"cons {bot_name} 201(Success)"

            if body not in self.permission_list.keys():
                return f"cons {bot_name} 404(No_function)"
            try:
                permission = self.permission_list[body].split(",")
                for i in permission:
                    name, arg = i.split("=")
                    if "level" == name and int(arg) != self.access_list[bot_name]["level"]:
                        return f"cons {bot_name} 403(No_access)"
                    if "name" == name and arg != "DzyCd" and arg != bot_name and not (
                            arg == "self" and bot_name == self.name):
                        return f"cons {bot_name} 403(No_access)"
            except:
                pass


        except Exception as e:
            print(f"\033[0;31m[!]From TLL:{e}\033[0m")
            return "101"

        try:
            arg_list = args[0:-1].strip(" ").split(",")
            msg = self.command_list[body](arg_list)
            if msg is None:
                return f"cons {bot_name} 201({msg})" if command == 'tips' else f"cons {bot_name} 201(Success)"
            if msg == "200" or msg == "400":
                return msg
            if len(msg) > 3 and msg[0:4] == "203+":
                self.process_check[msg[4:]] = bot_name
                return "203"
            if len(msg) > 3 and msg[0:4] == "202+":
                command, function = msg[4:].split("+")
                function = function.replace(" ", "")
                return f"{command} {bot_name} {function}"
            if msg == "406":
                return f"cons {bot_name} 406(Target_business)"
            if msg == "503":
                return f"cons {bot_name} 503(System_error)"

            return f"cons {bot_name} 201({msg})" if command == 'tips' else f"cons {bot_name} 201(Success)"
        except Exception as e:
            print(f"\033[0;31m[!]From TLL:{e}\033[0m")
            return f"407"

    def boot(self):
        self.socket = socket.socket()
        print(self.name + ": TLL open in ", self.cyber_pos, self.tll_port)
        self.socket.bind((self.cyber_pos, self.tll_port))
        self.socket.listen(5)
        try:
            self.request("tips", "SaYi_SV", "get(access_list)")
        except:
            pass
        while True:
            conn, address = self.socket.accept()
            data: str = conn.recv(1024).decode("UTF-8")
            if len(data):
                try:
                    if data[0:7] != "process":
                        print(f"\033[0;32;40m >>>from {data}\033[0m")
                        self.nlp_check(data)
                    else:
                        data = data[7:]
                        print(f"\033[0;32;40m >>>process {data}\033[0m")
                        ans = self.decode_msg(data)
                        if ans == "101":
                            self.request('cons', data.split(' ')[0], '101(TLL_error)')
                        elif ans == "407":
                            self.request('cons', data.split(' ')[0], '407(Unknown_problem)')
                        elif ans == "400":
                            self.request('tips', "SaYi_SV", "get(access_list)")
                            self.request('cons', data.split(' ')[0], '400(Not_LIS_BOT)')
                        elif ans == "203":
                            pass
                        elif ans == "200":
                            self.nlp_check(f"finish{data}")
                        else:
                            command, name, function = ans.split(" ")
                            self.request(command, name, function)



                except Exception as e:
                    print(f"\033[0;31m[!]From TLL:{e}\033[0m")
            conn.close()
