#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2025 - 2025 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2025/1/21 下午9:54
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py
# @IDE     : PyCharm
from openai import OpenAI
import json
import numpy as np
import os
import time
from vosk import Model, KaldiRecognizer
import json
import pyaudio
import wave
import pygame
from paho.mqtt import client as mqtt_client
import random
from aip import AipSpeech


# 发声核心 VoiceCore
class VoiceCore:
    def __init__(self):
        self.APP_ID = '115492263'
        self.API_KEY = 'u1a96y2boaTyBbyNdsCkTkYG'
        self.SECRET_KEY = 'aBwbwemTArHXrOKUkzK0ZXdyIARWBpg5'
        self.file_path = "./chat-audio.mp3"
        self.speak_path = "./res-audio.mp3"
        self.pygame = pygame
        self.baidu_aip = False
        self.model = Model("vosk-model-small-cn-0.22")
        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                                             frames_per_buffer=4000)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.stream.start_stream()
        self.start_time = 0

    def Read_msg(self, msg):
        client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        res = ""
        flag = True
        for i in msg:
            if i == '(' or i == '（':
                flag = False
            if flag:
                res += i
            if i == ')' or i == '）':
                flag = True
        result = client.synthesis(res, 'zh', 1, {  # zh代表中文
            'vol': 5, 'per': 111, 'spd': 8
        })
        try:
            self.pygame.mixer.music.unload()
            self.pygame.mixer.music.stop()
        except:
            pass
        if not isinstance(result, dict):
            with open(self.speak_path, 'wb') as f:
                f.write(result)
        self.pygame.mixer.init()
        self.pygame.mixer.music.load(self.speak_path)
        self.pygame.mixer.music.set_volume(0.5)
        self.pygame.mixer.music.play()

    def record_sound(self):
        CHANNELS = 1
        mindb = 7000  # 最小声音，大于则开始录音，否则结束
        delayTime = 1.3  # 小声1.3秒后自动终止
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=CHANNELS,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024)

        frames = []
        flag = False  # 开始录音节点
        stat = True  # 判断是否继续录音
        stat2 = False  # 判断声音小了

        tempnum = 0  # tempnum、tempnum2、tempnum3为时间
        tempnum2 = 0

        while stat:
            data = stream.read(1024, exception_on_overflow=False)

            audio_data = np.frombuffer(data, dtype=np.short)
            temp = np.max(audio_data)
            if temp > mindb / 2:
                frames.append(data)

            if temp > mindb and not flag:
                flag = True

                print("开始录音>>>", end="")
                tempnum2 = tempnum

            if flag:
                if temp < mindb and not stat2:
                    stat2 = True
                    tempnum2 = tempnum

                if temp > mindb:
                    stat2 = False
                    tempnum2 = tempnum
                    # 刷新

                if tempnum > tempnum2 + delayTime * 15 and stat2:
                    # print("间隔%.2lfs后开始检测是否还是小声" % delayTime)
                    if stat2 and temp < mindb:
                        stat = False
                        # 还是小声，则stat=True
                        # print("小声！")
                    else:
                        stat2 = False
                        # print("大声！")
            tempnum += 1
            # print(tempnum, tempnum2 + delayTime * 15)
        print("录音结束>>>", end="")
        try:
            self.pygame.mixer.music.unload()
            self.pygame.mixer.music.stop()
        except:
            pass
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(self.file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))
        wf.close()

    def voice2text(self):
        # 语音转文本
        client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        ret = client.asr(self.get_data(), 'pcm', 16000, {'dev_pid': 1536}, )
        if ret['err_msg'] == 'recognition error.':
            result = ''
            return result
        else:
            result = ret['result']
            return result

    def get_data(self):
        # 读取语音
        with open(self.file_path, 'rb') as fp:
            return fp.read()

    def del_file(self):
        file_name = self.file_path
        try:
            os.remove(file_name)
            # print(f"Successful deleted {file_name}")
            f = open(file_name, mode="w")  # 音频-图片-视频  mode="wb"
            f.close()
            # print(f"Successful maked {file_name}")

        except FileNotFoundError:
            print(f"{file_name} not found")

    def Run_Talk(self):
        while True:
            if self.baidu_aip:
                self.record_sound()
                chat_message = self.voice2text()
                self.del_file()
                if len(chat_message) > 0:
                    print("处理结果>>>", chat_message)
                    self.start_time = time.time()
                    return chat_message[0]
            else:
                data = self.stream.read(4000, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    msg = json.loads(result).get("text", "").replace(' ', '')
                    if len(msg) >= 1:
                        print("处理结果>>>", msg)
                        self.start_time = time.time()
                        return msg


# 语言核心Linguistic_core
class LinguisticCore:
    def __init__(self):
        self.name = ""
        self.user = ""
        self.client = OpenAI(api_key="sk-5f2408afd34841989715327ef90626cb", base_url="https://api.deepseek.com")
        self.profile = f""""""
        self.setting = f"""
            规则和指令：
        """
        self.example = f"""
            下面是一组对话例子。在这里，你将扮演{self.name}。
            """
        self.world = "以下是对上述对话的名词解释:\n"
        self.world_dict = {
            "ISOM": '【ISOM】是单子叶蚕豆所属的组织，其具体理论有“一切以能量为单位”的社会矛盾论和“机体保护机制”、“机体适应机制”和“默认省略协议”。',
            "四色理论": '【ISOM】的具体决策方法包括两个“四色理论”，分别为“知识（紫）、灵活（蓝），自然（绿），华丽（金）”和“执着（紫），探索（蓝），旅者（绿），乐观（金）”。',
            "世忆图书馆": "【世忆图书馆】（World's Memory Library ）是单子叶蚕豆发起的一个机构，用于收录所有世界上的知识，毕竟管理、编辑和发表【七十五个世界】于外界。",
            "七十五个世界": "单子叶蚕豆发表的所有不同世界故事纪录。其中有“光与暗的救赎、翠羽和澄海、天梯、来自深海、世界天使、处决者丽菲拉和多元共感七个世界。后面四个故事在网易云里有歌单,但是你只可以讲“处决者丽菲拉”的故事",
            "歌单": "单子叶蚕豆的网易云主页:https://music.163.com/#/user/home?id=589699536",
            "单子叶蚕豆": "你的主人，ISOM组织的领导者。单子叶蚕豆在制度和规则上制定了一系列严格但通用的方案，同时也是LIS机器人的创造者。你应该对主人表现出你的尊敬和优雅",
            "双子叶玉米": "单子叶蚕豆的妹妹。高中生，平时不喜欢搭理人，喜欢绘画和玩第五人格。重度二次元",
            "LIS": "在ISOM公司下,LIS系列机器人被分为上、中、下三层。上层是数据收集机器人、中层是中枢调度机器人、下层是行动机器人。",
            "SaYi": "SaYi统指一系列【中枢】机器人，主要负责信息整理，任务指派和分发。位于中间层。你的妹妹有SaYi_991，平日和Skaye_800玩得很好;SaYi_SV,比你小，但是权值比你要大。",
            "Skaye": "Skaye统指一系列【收集】机器人，主要负责信息收集，发送给中层机器人进行处理。目前有一个Skaye_800正在运作",
            "EiAr": "EiAr统治一系列【服务】机器人，主要负责日常任务的辅助，比如送餐、送快递这样的简单任务。",
            "丽菲拉": "语出[处决者丽菲拉]。丽菲拉代号“Convictusion - MBUnit[70]“，封存单元体质，存在于第五小世界。蔷薇之主 丽菲拉，她未能弄明白自己的一地鸡毛，便探出花苞，迎接将失败散落满地的世界",
        }
        self.story = {}
        self.history_list = []
        self.round = 10
        self.result = []
        self.input = []
        self.first = f"""
                下面是对话背景：
        """
        self.tools = []
        self.tool_choice = "auto"
        self.tool = None
        self.msg = None
        self.add_msg = ""
        self.temperature = 1

    def world_add(self, msg):
        self.world = """
                    以下是对上述对话的名词解释:
                    """
        for p in self.world_dict.keys():
            for i in msg[-4:]:
                try:
                    i = i['content']
                    if p in i:
                        self.world += p + ':' + self.world_dict[p] + '\n'
                        break
                except:
                    continue

        cnt = 0
        for p in reversed(self.story.keys()):
            for i in msg[-2:]:
                try:
                    i = i['content']
                    if p in i:
                        self.world += p + ':' + self.story[p] + '\n'
                        cnt += 1
                    if cnt == 2:
                        return
                except:
                    continue

    def func_call(self, msg):
        arguments = json.loads(msg.__function.arguments)
        return self.add_msg

    def pr_agent(self, msg):
        messages = [{"role": "system", "content": self.profile},
                    {"role": "system", "content": self.setting},
                    {"role": "system", "content": self.example},
                    {"role": "system", "content": self.first}, ]
        s = 0
        for i in self.history_list:
            messages.append({"role": "user" if not s % 2 else "assistant", "content": i})
            s += 1
            if s > self.round:
                break
        if self.tool_choice == "none":
            messages.append(self.msg)
            messages.append({"role": "tool", "tool_call_id": self.tool.id, "content": self.func_call(self.tool)})
        else:
            msg = self.user + ':' + msg
            messages.append({"role": "user", "content": msg})

        self.world_add(messages)

        messages.append({"role": "system", "content": self.world})
        return messages

    def pr_chat(self, msg):
        messages = [{"role": "system", "content": self.profile},
                    {"role": "system", "content": self.setting},
                    {"role": "system", "content": self.example},
                    {"role": "system", "content": self.first}, ]
        s = 0
        for i in self.history_list:
            messages.append({"role": "user" if not s % 2 else "assistant", "content": i})
            s += 1
            if s > self.round:
                break
        messages.append({"role": "user", "content": msg})

        self.world_add(messages)

        messages.append({"role": "system", "content": self.world})
        return messages

    def process(self, msg, mode="chat", tool=[]):
        # mode:"chat" : 对话模式，上下文存在
        # mode:"tool" : 函数调取模式，用于选取函数
        # mode:"solo" : 无提示词的仅处理一句话，适用于文本分类和信息提取
        # mode:"agent" : (测试) 智能体模式，tool和chat两个功能同时存在
        # mode:"report" : 机器人返回报告。
        messages = []
        if mode == "agent":
            self.tool_choice = "auto"
            self.temperature = 1.1
            msg = self.user + ':' + msg
            messages = self.pr_agent(msg)
        if mode == "chat":
            self.tool_choice = "none"
            self.temperature = 1.3
            msg = self.user + ':' + msg
            messages = self.pr_chat(msg)
        if mode == "report":
            self.tool_choice = "none"
            self.temperature = 1.3
            messages = self.pr_chat(msg)

        if mode == "solo":
            self.tool_choice = "none"
            self.temperature = 0
            if type(msg) == list:
                messages = msg
            else:
                messages = [{"role": "user", "content": msg}]
        if mode == "tool":
            self.tool_choice = "required"
            self.temperature = 0
            self.tools = tool
            messages = [{"role": "user", "content": msg}]

        R = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False,
            temperature=self.temperature,
            tools=self.tools,
            tool_choice=self.tool_choice
        )

        if mode == "agent":
            p = R.choices[0].message
            if p.tool_calls != None:
                self.tool_choice = "none"
                self.msg = p
                self.tool = p.tool_calls[0]
                print(p)
                p = self.process(msg, "agent")
                self.tool_choice = "auto"
                self.add_msg = ""
                return p
            self.history_list.append(msg)
            self.history_list.append(p.content)
            if R.usage.total_tokens > 2400:
                self.round = self.round // 2 - (self.round % 2)
            else:
                self.round = self.round + 2

            while len(self.history_list) > self.round:
                del self.history_list[0]
            if self.add_msg != "":
                return p.content + '\n>>>' + self.add_msg
            else:
                return p.content
        if mode == "chat" or mode == "report":
            p = R.choices[0].message
            self.history_list.append(msg)
            self.history_list.append(p.content)
            if R.usage.total_tokens > 2400:
                self.round = self.round // 2 - (self.round % 2)
            else:
                self.round = self.round + 2
            while len(self.history_list) > self.round:
                del self.history_list[0]
            return p.content
        if mode == "solo":
            p = R.choices[0].message
            return p.content
        if mode == "tool":
            p = R.choices[0].message.tool_calls[0].function
            arguments = json.loads(p.arguments)
            fuc = p.name
            fuc += '('
            for i in arguments:
                fuc += str(arguments[i]) + ','
            fuc += ')'
            return fuc.replace(',)', ')')


