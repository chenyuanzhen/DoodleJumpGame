# coding=utf-8
"""
    file name: settings.py
    effect: 有关游戏的相关设置
"""

'''
    class name: Settings
    effect: 存储游戏的所有设置的类
'''


class Settings:
    """构造函数"""

    def __init__(self):
        # 屏幕显示参数(宽高以及颜色)
        self.screen_height = 600
        self.screen_width = 400
        self.background_color = (230, 230, 230)

        # 涂鸦左右移动速度参数
        self.graffiti_move_speed = 0.2

        # 踏板参数
        self.pedal_height = 15  # 高度
        self.pedal_width = 70  # 宽度
        self.pedal_color = (110, 182, 22)  # 颜色
        self.pedal_num = 15  # 数量

        # 涂鸦跳起高度速度
        self.graffiti_jump_height = 0.05

        # 踏板的跳起高度
        self.pedal_jump_height = 80
        # 踏板之间的高度间隙
        self.pedal_gap = 45
