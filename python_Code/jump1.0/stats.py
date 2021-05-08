# coding=utf-8
"""
    file name: stats.py
    effect: 构建检测游戏状态信息的类
"""

'''
    class name: Stats
    effect: 显示游戏状态信息的类
'''
class Stats():
    """构造函数"""
    def __init__(self):
        # 游戏刚开始时为活动状态
        self.is_game_active = True
        # 初始化得分为0
        self.score = 0
