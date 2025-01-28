#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/17 下午6:54
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm
import socket
import time
import random
from LIS_Bot_method.LLM_model.deepseek_chat import response


# NLP 用于对自然语言转写TTL并提供聊天机制

# 下一步写一个情感池。


class NLP_Port:
    def __init__(self):
        self.name = "LIS_BOT"
        self.user = "user"
        self.function = ["用自己的语言陈述下面的处理结果:", "", "，不要带有多余的内容"]
        self.model = response()
        self.status = "finish"
        self.done = """ """
        self.cyber_pos = "127.0.0.1"
        self.real_pos = ""
        self.nlp_port = None
        self.tll_port = None
        self.tsk_port = None
        self.socket = ""
        self.free_time = time.time()
        self.spare_time_limit = 300
        self.history_list = []
        self.round = 0
        self.access_list = {"DzyCd": {"level": 0, "cyber_pos": "None", "real_pos": "None", "tll_port": "None", "introduce": "所有机器人的主人"},
                            "SaYi_SV": {"level": 2, "cyber_pos": '127.0.0.1', "real_pos": "None", "tll_port": 8040, "introduce": "所有家庭机器人的中枢。"},
                            "SaYi_991": {"level": 2, "cyber_pos": '127.0.0.1', "real_pos": "None", "tll_port": 8080, "introduce": "中层处理机器人，可以处理别人返回的数据，可以连接其它Skaye系列机器人"},
                            "Skaye_800": {"level": 3, "cyber_pos": '127.0.0.1', "real_pos": "None", "tll_port": 8060, "introduce": "上层监控机器人，可以提供监控功能。"},
                            "SaYi_998": {"level": 2, "cyber_pos": '47.100.11.98', "real_pos": "None", "tll_port": 8080, "introduce": "就是你。负责直接辅佐单子叶蚕豆的日常事务。"}
                            }
        self.translate = []

    def update_info(self):
        return f"""
        """

    def random_voice(self):
        random_message = ["给我讲个童话故事的片段来引起我的注意", "给我讲个网上的新闻来引起我的注意",
                          "给我讲个笑话来引起我的注意",
                          "想象一下未来的人的生活", "详细描述一个全球历史中发生的事情", "对我刚刚说的事情提问",
                          "你已经发现自己被闲置很长时间了，说点话来引起我的注意",
                          "你已经被闲置好久了，表达一下自己的无聊来引起我的注意"]
        while False:
            if time.time() - self.free_time > self.spare_time_limit:
                self.free_time = time.time()
                self.tell_to_TSK("speak" + self.get_process(random.choice(random_message), 2))
            time.sleep(10)

    def get_process(self, msg, mode):
        # mode0 : 碎片信息转写（涉及Natual to TLL、TLL to Natual时使用)  mode1：正常聊天  mode2:简洁模式，不让说废话
        message = self.function[mode] + msg
        if mode == 0:
            return self.model.process(message, "solo")
        if mode == 1:
            return self.model.process(message, "chat")
        if mode == 2:
            return self.model.process(message, "solo")

    def central_Split(self, msg):
        process_result = "正在执行" if self.status == "finish" else self.status
        return msg + "结果为" + process_result

    # 提炼号的关键词在确认为TLL时进行TLL处理
    def TLL_to_Natual(self, msg):
        if "finish" == msg[0:6]:
            msg = msg[6:]
        bot_name, command, target_name, func, time, place = msg.split(" ")
        time = float(time)
        body, args = func.split('(')
        arg, ans = args.split(')')
        cyber_pos, port, real_pos = place.split('+')
        msg = f"{bot_name} 说 {arg}"
        return msg

    # 返回机器人清单
    def introduce(self):
        msg = ""
        for i in self.access_list:
            msg += i + ':' + self.access_list[i]['introduce'] + '\n'
        return msg

    # 外面返回的TLL在确认陈述给人时进行Natual处理
    def Natual_to_TLL(self, msg):
        message = [{"role": "system",
                    "content": f"""#### 定位
                            - 智能助手
                             - 名称 ：文本分类specialist
                             - 主要任务 ：
                             下面对输入的文本文字进行自动分类，识别其所指示的机器人名称和对他的命令。机器人的名称见"文本种类。

                             #### 能力
                             - 分类识别 ：根据分析结果，将文本分类到预定义的机器人名字中。

                             #### 知识储备
                             - 文本种类 ：
                             {self.introduce()}

                             #### 使用说明
                             - 输入 ：一段文本。
                             - 输出 ：只输出机器人的名称和对他的命令。以【机器人的名称】+【对他的命令】格式返回，不需要额外解释。"""
                    }, {"role": 'user', 'content': msg}]

        a = self.model.process(message, "solo")

        p = a.replace("【", "").replace("】", "")
        botname, command = p.split('+')

        return f"{self.name} tips {self.name} send({botname},{command}) {time.time()} {self.cyber_pos}+{self.tll_port}+{self.real_pos}"

    def receiver_judge(self, msg, language):
        if language == "TLL":
            return "Natual" if "finish" == msg[0:6] else "TLL"

        message = [{"role": "system",
                    "content": f"""#### 定位
                    - 智能助手
                     - 名称 ：文本分类specialist
                     - 主要任务 ：这是其他机器人:{self.introduce()} 。
                     下面对输入的文本文字进行自动分类，识别其所属的文本类型，Natual说明是在跟模型聊天对话，TLL说明让模型完成对其他机器人的指令
                     
                     #### 举例
                     - 输入：你问问前端监控？
                     - 输出：TLL
                     - 输入：我回来了。前面监控方面有什么异常吗？
                     - 输出：TLL
                     - 输入：我回家来了
                     - 输出：Natual
                     #### 能力
                     - 分类识别 ：根据分析结果，将文本分类到预定义的种类中。
                     
                     #### 知识储备
                     - 文本种类 ：
                       - TLL
                       - Natual
                         
                     #### 使用说明
                       - 输入 ：一段文本。
                       - 输出 ：只输出文本所属的种类，不需要额外解释。"""
                    }, {"role": 'user', 'content': msg}]
        a = self.model.process(message, "solo")
        print(a)
        return a

    # 确定语言类型
    def language_judge(self, msg):
        try:
            bot_name, command, target_name, func, time, place = msg.split(" ")
            # time = float(time)
            # body, args = func.split('(')
            # arg, ans = args.split(')')
            # cyber_pos, port, real_pos = place.split('+')
            if command not in ["cons", "tips", "dos"]:
                return "Natual"
            return "TLL"
        except:
            return "Natual"

    def tell_to_NLP(self, msg):
        socket_client = socket.socket()
        socket_client.connect((self.cyber_pos, self.nlp_port))
        socket_client.send(msg.encode("utf-8"))
        socket_client.close()

    def tell_to_TSK(self, msg):
        socket_client = socket.socket()
        socket_client.connect((self.cyber_pos, self.tsk_port))
        socket_client.send(msg.encode("utf-8"))
        socket_client.close()

    def get_function(self, msg):
        return self.model.process(msg, "tool", self.translate)

    # 上传给自己的TLL端口
    def tell_to_TLL(self, msg):
        bot_name, command, target_name, func, times, place = msg.split(" ")
        if func.split('(')[0] == 'dec_':
            func = self.get_function(func[5:-1])

        msg = f"process{bot_name} {command} {target_name} {func} {times} {place}"
        # print(self.tll_port)
        socket_client = socket.socket()
        socket_client.connect((self.cyber_pos, self.tll_port))
        socket_client.send(msg.encode("utf-8"))
        socket_client.close()
        # print("send back:"+msg)

    # 上传给外部控制台
    def tell_to_Natual(self, msg):
        return msg

    def decode(self, msg):
        language = self.language_judge(msg)
        receiver = self.receiver_judge(msg, language)
        # print(language, receiver)
        # 释放截获信号
        if language == "TLL":
            if receiver == "Natual":
                msg = self.TLL_to_Natual(msg)
                return msg
            else:
                self.tell_to_TLL(msg)
        else:
            if receiver == "TLL":
                try:
                    self.tell_to_TLL(self.Natual_to_TLL(msg))
                    # self.tell_to_Natual(self.central_Split(msg))
                except:
                    print("TLL分析失败，转为Natual解释...")
                    receiver = 'Natual'
            if receiver == "Natual":
                msg = self.get_process(msg, 1)
                if msg[:6] == '[self]':
                    self.tell_to_TLL(
                        f"{self.name} dos {self.name} {msg[6:]} {time.time()} {self.cyber_pos}+{self.tll_port}+{self.real_pos}")
                else:
                    return self.tell_to_Natual(msg)


    def receive(self):
        self.socket = socket.socket()
        print(self.name + ": NLP open in ", self.cyber_pos, self.nlp_port)
        self.socket.bind((self.cyber_pos, self.nlp_port))
        self.socket.listen(5)

        while True:
            conn, address = self.socket.accept()
            data: str = conn.recv(1024).decode("UTF-8")
            # print("get message:" + data)
            if len(data):
                try:
                    self.free_time = time.time()
                    ans = self.decode(data)
                    if ans is not None:
                        self.tell_to_TSK("speak" + ans)
                except Exception as e:
                    print(f"\033[0;31m[!]From NLP:{e}\033[0m")
            conn.close()

    def boot(self):
        from threading import Thread
        th1 = Thread(target=self.receive)
        th2 = Thread(target=self.random_voice)

        th1.start()
        th2.start()

        th1.join()
        th2.join()
