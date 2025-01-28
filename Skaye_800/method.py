
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/12/8 下午8:01
# @Author  : 单子叶蚕豆_DzyCd
# @File    : Skaye.py
# @IDE     : PyCharm

from ultralytics import YOLO
import cv2 as cv
import os
import time
import socket

model = None
model_list = {
    0: "runs/detect/train4/weights/best.onnx",
    1: "yolov8n.yaml",
    2: "yolov8n.pt"
}


def model_load(name):
    global model
    model = YOLO("yolov8n.yaml")
    print(f"\033[0;33m正在加载模型 >>>{name}\033[0m")
    try:
        model = YOLO(name)
        model = YOLO("runs/detect/train4/weights/best.onnx")
        # model = YOLO("runs/detect/train4/weights/best.onnx")
        print(f"\033[0;32m模型加载成功 >>>{name}\033[0m")
        time.sleep(2)
    except Exception as e:
        print(f"\033[0;31m模型加载失败 >>>{name}\033[0m")
        raise


# Train the model using the 'coco8.yaml' dataset for 3 epochs
# results = model.train(data="E:\\Pycharm_projects\\LIS_BOT\\people_fall.yaml", epochs=10, amp=False)

# Evaluate the model's performance on the validation set
# results = model.val()

# Perform object Skaye_800 on an image using the model
# success = model.export(format="onnx")

act_time = time.time()
client_target = False
client_failed_time = 0
client_failed_count = 0
client = socket.socket()
server_ip = "255.255.255.255"
server_port = 8888

counter = [0, 0, 0]
Skaye_terminate = True

def title():
    print("\033[0;34;40mSkaye_992 天眼机器人 Version past.1\033[0m")
    print(
        '''
ＳＳＳ　　　ｋ　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　ＰＰＰＰ　　　　　　　　　　　　　　　　　　ｔ　　　　　　　　　１
Ｓ　　　Ｓ　　ｋ　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　Ｐ　　　Ｐ　　　　　　　　　　　　　　　　　ｔ　　　　　　　　１１
Ｓ　　　Ｓ　　ｋ　　　ｋ　　ａａａａ　　　ｙ　　　ｙ　　　ｅｅｅ　　　　　　　　　　　　　　　　Ｐ　　　Ｐ　　ａａａａ　　　　ｓｓｓ　　　ｔｔｔｔ　　　　　　　１
　Ｓ　　　　　ｋ　　ｋ　　　　　　　ａ　　ｙ　　　ｙ　　ｅ　　　ｅ　　　　　　　　　　　　　　　Ｐ　　　Ｐ　　　　　　ａ　　ｓ　　　ｓ　　　ｔ　　　　　　　　　１
　　Ｓ　　　　ｋ　ｋ　　　　　　　　ａ　　ｙ　　　ｙ　　ｅ　　　ｅ　　　　　　　　　　　　　　　ＰＰＰＰ　　　　　　　ａ　　ｓ　　　　　　　ｔ　　　　　　　　　１
　　　Ｓ　　　ｋｋ　　　　　　ａａａａ　　　ｙ　ｙ　　　ｅｅｅｅｅ　　　　　　　　　　　　　　　Ｐ　　　　　　　ａａａａ　　　ｓｓｓ　　　　ｔ　　　　　　　　　１
Ｓ　　　Ｓ　　ｋ　ｋ　　　　ａ　　　ａ　　　ｙ　ｙ　　　ｅ　　　　　　　　　　　　　　　　　　　Ｐ　　　　　　ａ　　　ａ　　　　　　ｓ　　　ｔ　　　　　　　　　１
Ｓ　　　Ｓ　　ｋ　　ｋ　　　ａ　　　ａ　　　　ｙ　　　　ｅ　　　ｅ　　　　　　　　　　　　　　　Ｐ　　　　　　ａ　　　ａ　　ｓ　　　ｓ　　　ｔ　　　　　．　　　１
　ＳＳＳ　　　ｋ　　　ｋ　　　ａａａａ　　　　ｙ　　　　　ｅｅｅ　　　　　　　　　　　　　　　　Ｐ　　　　　　　ａａａａ　　　ｓｓｓ　　　　　ｔｔ　　　．　　　１
　　　　　　　　　　　　　　　　　　　　　ｙｙ
    ''')
    print("model :   {}".format("Unknown..." if model == None else model.model_name))
    print("time :   " + str(time.strftime('%Y-%m-%d %H:%M:%S')) + "\t运行时间：   " + time.strftime('%H:%M:%S',
                                                                                                   time.localtime(
                                                                                                       time.time() + 57600 - act_time)))
    print("模型图像处理个数：   " + str(counter[0]) + "\t实例个数：   " + str(counter[1]))
    print("SaYi链接状态：   ", end="")
    print(f"\033[0;30;41m关闭\033[0m" if not client_target else f"\033[0;30;42m开启\033[0m\t 上报量：   " + str(
        counter[2]))
    print("-------------------------------------------------------------------------------")


