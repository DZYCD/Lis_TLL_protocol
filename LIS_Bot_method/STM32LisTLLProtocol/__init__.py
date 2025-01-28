#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2025 - 2025 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2025/1/21 下午9:54
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py
# @IDE     : PyCharm
import sys
import urequests
import ujson
import os
import time
from umqtt.simple import MQTTClient
import random
import _thread
import network
import LED
import io

class ERRINFO(io.IOBase):
    def __init__(self):
        self.info=''
        self.err_line=''
        self.linemark=False
    def write(self,t):
        s=t.decode()
        if s!='\n':
            if self.linemark:
                self.err_line=s
                self.linemark=False
            self.info+=s
            if s=='", line ':
                self.linemark=True

tb=ERRINFO()

def waiting_msg(socket, wifi):
    while True:
        time.sleep(0.1)
        try:
            wifi.wifi_check()
            socket.check_msg()
        except Exception as e:
            return

def get_time():
    t = time.localtime()
    return '当前时间是：{}年{}月{}日 {}:{}:{}'.format(t[0], t[1], t[2], t[3], t[4], t[5])


class Logger:
    def __init__(self, name, log):
        self.name = name
        self.log = log
        self.debug = False

    def logger(self, msg, _type="INFO"):
        now_time = get_time()
        with open(self.log, "a") as f:
            if _type == "INFO":
                # print("%s [%s]>>> \033[0;36;40mINFO: %s\033[0m" % (self.name, now_time, msg))
                f.write("%s [%s]>>> INFO: %s" % (self.name, now_time, msg) + "\n")
            if _type == "SUCCESS":
                # print("%s [%s]>>> \033[0;32;40mSUCCESS: %s\033[0m" % (self.name, now_time, msg))
                f.write("%s [%s]>>> SUCCESS: %s" % (self.name, now_time, msg) + "\n")
            if _type == "ERROR":
                # print("%s [%s]>>> \033[0;31;40mERROR: %s\033[0m" % (self.name, now_time, msg))
                f.write("%s [%s]>>> ERROR: %s" % (self.name, now_time, msg) + "\n")
            if _type == "WARNING":
                # print("%s [%s]>>> \033[0;33;40mWARNING: %s\033[0m" % (self.name, now_time, msg))
                f.write("%s [%s]>>> WARNING: %s" % (self.name, now_time, msg) + "\n")
            if _type == "SEND":
                # print("%s [%s]>>> \033[0;34;40mSEND: %s\033[0m" % (self.name, now_time, msg))
                f.write("%s [%s]>>> SEND: %s" % (self.name, now_time, msg) + "\n")
            if _type == "RECEIVE":
                # print("%s [%s]>>> \033[0;35;40mRECEIVE: %s\033[0m" % (self.name, now_time, msg))
                f.write("%s [%s]>>> RECEIVE: %s" % (self.name, now_time, msg) + "\n")
            if _type == "OUTPUT":
                # print("%s [%s]>>> \033[1;33;40mOUTPUT: \033[1;33;47m %s\033[0m" % (self.name, now_time, msg))
                f.write("%s [%s]>>> OUTPUT: %s" % (self.name, now_time, msg) + "\n")
            if _type == "DEBUG" and self.debug:
                # print("%s [%s]>>> \033[1;33;40mDEBUG: \033[1;33 %s\033[0m" % (self.name, now_time, msg))
                f.write("%s [%s]>>> DEBUG: %s" % (self.name, now_time, msg) + "\n")


