#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/15 下午9:44
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm


# 下面是家具的后端代码封装使用方面。

from LisTLLProtocol import LisTLLProtocol, LinguisticCore
import LED

personal = LinguisticCore()
realize = LisTLLProtocol()

# ---基础处理--- 你必须设置以下的值：
realize.name = "SaYi_992"  # 设置机器人名
realize.user = "单子叶蚕豆"  # 设置你的用户名
realize.description = "SaYi_992,是TLL协议整合后用的测试bot"
realize.speak_access = False  # 设置机器人语音权限
realize.listen_access = False  # 设置机器人听写权限
realize.spare_access = False  # 设置机器人闲置自动发消息权限
realize.tll_port = 8030  # 设置唯一标识符，用于机器人通讯。
realize.nlp_port = 8031  # 设置唯一标识符，用于处理文本。
realize.tsk_port = 8032  # 设置唯一标识符，用于机器人与人类交互。
realize.cyber_pos = 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn'  # mqtt服务器地址
realize.cyber_port = 1883  # mqtt服务器端口

realize.debug = True
# 注册表管理：如果你拥有一个前端(命名为SaYi_SV)，则只注册SV的位置和自己的权限，并将机器人直接在SV注册即可。如果没有，请参照下面格式：
realize.access_list = {
    "SaYi_SV": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None",
                "tll_port": 8040,
                "introduce": "所有家庭机器人的中枢。"},
    "SaYi_992": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None",
                 "tll_port": 8030,
                 "introduce": "负责控制灯光"}}


# ---功能装载--- 若需要增加机器人的工具，你需要设置下列字段：
# 这是你的所有功能。将功能封装，参数传入使用列表格式。


#  有的函数需要额外封装，就封装一下
def light_on(arg):
    LED.light_on()


def light_off(arg):
    LED.light_off()


def breath(arg):
    LED.breath_LED()


# 有的函数就是封装好的，直接用就可以了
# switch_port()

# api封装完成，装载上去，设置触发函数名
realize.command_list = {
    "start": light_on,
    "stop": light_off,
    "flash": breath,
    "send": realize.send
}

# 将函数的权限挂一下，没有就不填
realize.permission_list = {
    "start": "",  # 仅SV
    "stop": "",  # 仅SV
    "flash": "",
    "log_request": "level=2",  # 仅中层
    "log_detail": "",  # 没有就不填
    "write_log": "name=self"  # 仅允许自己
}

# 将函数调用方法补全，提供两个格式示例（详见deep-seek的tools）
realize.translate = [{
    "type": "function",
    "function": {
        "name": "start",  # 函数名
        "description": "开灯",  # 对函数功能的描述
        "parameters": {
            "type": "object",
            "properties": {
                "name": {  # 参数名
                    "type": "string",
                    # 描述参数的作用
                    "description": f"这是一个例子，返回None就可以",
                }
            },
            "required": ['name']  # 把所有声明参数放进来，按照格式分好
        },
    }
},
    {"type": "function", "function": {
        "name": "stop",
        "description": "关灯",
        "parameters": {
            "type": "object",
            "properties": {
            },
            "required": []
        },
    }
     },
    {"type": "function", "function": {
        "name": "flash",
        "description": "灯光调节",
        "parameters": {
            "type": "object",
            "properties": {
            },
            "required": []
        },
    }
     }
]

# ---人格数据--- 完善下列提示词，使语音助手人格更鲜明。不必须参数，不做解释

personal.user = "单子叶蚕豆"
personal.name = "SaYi_992"

personal.setting = """"""
personal.example = """"""

realize.Linguistic = personal  # 记得挂载上

# 下面是前端应该修改的方面
# 前端应该直接添加设备名，和设备地址，设备介绍，并尝试向设备的tll端口发送消息尝试连接。若任意返回格式为TLL，则连接成功。
# （前端作为注册表主动管理在自己的access_list里加上一条）{name：{level, cyber_pos, real_pos, tll_port, "introduce"}}

if __name__ == '__main__':
    realize.LIS_boot()  # 启动入口



