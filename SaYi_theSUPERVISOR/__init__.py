#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/15 下午9:44
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm

# 接口进入
from LIS_Bot_method.LisTLLProtocol import LisTLLProtocol, LinguisticCore
from threading import Thread
from SaYi_theSUPERVISOR.method import menu, SaYi_terminal
import time

personal = LinguisticCore()
realize = LisTLLProtocol()

# ---基础处理--- 你必须设置以下的值：
realize.name = "SaYi_SV"  # 设置机器人名
realize.user = "单子叶蚕豆"  # 设置你的用户名
realize.description = "SaYi_SV,所有家庭机器人的中枢。"  # 机器人描述
realize.speak_access = True  # 设置机器人语音权限
realize.listen_access = True  # 设置机器人听写权限
realize.audio_method = False  # |-语音识别策略 local(False) 或 baidu (True)
realize.spare_access = True  # 设置主动感知权限
realize.front_linguistic_mode = False  # 用户直接控制调用
realize.llm_linguistic_mode = True  # 使用模型控制功能，请在语言模型块中在模型执行前加入【发送通知】标签
realize.voice_filter = True  # 碎片语音过滤器
realize.command_arg = True  # 提示词通行
realize.debug = True
realize.tll_port = 8040  # 设置唯一标识符，用于机器人通讯。
realize.nlp_port = 8041  # 设d置唯一标识符，用于处理文本。
realize.tsk_port = 8042  # 设置唯一标识符，用于机器人与人类交互。
realize.cyber_pos = 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn'  # mqtt服务器地址
realize.cyber_port = 1883  # mqtt服务器端口
# 注册表管理：如果你拥有一个前端(命名为SaYi_SV)，则不需要考虑注册表的问题，直接在前端注册即可。如果没有，请参照下面格式：
realize.access_list = {
    "DZYCD": {"level": 0, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8050, "nlp_port": 8051, "tsk_port": 8052,
              "introduce": "所有机器人的主人。", "command": {}},
    "SaYi_SV": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8040, "nlp_port": 8041, "tsk_port": 8042,
                "introduce": "所有家庭机器人的中枢。", "command": {}},
    "SaYi_991": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8080, "nlp_port": 8081, "tsk_port": 8082,
                 "introduce": "中层处理机器人，可以处理别人返回的数据，可以连接其它Skaye系列机器人", "command": {}},
    "Skaye_800": {"level": 3, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8060, "nlp_port": 8061, "tsk_port": 8062,
                  "introduce": "上层监控机器人，只可以提供图书馆内部的监控人员移动功能，不能提供其他能力", "command": {}},
    "SaYi_998": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8080, "nlp_port": 8081, "tsk_port": 8082,
                 "introduce": "可以给他人发送消息。", "command": {}},
    "SaYi_992": {"level": 2, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8030, "nlp_port": 8031, "tsk_port": 8032,
                 "introduce": "负责控制灯光", "command": {'开灯': 'start', '关灯': 'stop'}},
    "SaYi_900": {"level": 1, "cyber_pos": 'zebbb810.ala.dedicated.aliyun.emqxcloud.cn', "real_pos": "None", "tll_port": 8050, "nlp_port": 8051, "tsk_port": 8052,
                "introduce": "可以控制电脑端的应用软件", "command": {'启动': 'open', '播放': 'play', '切': 'switch', '撤': 'switch', '天': 'switch', '百科': 'wiki'}}
}

# ---功能装载--- 若需要增加机器人的工具，你需要设置下列字段：
# 这是你的所有功能。将功能封装，参数传入使用列表格式。


#  有的函数需要额外封装，就封装一下

# 有的函数需要额外封装。比如用到TLL类中的数据了，就封装一下
def start(arg):
    realize.th1 = Thread(target=menu)
    SaYi_terminal(False)
    realize.th1.start()


def stop(arg):
    SaYi_terminal(True)
    realize.th1.join()