# 发声核心 VoiceCore
class VoiceCore:
    def __init__(self):
        self.APP_ID = '115492263'
        self.API_KEY = 'u1a96y2boaTyBbyNdsCkTkYG'
        self.SECRET_KEY = 'aBwbwemTArHXrOKUkzK0ZXdyIARWBpg5'
        self.file_path = "./chat-audio.mp3"
        self.speak_path = "./res-audio.mp3"
        # self.pygame = pygame

    def Read_msg(self, msg):
        client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        s = msg
        result = client.synthesis(s, 'zh', 1, {  # zh代表中文
            'vol': 5, 'per': 111
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
        mindb = 6000  # 最小声音，大于则开始录音，否则结束
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
                try:
                    self.pygame.mixer.music.unload()
                    self.pygame.mixer.music.stop()
                except:
                    pass
                # print("开始录音>>>", end="")
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
        # print("录音结束>>>", end="")

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
            f = open(file_name, mode="w")  # 音频-图片-视频  mode="wb"
            f.close()

        except FileNotFoundError:
            # print("%s not found" % file_name)
            pass

    def Run_Talk(self):
        while True:

            self.record_sound()

            chat_message = self.voice2text()

            self.del_file()
            if len(chat_message) > 0:
                return chat_message[0]


# 语言核心Linguistic_core
class LinguisticCore:
    def __init__(self):
        self.name = ""
        self.user = ""
        self.profile = """"""
        self.setting = """
            规则和指令：
        """
        self.example = """
            下面是一组对话例子。在这里，你将扮演%s。
            """ % self.name
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
        self.first = """
                下面是对话背景：
        """
        self.tools = []
        self.tool_choice = "auto"
        self.tool = None
        self.msg = None
        self.add_msg = ""
        self.temperature = 1
        self.log = None

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

    def func_call(self, msg):
        arguments = ujson.loads(msg.__function.arguments)
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
        messages = []
        if mode == "chat":
            self.tool_choice = "none"
            self.temperature = 1.3
            msg = self.user + ':' + msg
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

        self.log.logger("post " + str(messages), "DEBUG")

        response = urequests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer sk-5f2408afd34841989715327ef90626cb'
            },
            data=ujson.dumps({
                'model': 'deepseek-chat',
                "messages": messages,
                'stream': False,
                'temperature': self.temperature,
                'tools': self.tools,
                'tool_choice': self.tool_choice
            }).encode('utf8')
        )
        p = response.json()
        token = p['usage']['total_tokens']
        message = p['choices'][0]['message']['content']
        if mode == "chat":
            self.history_list.append(msg)
            self.history_list.append(message)
            if token > 2400:
                self.round = self.round // 2 - (self.round % 2)
            else:
                self.round = self.round + 2
            while len(self.history_list) > self.round:
                del self.history_list[0]
            return message
        if mode == "solo":
            return message
        if mode == "tool":
            self.log.logger(str(p), "DEBUG")
            p = p['choices'][0]['message']['tool_calls'][0]['function']
            arguments = ujson.loads(p['arguments'])
            fuc = p['name']
            fuc += '('
            for i in arguments:
                fuc += str(arguments[i]) + ','
            fuc += ')'
            return fuc.replace(',)', ')')