def connect_to_SaYi(ip, port):
    global client_target, client
    client = socket.socket()

    print(f"\033[0;33m尝试连接到SaYi...({ip}:{port})\033[0m")
    try:
        # 访问服务器的IP和端口
        ip_port = (ip, port)
        # 连接主机
        client.connect(ip_port)
    except socket.error:
        print("\033[0;31mSaYi链接失败\033[0m")
        time.sleep(2)
        return
    client_target = True
    client.send("name".encode())
    print("\033[0;32mSaYi链接成功！中层已接入\033[0m")
    time.sleep(2)


def send_data(msg_input):
    global client, client_target, client_failed_time, client_failed_count
    # 定义发送循环信息
    if client_target:
        try:
            client.send(msg_input.encode())
            counter[2] += 1
            client_failed_count = 0
        except Exception as e:
            print(e)
            client_failed_count += 1
            print("SaYi接收失败！ >>" + str(client_failed_count))
            if client_failed_count > 5:
                client_failed_count = 0
                client_failed_time = time.time()
                client.close()
                client_target = False

    else:
        if time.time() - client_failed_time > 5:
            connect_to_SaYi(server_ip, server_port)
            client_failed_time = time.time()


def input_image():
    lit = 0
    path = input()
    lit += 1
    if path == 'e':
        return
    results = model.predict(
        "E:\\Pycharm_projects\\LIS_BOT\\\datasets\\people_fall\\images\\train\\people({}).jpg".format(lit),
        save=True)
    counter[0] += 1
    final_list = []

    for result in results:
        cap_list, position, name = result.printf()
        for i in range(len(cap_list)):
            counter[1] += 1
            cap = cap_list[i]
            pos = position[i]
            final_list.append([name[int(cap)],
                               [float(pos[0] + pos[2]) / 2, float(pos[1] + pos[3]) / 2]])
        # result.show()
    # Export the model to ONNX format


def cap_capture():
    global Skaye_terminate
    capture = cv.VideoCapture(1)

    while True:
        if Skaye_terminate:
            return
        ret, frame = capture.read()
        if not ret:
            continue
        image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        result = model.predict(image_rgb)[0]
        counter[0] += 1
        cap_list, position, name = result.printf()

        final_list = []
        for i in range(len(cap_list)):
            cap = cap_list[i]
            counter[1] += 1
            pos = position[i]
            final_list.append([name[int(cap)],
                               [float(pos[0] + pos[2]) / 2, float(pos[1] + pos[3]) / 2]])

        os.system('cls')
        title()

        for res in final_list:
            time.sleep(0.05)
            send_data(str(res[0]) + '|' + str(res[1][0]) + '|' + str(res[1][1]) + '|' + str(time.time()))
            print(f"\033[1;31;46m{res}\033[0m")
        if len(final_list) == 0:
            send_data("none|0|0|0")
        result.save("result.png")
        cv.imshow('image', cv.cvtColor(cv.imread("result.png"), cv.COLOR_BGR2RGB))
        if cv.waitKey(1) & 0xFF == ord('q'):
            client.close()
            break


# server_ip = "47.100.11.98"

def switch_port(ip, port):
    global server_ip, server_port
    server_ip, server_port = ip, int(port)


def SV_open_Skaye():
    title()
    # input_image()
    model_load("yolov8n.pt")
    cap_capture()


def menu():
    title()


def Skaye_terminal(arg):
    global Skaye_terminate
    Skaye_terminate = arg