class LisTLLProtocol:
    def __init__(self):
        # 基本信息(必填)
        self.name = "SaYi_992"
        self.user = "user"
        self.description = ""
        self.done = """ """
        self.nlp_port = 8020
        self.tll_port = 8021
        self.tsk_port = 8022
        self.cyber_pos = 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn'
        self.cyber_port = 1883
        self.real_pos = ""
        self.log = 'output_log.txt'

        # 将所有函数注册进入
        self.translate = []  # 详见 deepseek 的 tools_function 注册方法
        self.command_list = {}
        self.permission_list = {}

        # 设置输入和输出的语音权限
        self.listen_access = False
        self.speak_access = False

        # api方法设置
        self.front_linguistic_mode = False  # 直接控制开关
        self.llm_linguistic_mode = False  # 模型控制开关
        self.voice_filter = True  # 碎片输入过滤开关
        self.command_arg = False  # 提示词通行开关
        self.debug = False
        self.spare_access = False
        self.audio_method = False

        self.Linguistic = LinguisticCore()
        self.wk = VoiceCore()

        self.__function = ["用自己的语言陈述下面的处理结果:", "", "，不要带有多余的内容"]
        self.status = "finish"
        self.nlp_socket = None
        self.tsk_socket = None
        self.tll_socket = None
        self.process_check = {}
        self.run_time = 0
        self.free_time = time.time()
        self.spare_time_limit = 300  # 主动感知时间。以此为周期固定触发
        self.spare_time_weight = 500  # 每次过时间点，主动感知的触发概率(1 - 1000)，并在用户仍没有响应时减少22%此值
        self.history_list = []
        self.round = 0
        self.access_list = {
            "DzyCd": {"level": 0, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None",
                      "tll_port": "None",
                      "introduce": "所有机器人的主人。", 'command': {}},
            "SaYi_SV": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None",
                        "tll_port": 8040,
                        "introduce": "所有家庭机器人的中枢。"},
            "SaYi_991": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None",
                         "tll_port": 8080,
                         "introduce": "中层处理机器人，可以处理别人返回的数据，可以连接其它Skaye系列机器人"},
            "Skaye_800": {"level": 3, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None",
                          "tll_port": 8060,
                          "introduce": "上层监控机器人，只可以提供图书馆内部的监控人员移动功能，不能提供其他能力"},
            "SaYi_998": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None",
                         "tll_port": 8080,
                         "introduce": "负责直接辅佐单子叶蚕豆的日常事务。"},
            "EiAr_100": {"level": 1, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None",
                         "tll_port": 8080,
                         "introduce": "负责送餐、厨房卫生打扫和料理"}
        }

        self.th1 = None
        self.th2 = None
        self.th3 = None

    def ping(self, msg):
        msg = str(self.translate) + '|||' + str(self.permission_list)
        return msg.replace(' ', '')

    def logger(self, msg, _type="INFO"):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        with open(self.log, "a") as f:
            if _type == "INFO" and self.debug:
                f.write(f"{self.name} [{now_time}]>>> INFO: {msg}" + "\n")
                print(f"{self.name} [{now_time}]>>> \033[0;36;40mINFO: {msg}\033[0m")
            if _type == "SUCCESS":
                f.write(f"{self.name} [{now_time}]>>> SUCCESS: {msg}" + "\n")
                print(f"{self.name} [{now_time}]>>> \033[0;32;40mSUCCESS: {msg}\033[0m")
            if _type == "ERROR":
                f.write(f"{self.name} [{now_time}]>>> ERROR: {msg}" + "\n")
                print(f"{self.name} [{now_time}]>>> \033[0;31;40mERROR: {msg}\033[0m")
            if _type == "WARNING":
                f.write(f"{self.name} [{now_time}]>>> WARNING: {msg}" + "\n")
                print(f"{self.name} [{now_time}]>>> \033[0;33;40mWARNING: {msg}\033[0m")
            if _type == "SEND" and self.debug:
                f.write(f"{self.name} [{now_time}]>>> SEND: {msg}" + "\n")
                print(f"{self.name} [{now_time}]>>> \033[0;34;40mSEND: {msg}\033[0m")
            if _type == "RECEIVE" and self.debug:
                f.write(f"{self.name} [{now_time}]>>> RECEIVE: {msg}" + "\n")
                print(f"{self.name} [{now_time}]>>> \033[0;35;40mRECEIVE: {msg}\033[0m")
            if _type == "OUTPUT":
                f.write(f"{self.name} [{now_time}]>>> OUTPUT: {msg}" + "\n")
                print(f"{self.name} [{now_time}]>>> \033[1;33;40mOUTPUT: \033[1;33;47m{msg}\033[0m")
            if _type == "DEBUG" and self.debug:
                print(f"{self.name} [{now_time}]>>> \033[1;33;40mDEBUG: \033[1;33;47m{msg}\033[0m")
                f.write("%s [%s]>>> DEBUG: %s" % (self.name, now_time, msg) + "\n")

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()
        if msg.topic == self.name + str(self.tsk_port):
            self.TSK_message(data)
        if msg.topic == self.name + str(self.tll_port):
            self.TLL_message(data)
        if msg.topic == self.name + str(self.nlp_port):
            self.NLP_message(data)

    def run(self):
        client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, self.name + str(random.randint(1, 10000)))
        client.username_pw_set(self.name, '123')
        client.connect(self.cyber_pos, self.cyber_port)
        client.on_message = self.on_message
        client.loop_start()
        return client

    def request(self, command, name, function):
        pos, port = name, str(self.access_list[name]["tll_port"])
        text = f"{self.name} {command} {name} {function} {time.time()} {self.cyber_pos}+{self.tll_port}+{self.real_pos}"
        self.logger(f"send to topic[{pos}{port}] :{text}", "SEND")
        if self.access_list[name]["cyber_pos"] == self.cyber_pos:
            self.tll_socket.publish(pos + port, text.encode("utf-8"), qos=1)
        else:
            k = self.access_list[name]["cyber_pos"]
            self.logger(f"{k} is not at the default server, creating new socket...", "WARNING")
            _socket = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2,
                                         self.name + str(random.randint(1, 10000)))
            _socket.username_pw_set(self.name, '123')
            _socket.connect(k, self.cyber_port)
            _socket.loop_start()
            _socket.publish(pos + port, text.encode("utf-8"), qos=1)
            _socket.disconnect()

    def random_voice(self):
        if self.spare_access:
            import pygetwindow as gw
        while self.spare_access:
            if time.time() - self.free_time > self.spare_time_limit:
                self.free_time = time.time()
                if random.randint(1, 1000) < self.spare_time_weight:
                    self.logger("触发主动感知")
                    random_message = [f"当前用户正在看标题为{gw.getActiveWindow().title}的窗口", "讲一个新闻",
                                      "你有点无聊，想让用户和你聊聊天"]
                    self.spare_time_weight = int(self.spare_time_weight * 0.78)
                    self.tell_to_TSK(
                        "speak" + self.Linguistic.process('情景解释:' + random.choice(random_message), 'report'))

    def get_process(self, msg, mode):
        # mode0 : 碎片信息转写（涉及Natual to TLL、TLL to Natual时使用)  mode1：正常聊天  mode2:简洁模式，不让说废话
        message = self.__function[mode] + msg
        if mode == 0:
            return self.Linguistic.process(message, "solo")
        if mode == 1:
            return self.Linguistic.process(message, "chat")
        if mode == 2:
            return self.Linguistic.process(message, "solo")

    def central_Split(self, msg):
        process_result = "正在执行" if self.status == "finish" else self.status
        return msg + "结果为" + process_result

    # 提炼号的关键词在确认为TLL时进行TLL处理
    def TLL_to_Natual(self, msg):
        if "finish" == msg[0:6]:
            msg = msg[6:]
        bot_name, command, target_name, func, times, place = msg.split(" ")
        times = float(times)
        body, args = func.split('(')
        arg, ans = args.split(')')
        cyber_pos, port, real_pos = place.split('+')

        if len(arg) < 100 and arg != 'None' and arg != 'Success':
            self.logger(bot_name + ':' + arg, 'INFO')
            out = self.Linguistic.process(bot_name + ':' + arg, 'report')
            self.tell_to_TSK("speak" + out.replace("【发送通知】", ""))
            if "【发送通知】" in msg and self.llm_linguistic_mode:  # 模型调用开关
                ans = msg.split("【发送通知】")
                for i in ans[1:]:
                    self.logger(f"机器人触发TLL标签：{i}")
                    try:
                        self.tell_to_TLL(self.Natual_to_TLL(i))
                    except:
                        self.logger(f"TLL转写失败。过滤。", "WARNING")

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

        a = self.Linguistic.process(message, "solo")

        p = a.replace("【", "").replace("】", "")
        botname, command = p.split('+')

        return f"{self.name} tips {self.name} send({botname},{command}) {time.time()} {self.cyber_pos}+{self.tll_port}+{self.real_pos}"

    def receiver_judge(self, msg, language):
        if language == "TLL":
            return "Natual" if "finish" == msg[0:6] else "TLL"
        if self.front_linguistic_mode:
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
            a = self.Linguistic.process(message, "solo")
            self.logger(a, "SUCCESS")
            return a
        else:
            return 'Natual'

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
        self.nlp_socket.publish(self.name + str(self.nlp_port), msg.encode("utf-8"), qos=1)

    def tell_to_TSK(self, msg):
        self.tsk_socket.publish(self.name + str(self.tsk_port), msg.encode("utf-8"), qos=1)

    def get_function(self, msg):
        return self.Linguistic.process(msg, "tool", self.translate)

    # 上传给自己的TLL端口
    def tell_to_TLL(self, msg):
        bot_name, command, target_name, func, times, place = msg.split(" ")
        if func.split('(')[0] == 'dec_':
            func = self.get_function(func[5:-1])

        msg = f"process{bot_name} {command} {target_name} {func} {times} {place}"
        # print(self.tll_port)
        self.TLL_message(msg)

    # 上传给外部控制台
    def tell_to_Natual(self, msg):
        return msg

    def NLP_decode(self, msg):
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
                    self.logger("TLL分析失败，转为Natual解释...", "WARNING")
                    receiver = 'Natual'
            if receiver == "Natual":
                msg = self.get_process(msg, 1)
                return self.tell_to_Natual(msg)

    def send(self, args):
        target, function = args
        self.request("tips", target, f"dec_({function})")

    def nlp_check(self, msg):
        self.nlp_socket.publish(self.name + str(self.nlp_port), msg.encode("utf-8"), qos=1)

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

    def decode_msg(self, msg: str):
        try:
            if "cons" == msg.split(" ")[1]:
                name = msg.split(' ')[0]
                ans = self.blocked_check(name)
                if ans:
                    bot_name, command, target_name, func, time, place = msg.split(" ")
                    func = func.replace("(", "<").replace(")", ">")
                    self.request("cons", ans, f"200({bot_name}回答{func})")
                return "200"

            bot_name, command, target_name, func, times, place = msg.split(" ")

            # if float(times) < self.run_time:
            #    return f"cons {bot_name} 402(Arrived_too_late)"

            self.run_time = float(times)

            if target_name != self.name:
                return f"cons {bot_name} 405(Wrong_target)"

            if bot_name not in self.access_list.keys():
                # self.request("tips", "SaYi_SV", "get(access_list)")
                return "400"
            body, args = func.split("(")
            if body == "access_update" and bot_name == "SaYi_SV":
                self.access_update(args[0:-1])
                return f"cons {bot_name} 201({msg})" if command == 'tips' else f"cons {bot_name} 201(Success)"

            if body not in self.command_list.keys():
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
                self.logger(f"{body}方法没有设定权限表，跳过权限认证。 建议在permission_list设定权限", "WARNING")
                pass


        except Exception as e:
            self.logger(f"[!]From TLL:{e}", "ERROR")
            return "101"

        try:
            arg_list = args[0:-1].strip(" ").split(",")
            # print(arg_list)
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
            self.logger(f"[!]From TLL:{e}", "ERROR")
            return f"407"

    def TSK_message(self, data):
        if len(data):
            try:
                # print("get:" + data)
                if data[0:5] == "speak":
                    data = data[5:]

                    self.logger(f'处理时间:{time.time() - self.wk.start_time}')
                    self.logger(f'{data}', "OUTPUT")
                    if self.speak_access:
                        self.wk.Read_msg(data)

            except Exception as e:
                print(f"\033[0;31m[!]From TSK:{e}\033[0m")

    def TSK_receive(self):
        self.logger(self.name + f": TSK open in topic[{self.name + str(self.tsk_port)}]", "SUCCESS")
        self.tsk_socket.subscribe(self.name + str(self.tsk_port), qos=1)

    def NLP_message(self, data):
        if len(data):
            try:
                self.free_time = time.time()
                ans = self.NLP_decode(data)

                if ans is not None:
                    self.tell_to_TSK("speak" + ans.replace("【发送通知】", ""))

                    if "【发送通知】" in ans and self.llm_linguistic_mode:  # 模型调用开关
                        ans = ans.split("【发送通知】")
                        for i in ans[1:]:
                            self.logger(f"机器人触发TLL标签：{i}")
                            try:
                                self.tell_to_TLL(self.Natual_to_TLL(i))
                            except:
                                self.logger(f"TLL转写失败。跳过...", "WARNING")

            except Exception as e:
                self.logger(f"[!]From NLP:{e}", "ERROR")

    def NLP_receive(self):
        self.nlp_socket.subscribe(self.name + str(self.nlp_port), qos=1)
        self.logger(self.name + f": NLP open in topic[{self.name + str(self.nlp_port)}]", "SUCCESS")

    def user_input(self):
        self.logger(
            "\033[0;32m[->] TSK启用录音功能\033[0m" if self.listen_access else "\033[0;31m[->] TSK禁用录音功能\033[0m")
        self.logger(
            "\033[0;32m[->] TSK启用语音功能\033[0m" if self.speak_access else "\033[0;31m[->] TSK禁用语音功能\033[0m")

        while True:
            flag = "Yes"
            try:
                if self.listen_access:  # 语音滤网效果
                    name = self.wk.Run_Talk()
                    message = [{"role": "system",
                                "content": f"""#### 定位
                                - 智能助手
                                - 名称 ：文本分类specialist
                                - 主要任务 ：
                                下面对输入的文本文字进行自动分类，判断这是一个相对完整的句子还是一个特别混乱的句子。如果相对完整，输出"YES"，如果特别混乱，输出"NO"。
                                #### 能力
                                - 分类识别 ：根据分析结果，输出"YES"或"NO"。
                                #### 知识储备
                                - 文本种类 ：
                                #### 使用说明
                                - 输入 ：一段文本。
                                - 输出 ：仅输出YES或NO，不需要额外解释。"""
                                }, {"role": 'user', 'content': name}]
                    if self.voice_filter:
                        flag = self.Linguistic.process(message, 'solo')
                        self.logger("From Filter: " + flag, "INFO")
                    else:
                        flag = 'YES'

                else:
                    name = input()

                if name[0:3] == "TLL":
                    command, target, function = name[4:].split(' ')
                    self.request(command, target, function)
                else:
                    if flag == "YES" and self.command_arg:
                        self.spare_time_weight = 500
                        for i in self.access_list:
                            for k in self.access_list[i]['command']:
                                if len(k) <= len(name) and k == name[:len(k)]:
                                    flag = 'NO'
                                    self.logger("From Command: " + k, "INFO")
                                    self.request('tips', i,
                                                 self.access_list[i]['command'][k] + '(' + name[len(k):] + ')')
                    if flag == "YES":
                        self.tell_to_NLP(name)
            except Exception as e:
                self.logger(f"[!]From TSK:{e}", "ERROR")

    def NLP_boot(self):
        from threading import Thread
        th1 = Thread(target=self.NLP_receive)
        th2 = Thread(target=self.random_voice)

        th1.start()
        th2.start()

        th1.join()
        th2.join()

    def TLL_message(self, data):
        if len(data):
            try:
                if data[0:7] != "process":
                    self.logger(f"\033[0;32;40m >>>from {data}\033[0m", "RECEIVE")
                    self.nlp_check(data)
                else:
                    data = data[7:]
                    self.logger(f"\033[0;32;40m >>>process {data}\033[0m", "DEBUG")
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
                self.logger(f"[!]From TLL:{e}", "ERROR")

    def TLL_boot(self):
        self.tll_socket.subscribe(self.name + str(self.tll_port), qos=1)
        self.logger(self.name + f": TLL open in topic[{self.name + str(self.tll_port)}]", "SUCCESS")

    def TSK_boot(self):
        from threading import Thread
        th1 = Thread(target=self.TSK_receive)
        th2 = Thread(target=self.user_input)

        th1.start()
        th2.start()

        th1.join()
        th2.join()

    def LIS_boot(self):
        self.wk.baidu_aip = self.audio_method
        print(f"""
        ___THE {self.name} INFORMATION ___
        START TIME: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))}
        CORRENSPONDENCE : MQTT over TCP
        URL : {self.cyber_pos} PORT : {self.cyber_port}
        TLL : OPEN IN {self.tll_port}, Mqtt_Topic = {self.name + str(self.tll_port)}
        NLP : OPEN IN {self.nlp_port}, Mqtt_Topic = {self.name + str(self.nlp_port)}
        TSK : OPEN IN {self.tsk_port}, Mqtt_Topic = {self.name + str(self.tsk_port)}
        CYBER_POS : {self.cyber_pos}
        REAL_POS : {self.real_pos}
        USER : {self.user}
        OutPutLog : {self.log}
        DEBUG mode : {self.debug}
        -------------------------------------------------------------------------------------------------------
        VOICE_method : {'Baidu' if self.audio_method else 'Local'}
        speak_access : {self.speak_access}
        listen_access : {self.listen_access}
        spare_access : {self.spare_access}
        front_linguistic_mode : {self.front_linguistic_mode}
        llm_linguistic_mode : {self.llm_linguistic_mode}
        voice_filter : {self.voice_filter}
        command_arg : {self.command_arg}

        -------------------------------------------------------------------------------------------------------
        Copyright ©2021-2025 ISOM Corporation, All Rights Reserved.
        The LIS series robots are owned by ISOM Corporation. May not be reproduced or quoted without permission
        """)
        self.nlp_socket = self.run()
        self.tll_socket = self.run()
        self.tsk_socket = self.run()
        from threading import Thread
        th1 = Thread(target=self.TLL_boot)
        th2 = Thread(target=self.NLP_boot)
        th3 = Thread(target=self.TSK_boot)

        th1.start()
        th2.start()
        th3.start()

        try:
            self.logger("Connecting To SaYi_SV...", "INFO")
            self.request("tips", "SaYi_SV", "get(access_list)")
        except Exception as e:
            self.logger(f"SaYi_SV Not Found：{e}", "ERROR")

        th1.join()
        th2.join()
        th3.join()


if __name__ == "__main__":
    p = LisTLLProtocol()
    p.LIS_boot()
