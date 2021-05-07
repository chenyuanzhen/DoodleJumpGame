# coding=utf-8
"""
    file name: window.py
    effect: 游戏运行的主循环
"""

import sys
import pygame
from pygame.sprite import Group

import function
from graffiti import Graffiti
from settings import Settings
from end import GameEnd
from score import Score
from stats import Stats

'''
    function name: beginGame
    effect: 创建窗口并刷新
'''


def beginGame():
    # 初始化
    pygame.init()
    ai_settings = Settings()

    # screen为窗口,将其设置为显示
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    # 窗口名
    pygame.display.set_caption("doodle_jump")

    # 新建涂鸦对象
    graffiti = Graffiti(screen, ai_settings)

    # 新建踏板对象
    pedals = Group()
    function.updatePedal(pedals, ai_settings, screen)

    # 新建游戏状态对象
    stats = Stats()

    # 新建游戏结束对象
    gameOver = GameEnd(screen, "Game Over")

    # 新建游戏得分对象
    score = Score(screen, stats, ai_settings)

    # 窗口刷新主循环
    while True:

        # 检测按键
        function.checkEvents(graffiti)

        # 当读取到退出信息时则退出窗口
        if stats.is_game_active:
            # 更新踏板
            function.updatePedals(pedals, ai_settings, screen)
            # 更新涂鸦
            graffiti.updateGraffiti(ai_settings, pedals, stats)
            # 更新得分
            score.initScore()

        # 刷新屏幕
        function.updateScreen(ai_settings, screen,
                              graffiti, pedals,
                              stats, gameOver,
                              score)