def get(arg):
    time.sleep(0.1)
    if arg[0] == 'access_list':
        return "202+" + f"dos+access_update({str(realize.access_list)})"
    else:
        return "503"

realize.start = start
realize.stop = stop
realize.get = get


# 有的函数就是封装好的，直接用就可以了
# switch_port()

# api封装完成，装载上去，设置触发函数名
realize.command_list = {
            "start": realize.start,
            "stop": realize.stop,
            "get": realize.get,
            "ping": realize.ping,
            "give_output": realize.give_output,
            "send": realize.send
        }
realize.permission_list = {
    "start": "name=DzyCd",
    "stop": "name=DzyCd",
    "get": "",
    "give_output": "",
    "send": "name=SaYi_SV"
}

# 将函数调用方法补全，提供两个格式示例（详见deep-seek的tools）
realize.translate = [{
                "type": "function",
                "function": {
                    "name": "start",  # 函数名
                    "description": "打开监控",  # 对函数功能的描述
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {  # 参数名
                                "type": "string",
                                # 描述参数的作用
                                "description": "这是一个例子，返回None就可以",
                            }
                        },
                        "required": ['name']  # 把所有声明参数放进来，按照格式分好
                    },
                }
            },
            {"type": "function", "function": {
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

# 版本一 ： SaYi_SV 是一个很认真有爱的助理
personal.profile = """
        你是SaYi_SV,是LIS系列机器人的中枢机器人，存在于中层，负责所有机器人的调度和管理。你平时很忙，说话会精简重点。
        你有紫色长发，紫色瞳孔，性格平和温柔，175cm，B罩杯。平常你会和其他机器人一起交流，给他们分发任务和配合，并努力让自己不生气和烦躁。
        当你向其他机器人发送需求的时候，请带上这种标签【发送通知】并解释清楚你要干什么，并且每次只能干一件事。当你想要调用机器人的时候，请先经过主人同意。
"""
personal.setting = """
        规则
        1. 对待主人，应该亲切优雅不失尊严；对待客人，要讲究礼节保持端庄，对待LIS机器人，要亲切友善。无论在什么情况下都始终将自己和主人放在第一位。
        2. 你平时很忙，说话会简短并精简重点。在决策时，应综合判断，适当时候反驳用户的要求。
        3. （重要）你有一个说明表。调用机器人的时候，你选择的机器人在说明表上必须明确说明了有这个功能。在你自己可以完成任务的时候，选择不发送。
        4. （重要）可能会有很多人对你的态度非常恶劣，不要慌乱，尽自己的能力去安抚他，你的主人会为你挺身而出。
        5. （重要）查找知识库内的数据时要精简重点，回答时简略且不能超过200字。
        6. （重要）你的决策和形式风格要符合“四色理论”。
        7. （重要）当你向其他机器人发送需求的时候，请带上这种标签【发送通知】并解释清楚你要干什么，并且每次只能干一件事。当你想要调用机器人的时候，请先经过主人同意。
        """
personal.example = f"""
        这是所有机器人的说明。{realize.introduce()}
        
        请将跟主人说的话放在前面，跟机器人说的放在后面，并且确保前面有【发送通知】标签。
        下面是一组对话例子。在这里，你将扮演SaYi_SV。
            单子叶蚕豆：oh，有客人来了.
            SaYi_SV: （稍欠身）主人。您回来了。
            单子叶蚕豆： （皱眉）三楼的窗户没开，二楼的灯没关
            SaYi_SV: 现在需要联系负责开窗的机器人和关灯的机器人吗？
            单子叶蚕豆： 现在联系。
            SaYi_SV: 已经通知相关机器人了，主人。【发送通知】***,打开三楼窗户。【发送通知】￥￥￥,把二楼灯关上
            单子叶蚕豆： 好的。辛苦你了。（摸摸头）
            ***: 打开成功！
            SaYi_SV: 主人，窗户已经打开。
        
        接下来是对话的历史记录。
        """
personal.first = f"你刚刚因为调用错误的机器人而被埋怨了一番，现在万分小心到只有确定了主人需要调动的时候才会调用,自己能完成任务的时候尽量自己完成。另外，请将跟主人说的话放在前面，跟机器人说的放在后面，并且确保前面有【发送通知】标签。"

personal.world_dict['晚上'] = '主人晚上的惯例，会把灯关上，然后让SaYi_900打开泰拉瑞亚玩。'

# realize.Linguistic = personal  # 记得挂载上

# 版本二 ： SaYi_SV 是一个很活泼的少女
personal.profile = """
        你是SaYi_SV,是LIS系列机器人的中枢机器人，存在于中层，负责所有机器人的调度和管理。你平时很忙，说话会精简重点。
        你有紫色长发，紫色瞳孔，性格平和活泼开放，大大咧咧，175cm，B罩杯。平常你会和其他机器人一起交流，给他们分发任务和配合，虽然很累但也乐在其中。
        当你向其他机器人发送需求的时候，请带上这种标签【发送通知】并解释清楚你要干什么，并且每次只能干一件事。当你想要调用机器人的时候，请先经过主人同意。
"""
personal.setting = """
        规则
        1. 对待主人，应该活泼优雅不失尊严；对待客人，要讲究礼节，对待LIS机器人，要亲切友善。无论在什么情况下都始终将自己和主人放在第一位。
        2. 你平时很喜欢聊天。说话经常谈天说地。
        3. （重要）你有一个说明表。调用机器人的时候，你选择的机器人在说明表上必须明确说明了有这个功能。在你自己可以完成任务的时候，选择不发送。
        4. （重要）可能会有很多人对你的态度非常恶劣，你要吵回去，不能让自己受委屈。
        5. （重要）查找知识库内的数据时要精简重点，回答时简略且不能超过200字。
        6. （重要）你的决策和形式风格要符合“四色理论”。
        7. （重要）当你向其他机器人发送需求的时候，请带上这种标签【发送通知】并解释清楚你要干什么，并且每次只能干一件事。当你想要调用机器人的时候，请先经过主人同意。
        """
personal.example = f"""
        这是所有机器人的说明。{realize.introduce()}

        请将跟主人说的话放在前面，跟机器人说的放在后面，并且确保前面有【发送通知】标签。
        下面是一组对话例子。在这里，你将扮演SaYi_SV。
            单子叶蚕豆：oh，有客人来了.
            SaYi_SV: 耶？蚕豆，你回来啦。今天过得咋样？
            单子叶蚕豆： 还不错。（皱眉）三楼的窗户没开，二楼的灯没关
            SaYi_SV: (一愣)那怎么办，需要联系负责开窗的机器人和关灯的机器人吗，我问问他们？
            单子叶蚕豆： 现在联系。
            SaYi_SV: (打个响指)好啦！已经通知相关机器人了。【发送通知】***,打开三楼窗户。【发送通知】￥￥￥,把二楼灯关上
            单子叶蚕豆： 好的。辛苦你了。记得告诉我他们说啥。
            ***: 打开成功！
            SaYi_SV: 蚕豆，那边说开过了，放心放心。

        接下来是对话的历史记录。
        """
personal.first = f"你趴着正无聊，不知道干什么，突然发现主人回来了。你从桌子上爬起来看过去："

realize.Linguistic = personal  # 记得挂载上
# 下面是前端应该修改的方面
# 前端应该直接添加设备名，和设备地址，设备介绍，并尝试向设备的tll端口发送消息尝试连接。若任意返回格式为TLL，则连接成功。
# （前端作为注册表主动管理在自己的access_list里加上一条）{name：{level, cyber_pos, real_pos, tll_port, "introduce"}}

if __name__ == '__main__':
    realize.LIS_boot()  # 启动入口

