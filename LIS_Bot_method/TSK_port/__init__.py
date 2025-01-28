#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/17 下午6:54
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm
import numpy as np
import os
import time
from aip import AipSpeech
import socket
import pyaudio
import wave
import pygame
from LIS_Bot_method.LLM_model.deepseek_chat import response


class Wake_Up:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY, file_path, speak_path):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.file_path = file_path
        self.speak_path = speak_path
        self.pygame = pygame

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
        mindb = 5000  # 最小声音，大于则开始录音，否则结束
        delayTime = 1.3  # 小声2秒后自动终止
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
            if temp > mindb/2:
                frames.append(data)

            if temp > mindb and not flag:
                flag = True
                try:
                    self.pygame.mixer.music.unload()
                    self.pygame.mixer.music.stop()
                except:
                    pass
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
        # print(ret)
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

            self.record_sound()

            chat_message = self.voice2text()
            print("处理结果>>>", chat_message)

            self.del_file()
            if len(chat_message) > 0:
                return chat_message[0]


class TSK_Port:
    def __init__(self):
        self.TLL = None
        self.NLP = None
        self.name = None
        self.tsk_port = None
        self.cyber_pos = None
        self.APP_ID = '115492263'
        self.API_KEY = 'u1a96y2boaTyBbyNdsCkTkYG'
        self.SECRET_KEY = 'aBwbwemTArHXrOKUkzK0ZXdyIARWBpg5'
        self.file_path = "./chat-audio.mp3"
        self.speak_path = "./res-audio.mp3"
        self.wk = Wake_Up(self.APP_ID, self.API_KEY, self.SECRET_KEY, self.file_path, self.speak_path)
        self.socket = socket.socket()
        self.listen_access = False
        self.speak_access = False
        self.model = response()

    def speak(self):
        while True:
            print(self.name + ": TSK open in ", self.cyber_pos, self.tsk_port)
            self.socket.bind((self.cyber_pos, self.tsk_port))
            self.socket.listen(1)

            while True:
                conn, address = self.socket.accept()
                data: str = conn.recv(8192).decode("UTF-8")
                # print("get message:" + data)
                if len(data):
                    try:
                        # print("get:" + data)
                        if data[0:5] == "speak":
                            data = data[5:]
                            if self.speak_access:
                                self.wk.Read_msg(data)
                            print(f'\033[33m{data}\033[0m')

                    except Exception as e:
                        print(f"\033[0;31m[!]From TSK:{e}\033[0m")
                conn.close()

    def user_input(self):
        with open(self.file_path, 'w'):
            pass
        with open(self.speak_path, 'w'):
            pass

        print("\033[0;32m[->] TSK启用录音功能\033[0m" if self.listen_access else "\033[0;31m[->] TSK禁用录音功能\033[0m")
        print("\033[0;32m[->] TSK启用语音功能\033[0m" if self.speak_access else "\033[0;31m[->] TSK禁用语音功能\033[0m")

        while True:
            flag = "Yes"
            try:
                if self.listen_access:
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
                    flag = self.model.process(message, 'solo')
                    print(flag)
                else:
                    name = input()

                if name[0:3] == "TLL":
                    command, target, function = name[4:].split(' ')
                    self.TLL.request(command, target, function)
                else:
                    if flag == "YES":
                        self.NLP.tell_to_NLP(name)
            except Exception as e:
                print(f"\033[0;31m[!]From TSK:{e}\033[0m")

    def boot(self):
        from threading import Thread
        th2 = Thread(target=self.speak)
        th3 = Thread(target=self.user_input)

        th2.start()
        th3.start()

        th2.join()
        th3.join()