class WiFiCore:
    def __init__(self):
        self.name = 'TP-LINK_HyFi_50'
        self.password = 'woailaopo'
        self.log = None
        self.sta_if = network.WLAN(network.STA_IF)


    def wifi_check(self):
        self.sta_if.active(True)
        while not self.sta_if.isconnected():
            self.log.logger("WIFI disconnected, relink_wifi...", "WARNING")
            try:
                self.sta_if.reconnect()
            except:
                time.sleep(1)
        self.log.logger(" WIFI CONNECTED!" + str(self.sta_if.ifconfig()), "SUCCESS")


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
        self.log_pos = 'output_log.txt'
        self.log = None
        self.debug = False  # Debug模式开关

        # 将所有函数注册进入
        self.translate = []  # 详见 deepseek 的 tools_function 注册方法
        self.command_list = {}
        self.permission_list = {}

        # 设置输入和输出的语音权限
        self.listen_access = False
        self.speak_access = False
        self.spare_access = False

        # api方法设置
        self.front_linguistic_mode = False  # 直接控制开关
        self.llm_linguistic_mode = False  # 模型控制开关
        self.voice_filter = False  # 碎片输入过滤开关
        self.command_arg = False  # 提示词通行开关

        self.Linguistic = LinguisticCore()
        self.wk = VoiceCore()
        self.wifi = WiFiCore()
        self.__function = ["用自己的语言陈述下面的处理结果:", "", "，不要带有多余的内容"]
        self.status = "finish"
        self.socket = None
        self.process_check = {}
        self.run_time = 0
        self.free_time = time.time()+946656000
        self.spare_time_limit = 300
        self.history_list = []
        self.round = 0
        self.access_list = {"SaYi_SV": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8040,
                "introduce": "所有家庭机器人的中枢。"}}  # 预留一个默认值

        self.th1 = None
        self.th2 = None
        self.th3 = None

    def ping(self, msg):
        msg = str(self.translate) + '|||' + str(self.permission_list)
        return msg.replace(' ', '')

    def on_message(self, topic, msg):
        data = msg.decode()
        topic = topic.decode()
        self.log.logger(data, "DEBUG")
        if topic == self.name + str(self.tsk_port):
            self.TSK_message(data)
        if topic == self.name + str(self.tll_port):
            self.TLL_message(data)
        if topic == self.name + str(self.nlp_port):
            self.NLP_message(data)

    def run(self):
        self.log.logger("creating basic client...", "DEBUG")
        client = MQTTClient(self.name + str(random.randint(1, 10000)), self.cyber_pos, self.cyber_port, self.name,
                            '123')
        client.set_callback(self.on_message)
        client.connect()
        self.log.logger("creating Finished!", "DEBUG")
        return client

    def publish(self, socket, topic, msg):
        self.wifi.wifi_check()
        socket.publish(topic, msg, qos=1)

    def request(self, command, name, function):
        pos, port = name, str(self.access_list[name]["tll_port"])
        text = "%s %s %s %s %s %s+%s+%s" % (
            self.name, command, name, function, str(time.time() + 946656000), self.cyber_pos, str(self.tll_port),
            self.real_pos)
        self.log.logger("send to topic[%s%s] :%s" % (pos, port, text), "SEND")
        if self.access_list[name]["cyber_pos"] == self.cyber_pos:
            self.publish(self.socket, pos + port, text.encode("utf-8"))
        else:
            k = self.access_list[name]["cyber_pos"]
            self.log.logger("%s is not at the default server, creating new socket..." % k, "WARNING")
            _socket = MQTTClient(self.name + str(random.randint(1, 10000)), k, self.cyber_port, self.name, '123')
            _socket.connect()
            self.publish(_socket, pos + port, text.encode("utf-8"))
            _socket.disconnect()

    def random_voice(self):
        random_message = ["给我讲个童话故事的片段来引起我的注意", "给我讲个网上的新闻来引起我的注意",
                          "给我讲个笑话来引起我的注意",
                          "想象一下未来的人的生活", "详细描述一个全球历史中发生的事情", "对我刚刚说的事情提问",
                          "你已经发现自己被闲置很长时间了，说点话来引起我的注意",
                          "你已经被闲置好久了，表达一下自己的无聊来引起我的注意"]
        while self.spare_access:
            if time.time()+946656000 - self.free_time > self.spare_time_limit:
                self.free_time = time.time()+946656000
                self.tell_to_TSK("speak" + self.Linguistic.process(random.choice(random_message), 'solo'))

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
        msg = "%s 说 %s" % (bot_name, arg)
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
                    "content": """#### 定位
                            - 智能助手
                             - 名称 ：文本分类specialist
                             - 主要任务 ：
                             下面对输入的文本文字进行自动分类，识别其所指示的机器人名称和对他的命令。机器人的名称见"文本种类。

                             #### 能力
                             - 分类识别 ：根据分析结果，将文本分类到预定义的机器人名字中。

                             #### 知识储备
                             - 文本种类 ：
                             %s

                             #### 使用说明
                             - 输入 ：一段文本。
                             - 输出 ：只输出机器人的名称和对他的命令。以【机器人的名称】+【对他的命令】格式返回，不需要额外解释。""" % self.introduce()
                    }, {"role": 'user', 'content': msg}]

        a = self.Linguistic.process(message, "solo")

        p = a.replace("【", "").replace("】", "")
        botname, command = p.split('+')

        return "%s tips %s send(%s,%s) %s %s+%s+%s" % (
            self.name, self.name, botname, command, str(time.time() + 946656000), self.cyber_pos, str(self.tll_port),
            self.real_pos)

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
            self.log.logger(a, "SUCCESS")
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
        self.publish(self.socket, self.name + str(self.nlp_port), msg.encode("utf-8"))



    def tell_to_TSK(self, msg):
        self.publish(self.socket, self.name + str(self.tsk_port), msg.encode("utf-8"))



    def get_function(self, msg):
        return self.Linguistic.process(msg, "tool", self.translate)

    # 上传给自己的TLL端口
    def tell_to_TLL(self, msg):
        bot_name, command, target_name, func, times, place = msg.split(" ")
        if func.split('(')[0] == 'dec_':
            func = self.get_function(func[5:-1])

        msg = "process%s %s %s %s %s %s" % (bot_name, command, target_name, func, times, place)
        # print(self.tll_port)
        self.publish(self.socket, self.name + str(self.tll_port), msg.encode("utf-8"))



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
                    self.log.logger("TLL分析失败，转为Natual解释...", "WARNING")
                    receiver = 'Natual'
            if receiver == "Natual":
                msg = self.get_process(msg, 1)
                if "【发送通知】" in msg and self.llm_linguistic_mode:
                    ans = msg.split("【发送通知】")[1]
                    self.log.logger("机器人触发TLL标签：%s" % ans)
                    try:
                        self.tell_to_TLL(self.Natual_to_TLL(ans))
                    except:
                        self.log.logger("TLL转写失败。转为Natual", "WARNING")
                msg = msg.replace("【发送通知】", "")
                return self.tell_to_Natual(msg)

    def send(self, args):
        target, function = args
        self.request("tips", target, "dec_(%s)" % function)

    def nlp_check(self, msg):
        self.publish(self.socket, self.name + str(self.nlp_port), msg.encode("utf-8"))


    def access_update(self, arg):
        self.access_list = ujson.loads(arg.replace("'", '"'))

    def write(self, key, arg, form):
        with open(os.getcwd() + '/' + self.name + self.log, 'r') as f:
            msg = f.read()
            p = ujson.loads(msg)
            if form == 'cover':  # 直接覆盖
                p['data'][key] = arg
            if form == 'add':  # 追加
                p['data'][key].append(arg)
        with open(os.getcwd() + '/' + self.name + self.log, 'w') as f:
            f.write(ujson.dumps(p))

    def Natual(self, arg):
        pass

    def give_output(self, arg):
        self.nlp_check(arg[0])

    def get_msg(self, key=None, arg=None):
        with open(os.getcwd() + '/' + self.name + self.log, 'r') as f:
            msg = f.read()
            p = ujson.loads(msg)
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
                    self.request("cons", ans, "200(%s回答%s)" % (bot_name, func))
                return "200"

            bot_name, command, target_name, func, times, place = msg.split(" ")

            if float(times) < self.run_time:
                pass
                # return "cons %s 402(Arrived_too_late)" % bot_name

            self.run_time = float(times)

            if target_name != self.name:
                return "cons %s 405(Wrong_target)" % bot_name

            if bot_name not in self.access_list.keys():
                # self.request("tips", "SaYi_SV", "get(access_list)")
                return "400"
            body, args = func.split("(")
            if body == "access_update" and bot_name == "SaYi_SV":
                self.access_update(args[0:-1])
                return "cons %s 201(%s)" % (bot_name, msg) if command == 'tips' else "cons %s 201(Success)" % bot_name

            if body not in self.command_list.keys():
                return "cons %s 404(No_function)" % bot_name
            try:
                permission = self.permission_list[body].split(",")
                for i in permission:
                    name, arg = i.split("=")
                    if "level" == name and int(arg) != self.access_list[bot_name]["level"]:
                        return "cons %s 403(No_access)" % bot_name
                    if "name" == name and arg != "DzyCd" and arg != bot_name and not (
                            arg == "self" and bot_name == self.name):
                        return "cons %s 403(No_access)" % bot_name
            except:
                self.log.logger("%s方法没有设定权限表，跳过权限认证。 建议在permission_list设定权限" % body, "WARNING")
                pass

        except Exception as e:
            sys.print_exception(e)
            self.log.logger("[!]From TLL:%s" % e, "ERROR")
            return "101"

        try:
            arg_list = args[0:-1].strip(" ").split(",")
            # print(arg_list)
            msg = self.command_list[body](arg_list)
            if msg is None:
                return "cons %s 201(%s)" % (bot_name, msg) if command == 'tips' else "cons %s 201(Success)" % bot_name
            if msg == "200" or msg == "400":
                return msg
            if len(msg) > 3 and msg[0:4] == "203+":
                self.process_check[msg[4:]] = bot_name
                return "203"
            if len(msg) > 3 and msg[0:4] == "202+":
                command, function = msg[4:].split("+")
                function = function.replace(" ", "")
                return "%s %s %s" % (command, bot_name, function)
            if msg == "406":
                return "cons %s 406(Target_business)" % bot_name
            if msg == "503":
                return "cons %s 503(System_error)" % bot_name

            return "cons %s 201(%s)" % (bot_name, msg) if command == 'tips' else "cons %s 201(Success)" % bot_name
        except Exception as e:
            sys.print_exception(e)
            self.log.logger("[!]From TLL:%s" % e, "ERROR")
            return "407"

    def TSK_message(self, data):
        if len(data):
            try:
                # print("get:" + data)
                if data[0:5] == "speak":
                    data = data[5:]
                    if self.speak_access:
                        self.wk.Read_msg(data)
                    self.log.logger(f'{data}', "OUTPUT")

            except Exception as e:
                sys.print_exception(e)
                self.log.logger("[!]From TSK:%s" % e, "ERROR")

    def NLP_message(self, data):
        if len(data):
            try:
                self.free_time = time.time()+946656000
                ans = self.NLP_decode(data)
                if ans is not None:
                    self.tell_to_TSK("speak" + ans)
            except Exception as e:
                sys.print_exception(e)
                self.log.logger("[!]From NLP:%s" % e, "ERROR")

    def user_input(self):
        self.log.logger(
            "\033[0;32m[->] TSK启用录音功能\033[0m" if self.listen_access else "\033[0;31m[->] TSK禁用录音功能\033[0m")
        self.log.logger(
            "\033[0;32m[->] TSK启用语音功能\033[0m" if self.speak_access else "\033[0;31m[->] TSK禁用语音功能\033[0m")

        while True:
            flag = "Yes"
            try:
                if self.listen_access:
                    name = self.wk.Run_Talk()
                    message = [{"role": "system",
                                "content": """#### 定位
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
                    else:
                        flag = 'YES'
                    self.logger("From Filter: " + flag, "INFO")
                else:
                    name = input()

                if name[0:3] == "TLL":
                    command, target, function = name[4:].split(' ')
                    self.request(command, target, function)
                else:
                    if flag == "YES" and self.command_arg:
                        for i in self.access_list:
                            for k in self.access_list[i]['command']:
                                if len(k) <= len(name) and k == name[:len(k)]:
                                    flag = 'NO'
                                    self.logger("From Command: " + k, "INFO")
                                    self.request('tips', i, self.access_list[i]['command'][k] + '(' + name[len(k):] + ')')
                    if flag == "YES":
                        self.tell_to_NLP(name)
            except Exception as e:
                self.logger(f"[!]From TSK:{e}", "ERROR")

    def TLL_message(self, data):
        if len(data):
            try:
                if data[0:7] != "process":
                    self.log.logger("\033[0;32;40m >>>from %s\033[0m" % data, "RECEIVE")
                    self.nlp_check(data)
                else:
                    data = data[7:]
                    self.log.logger("\033[0;32;40m >>>process %s\033[0m" % data, "RECEIVE")
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
                        self.nlp_check("finish%s" % data)
                    else:
                        command, name, function = ans.split(" ")
                        self.request(command, name, function)
            except Exception as e:
                sys.print_exception(e)
                self.log.logger("[!]From TLL:%s" % e, "ERROR")

    def connect_SaYi_SV(self):
        LED.reset()
        try:
            self.log.logger("Connecting To SaYi_SV...", "INFO")
            self.request("tips", "SaYi_SV", "get(access_list)")
        except Exception as e:
            self.log.logger("SaYi_SV Not Found：%s" % str(sys.print_exception(e)), "ERROR")
        LED.reset()

    def LIS_boot(self):
        info = """
        ___THE %s INFORMATION ___
        START TIME: %s
        WIFI : %s
        CORRENSPONDENCE : MQTT over TCP
        URL : %s PORT : %s
        TLL : OPEN IN %s, Mqtt_Topic = %s
        NLP : OPEN IN %s, Mqtt_Topic = %s
        TSK : OPEN IN %s, Mqtt_Topic = %s
        CYBER_POS : %s
        REAL_POS : %s
        USER : %s
        OutPutLog : %s
        DEBUG mode : %s

        Please check dynamic output by open the logfile.

        Copyright ©2021-2025 ISOM Corporation, All Rights Reserved.
        The LIS series robots are owned by ISOM Corporation. May not be reproduced or quoted without permission
        """ % (self.name, get_time(), self.wifi.name, self.cyber_pos, str(self.cyber_port),
               str(self.tll_port), self.name + str(self.tll_port), str(self.nlp_port), self.name + str(self.nlp_port),
               str(self.tsk_port), self.name + str(self.tsk_port),
               self.cyber_pos, self.real_pos, self.user, self.log_pos, str(self.debug))

        print(info)
        self.log = Logger(self.name, self.log_pos)
        self.log.debug = self.debug
        self.wifi.log = self.log
        self.Linguistic.log = self.log
        self.log.logger(info)
        while True:
            self.log.logger(self.name + ": Subscribing...", "INFO")
            self.wifi.wifi_check()
            self.socket = self.run()

            self.socket.subscribe(self.name + str(self.tll_port))
            self.log.logger(self.name + ": TLL open in topic[%s]" % (self.name + str(self.tll_port)), "SUCCESS")

            self.socket.subscribe(self.name + str(self.nlp_port))
            self.log.logger(self.name + ": NLP open in topic[%s]" % (self.name + str(self.nlp_port)), "SUCCESS")

            self.socket.subscribe(self.name + str(self.tsk_port))
            self.log.logger(self.name + ": TSK open in topic[%s]" % (self.name + str(self.tsk_port)), "SUCCESS")

            self.connect_SaYi_SV()
            print("Running...")
            # _thread.start_new_thread(self.user_input, ())
            waiting_msg(self.socket, self.wifi)
            self.log.logger(self.name + ": socket error,reconnecting...", "WARNING")
            print("error,RE Running...")
            time.sleep(1)


if __name__ == "__main__":
    p = LisTLLProtocol()
    p.LIS_boot()






