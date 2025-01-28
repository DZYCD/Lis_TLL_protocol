#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2025 - 2025 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2025/1/25 下午3:24
# @Author  : 单子叶蚕豆_DzyCd
# @File    : LED.py
# @IDE     : PyCharm
from machine import Pin, PWM
import time

led2 = PWM(Pin(2))
led2.freq(1000)


def breath_LED():1
    for i in range(0, 1024):
        led2.duty(i)
        time.sleep_ms(1)

    for i in range(1023, -1, -1):
        led2.duty(i)
        time.sleep_ms(1)


def light_on(arg):
    led2.duty(1000)


def light_off():
    led2.duty(0)


def reset():
    for i in range(5):
        light_on()
        time.sleep(0.2)
        light_off()
        time.sleep(0.2)

