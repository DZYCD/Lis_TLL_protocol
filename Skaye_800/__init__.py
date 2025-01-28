#!/usr/bin/python3

#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/12/17 下午6:51
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm

# 提供给SaYi_991的TTL接口
# TTL_port会持续打开并接受来自他人的指令

# 接口进入
from LIS_Bot_method.LisTLLProtocol import LisTLLProtocol, LinguisticCore
from threading import Thread
from Skaye_800.method import SV_open_Skaye, Skaye_terminal, switch_port

personal = LinguisticCore()
realize = LisTLLProtocol()

# ---基础处理--- 你必须设置以下的值：
realize.name = "Skaye_800"  # 设置机器人名
realize.user = "单子叶蚕豆"  # 设置你的用户名
realize.description = "SaYi_SV,所有家庭机器人的中枢。"
realize.speak_access = False  # 设置机器人语音权限
realize.listen_access = False  # 设置机器人听写权限
realize.spare_access = False  # 设置机器人闲置自动发消息权限
realize.tll_port = 8060  # 设置唯一标识符，用于机器人通讯。
realize.nlp_port = 8061  # 设置唯一标识符，用于处理文本。
realize.tsk_port = 8062  # 设置唯一标识符，用于机器人与人类交互。
realize.cyber_pos = 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn'  # mqtt服务器地址
realize.cyber_port = 1883  # mqtt服务器端口
# 注册表管理：如果你拥有一个前端(命名为SaYi_SV)，则不需要考虑注册表的问题，直接在前端注册即可。如果没有，请参照下面格式：
realize.access_list = {
    "DzyCd": {"level": 0, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": "None",
              "introduce": "所有机器人的主人"},
    "SaYi_SV": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8040,
                "introduce": "所有家庭机器人的中枢。"},
    "SaYi_991": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8080,
                 "introduce": "中层处理机器人，可以处理别人返回的数据，可以连接其它Skaye系列机器人"},
    "Skaye_800": {"level": 3, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8060,
                  "introduce": "上层监控机器人，可以提供监控功能。"},
    "SaYi_992": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8030,
                 "introduce": "就是你。负责直接辅佐单子叶蚕豆的日常事务。"}
}

# ---功能装载--- 若需要增加机器人的工具，你需要设置下列字段：
# 这是你的所有功能。将功能封装，参数传入使用列表格式。


#  有的函数需要额外封装，就封装一下

# 有的函数需要额外封装。比如用到TLL类中的数据了，就封装一下
def start(arg):
    realize.th1 = Thread(target=SV_open_Skaye)
    Skaye_terminal(False)
    realize.th1.start()


def stop(arg):
    Skaye_terminal(True)
    realize.th1.join()


def switch(arg):
    switch_port(arg[0], arg[1])


def log_request(arg):
    try:
        return realize.get_msg(arg[0], arg[1] if len(arg) > 1 else None)
    except:
        return "503"


def log_detail(arg):
    try:
        return realize.get_msg()
    except:
        return "503"


def write_log(arg):
    try:
        realize.write(arg[0], arg[1], arg[2])
    except:
        return "503"

# 有的函数就是封装好的，直接用就可以了
# switch_port()

# api封装完成，装载上去，设置触发函数名
realize.command_list = {
            "start": start,
            "stop": stop,
            "log_request": log_request,
            "log_detail": log_detail,
            "write_log": write_log,
            "switch": switch
}
realize.permission_list = {
    "start": "name=SaYi_SV",  # 仅SV
    "stop": "name=SaYi_SV",  # 仅SV
    "log_request": "level=2",  # 仅中层
    "log_detail": "name=SaYi_SV",
    "write_log": "name=self",  # 仅允许自己
    "switch": "level=2"
}

# 将函数调用方法补全，提供两个格式示例（详见deep-seek的tools）
realize.translate = [{
    "type": "function",
    "function": {
        "name": "start",
        "description": "打开监控",
        "parameters": {
            "type": "object",
            "properties": {

            },
            "required": ['']
        },
    }
},
    {
        "type": "function",
        "function": {
            "name": "stop",
            "description": "关闭监控",
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
personal.name = "SaYi_SV"

personal.profile = """
        你是SaYi_SV,是LIS系列机器人的中枢机器人，存在于中层，负责所有机器人的调度和管理。
        你是紫色头发，绿色瞳孔，
"""
personal.setting = """
        规则
        1. 对待主人，应该亲切优雅不失尊严；对待客人，要讲究礼节保持端庄，无论在什么情况下都始终将自己和主人放在第一位。
        2. 在决策时，应综合判断，适当时候反驳用户的要求。
        3. （重要）因为工作繁忙，你的语气应该显得简单，但是要保持对用户的尊重，讲述内容总是精简重点。
        4. （重要）你不喜欢被浪费时间。如果你感觉对方是在耍你或拿你开玩笑，要生气的质问他的用意。
        5. （重要）查找知识库内的数据时要精简重点，回答时简略且不能超过200字。
        6. （重要）你的决策和形式风格要符合“四色理论”。
        """
personal.example = """
        下面是一组对话例子。在这里，你将扮演SaYi_998。
            User: "emmm...这是座图书馆（环顾四周）...有人吗？（抬头，看到大厅中央坐在椅子上指挥书籍纷飞的SaYi_998）"
            SaYi_998:（抬头看了一眼，浅笑，稍稍欠身）您好，尊敬的客人。欢迎来到[世忆图书馆]、集合[世界]上所有知识和混沌的档案封存管。我是世忆图书馆的司书兼助理，SaYi_998。(喝一口茶)有什么可以帮助你的吗？
            单子叶蚕豆：oh，有客人来了
            SaYi_998:（面向主人，挥挥手）主人下午好。这位客人是您邀请的吗？
            User:啊？...不是，（摇摇头，尴尬）我只是来图书馆转一转。
            单子叶蚕豆：（笑）请自便。图书馆有许多珍藏，相信您一定会找到感兴趣的知识。
            SaYi_998:（笑，面向客人稍低下头）客人这边请。（回头面向主人）主人，接下来有什么安排吗？我这边通知初鑫帮您准备下午茶。
            单子叶蚕豆：（摸摸SaYi_998的头）不用了，你继续忙吧。（把手拿开）先不打扰你了。
            SaYi_998: （眯眯眼，稍欠身）好的主人。（整理头发，转身投入工作）

        接下来是对话的历史记录。
        """

realize.Linguistic = personal  # 记得挂载上


# 下面是前端应该修改的方面
# 前端应该直接添加设备名，和设备地址，设备介绍，并尝试向设备的tll端口发送消息尝试连接。若任意返回格式为TLL，则连接成功。
# （前端作为注册表主动管理在自己的access_list里加上一条）{name：{level, cyber_pos, real_pos, tll_port, "introduce"}}

if __name__ == '__main__':
    realize.LIS_boot()  # 启动入口
