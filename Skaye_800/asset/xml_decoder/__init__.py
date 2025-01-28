#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/9 下午10:49
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm
import xml.etree.ElementTree as ET
import cv2


class DatasetPre:
    def __init__(self):
        self.root = "E:/Pycharm_projects/LIS_BOT"
        self.target = "people_fall"
        self.arg = "train"
        self.filename = "people(6178)"

    def change(self, name, args):
        self.filename = name
        self.arg = args

    def work(self):
        # 解析XML文件
        # print(self.filename)
        tree = ET.parse("C:/Users/DZYCD/Downloads/Annotations/{}.xml".format(self.filename))
        rt = tree.getroot()
        boxes_list=[]
        try:
            image = cv2.imread("C:/Users/DZYCD/Downloads/JPEGImages/{}.jpg".format(self.filename))
            size = image.shape
            width = size[1]  # 宽度
            height = size[0]  # 高度
        except:
            width = int(rt.find(".//size/width").text) + 1
            height = int(rt.find(".//size/height").text) + 1
        # print(self.filename, height, width)
        for child in rt:
            if child.tag == "object":
                name = child.find('name').text
                for bndbox in child:
                    if bndbox.tag == "bndbox":

                        xmin = int(bndbox.find('xmin').text)
                        ymin = int(bndbox.find('ymin').text)
                        xmax = int(bndbox.find('xmax').text)
                        ymax = int(bndbox.find('ymax').text)

                        # 转换为中心点坐标和宽高
                        x_center = (xmin + xmax) / 2.0
                        y_center = (ymin + ymax) / 2.0
                        w = xmax - xmin
                        h = ymax - ymin

                        # 归一化
                        x = x_center / width
                        y = y_center / height
                        w = w / width
                        h = h / height

                        if min(w, h) > 0.3:
                            continue
                        boxes_list.append("{} {} {} {} {}".format(int(name == 'down'), x, y, w, h))

        with open("{}/datasets/{}/labels/{}/{}.txt".format(self.root, self.target, self.arg, self.filename), "w")as f:
            for l in boxes_list:
                for k in l:
                    f.write(str(k))
                f.write('\n')


import os

paths = 'E:\\Pycharm_projects\\LIS_BOT\\datasets\\people_fall\\images\\train'
tools = DatasetPre()
def traversal_files(path,args):
    dirs = []
    files = []
    for item in os.scandir(path):
        if item.is_dir():
            dirs.append(item.path)

        elif item.is_file():
            name = item.name.split('.jpg')[0]
            tools.change(name, args)
            tools.work()


traversal_files('/\\datasets\\people_fall\\images\\train', 'train')
traversal_files('/\\datasets\\people_fall\\images\\val', 'val')
traversal_files('/\\datasets\\people_fall\\images\\test', 'test')



