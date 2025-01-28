#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2025 - 2025 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2025/1/24 下午2:24
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm
#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/12/14 下午8:37
# @Author  : 单子叶蚕豆_DzyCd
# @File    : SaYi.py
# @IDE     : PyCharm

#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/12/17 下午6:51
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm

from LisTLLProtocol import LisTLLProtocol, LinguisticCore
from method import *

personal = LinguisticCore()
realize = LisTLLProtocol()

# ---基础处理--- 你必须设置以下的值：
realize.name = "SaYi_900"  # 设置机器人名
realize.user = "单子叶蚕豆"  # 设置你的用户名
realize.description = "可以控制电脑端的应用软件"
realize.speak_access = False  # 设置机器人语音权限
realize.listen_access = False  # 设置机器人听写权限
realize.spare_access = False  # 设置机器人智能感知权限
realize.tll_port = 8050  # 设置唯一标识符，用于机器人通讯。
realize.nlp_port = 8051  # 设置唯一标识符，用于处理文本。
realize.tsk_port = 8052  # 设置唯一标识符，用于机器人与人类交互。
realize.cyber_pos = 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn'  # mqtt服务器地址
realize.cyber_port = 1883  # mqtt服务器端口
# 注册表管理：如果你拥有一个前端(命名为SaYi_SV)，则不需要考虑注册表的问题，直接在前端注册即可。如果没有，请参照下面格式：
realize.access_list = {
    "SaYi_900": {"level": 1, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8050,
                "introduce": "可以控制电脑端的应用软件"},
    "SaYi_SV": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8040,
                "introduce": "所有家庭机器人的中枢。"}
}

# ---功能装载--- 若需要增加机器人的工具，你需要设置下列字段：
# 这是你的所有功能。将功能封装，参数传入使用列表格式。


#  有的函数需要额外封装，就封装一下

# 有的函数需要额外封装。比如用到TLL类中的数据了，就封装一下

realize.command_list = {
    'open': open,
    'select_music': print_text
}
realize.permission_list = {
    'open': "name=SaYi_SV",
    'select_music': ''
}
realize.translate = [
    {
        "type": "function",
        "function": {
            "name": "open",
            "description": "在应用未打开时打开应用",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": f"可以打开电脑上的应用。可选应用如下{str(software.keys())}",
                    }
                },
                "required": ["name"]
            },
        }
    }, {
        "type": "function",
        "function": {
            "name": 'select_music',
            "description": "在网易云音乐中播放歌曲",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": f"歌曲名",
                    }
                },
                "required": ["name"]
            },
        }
    }
]


# 有的函数就是封装好的，直接用就可以了
# switch_port()

# api封装完成，装载上去，设置触发函数名


# 将函数调用方法补全，提供两个格式示例（详见deep-seek的tools）

# ---人格数据--- 完善下列提示词，使语音助手人格更鲜明。不必须参数，不做解释

personal.user = "单子叶蚕豆"
personal.name = "SaYi_900"


# 下面是前端应该修改的方面
# 前端应该直接添加设备名，和设备地址，设备介绍，并尝试向设备的tll端口发送消息尝试连接。若任意返回格式为TLL，则连接成功。
# （前端作为注册表主动管理在自己的access_list里加上一条）{name：{level, cyber_pos, real_pos, tll_port, "introduce"}}

if __name__ == '__main__':
    realize.LIS_boot()  # 启动入口
