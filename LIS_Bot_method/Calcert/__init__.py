#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/26 上午11:22
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm

class Calcert:
    def __init__(self):
        super().__init__()
        self.TLL = None
        self.TSK = None
        self.NLP = None
        self.name = None
        self.cyber_pos = None
        self.real_pos = None
        self.tsk_port = None
        self.tll_port = None
        self.nlp_port = None

    def pack_up(self, NAME):
        NAME.name = self.name
        NAME.cyber_pos = self.cyber_pos
        NAME.real_pos = self.real_pos
        NAME.tsk_port = self.tsk_port
        NAME.tll_port = self.tll_port
        NAME.nlp_port = self.nlp_port

    def boot(self):
        self.pack_up(self.TLL)
        self.pack_up(self.TSK)
        self.pack_up(self.NLP)
        self.TSK.TLL = self.TLL
        self.TSK.NLP = self.NLP

        from threading import Thread
        th1 = Thread(target=self.TLL.NLP_boot)
        th2 = Thread(target=self.NLP.NLP_boot)
        th3 = Thread(target=self.TSK.NLP_boot)

        th1.start()
        th2.start()
        th3.start()

        th1.join()
        th2.join()
        th3.join()
