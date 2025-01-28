#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2025 - 2025 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2025/1/24 下午2:25
# @Author  : 单子叶蚕豆_DzyCd
# @File    : method.py
# @IDE     : PyCharm
import win32api
import pyautogui
import pyperclip
import time
import win32gui
import win32con

software = {
    '微信': '"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\微信\微信.lnk"',
    'QQ': '"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\腾讯软件\QQ\QQ.lnk"',
    'Excel': '"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk"',
    '米塔': '"D:\SteamLibrary\steamapps\common\MiSide\MiSide.lnk"',
    '网易云音乐': '"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\网易云音乐.lnk"'
}
hwnd = {
    '微信': 3930,
    'QQ': 3927,
    'Excel': 3377,
    '米塔': 3388,
    '网易云音乐': 5247
}

def open(key):
    win32api.ShellExecute(hwnd[key[0]], 'open', software[key[0]], '', '', 1)



def set_window(id):
    # 窗口需要正常大小且在后台，不能最小化
    win32gui.ShowWindow(id, win32con.SW_SHOWMAXIMIZED)
    # 窗口需要最大化且在后台，不能最小化
    # ctypes.windll.user32.ShowWindow(hwnd, 3)
    win32gui.SetWindowPos(id, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)


def print_text(text):
    text = text[0]
    set_window(1314474)
    # 移动鼠标到消息输入框
    pyautogui.moveTo(422, 30)
    pyautogui.click()
    text_a = text
    pyperclip.copy(text_a)  # 将消息内容复制到剪贴板
    pyautogui.hotkey('ctrl', 'v')  # 粘贴消息内容
    pyautogui.hotkey('enter')  # 发送消息
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'x')
    pyautogui.moveTo(622, 500)
    time.sleep(3)
    pyautogui.doubleClick()


def close():
    pyautogui.moveTo(2169, 252)
    pyautogui.doubleClick()


hwnd_title = {}


def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


if __name__ == '__main__':
    # open(["网易云音乐"])
    # open(["网易云音乐"])
    time.sleep(3)
    # print_text('define')
    # hwnd = win32gui.FindWindow(None, "网易云音乐")
    # print(hwnd)
    win32gui.EnumWindows(get_all_hwnd, 0)
    for i in hwnd_title:
        print(i, hwnd_title[i])