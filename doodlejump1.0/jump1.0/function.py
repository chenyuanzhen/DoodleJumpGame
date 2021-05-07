# coding=utf-8
"""
    file name: function.py
    effect: 游戏运行时的相关函数
"""

import sys
import pygame
from pedal import Pedal
import random

'''
    function name: checkEvents
    effect: 检测键盘与鼠标事件并对涂鸦做出相应动作
'''


def checkEvents(graffiti):
    for event in pygame.event.get():
        # 按键事件为退出
        if event.type == pygame.QUIT:
            sys.exit()

        # 按键事件为按下按键
        elif event.type == pygame.KEYDOWN:
            checkKeyboardDown(event, graffiti)
        # 按键事件为松开按键
        elif event.type == pygame.KEYUP:
            checkKeyboardUp(event, graffiti)


'''
    function name: checkKeyboardDown
    effect: 对按键按下事件的响应
'''


def checkKeyboardDown(event, graffiti):
    # 按左方向键
    if event.key == pygame.K_LEFT:
        graffiti.moving_left = True
    # 按右方向键
    elif event.key == pygame.K_RIGHT:
        graffiti.moving_right = True


'''
    function name: checkKeyboardUp
    effect: 对按键松开事件的响应
'''


def checkKeyboardUp(event, graffiti):
    # 松开左方向键
    if event.key == pygame.K_LEFT:
        graffiti.moving_left = False
        print("left")
    # 松开右方向键
    elif event.key == pygame.K_RIGHT:
        graffiti.moving_right = False
        print("right")


'''
    function name: updateScreen
    effect: 刷新屏幕
'''


def updateScreen(ai_settings, screen, graffiti, pedals, stats, gameOver, score):
    # 循环重绘屏幕
    screen.fill(ai_settings.background_color)

    # 绘制踏板
    for pedal in pedals.sprites():
        pedal.drawPedal()

    # 绘制涂鸦
    graffiti.setGraffiti()

    # 绘制分数
    score.showScore()

    # 游戏结束情况
    if not stats.is_game_active:
        gameOver.showEnd()

    # 显示屏幕信息
    pygame.display.flip()


'''
    function name: updatePedal
    effect: 随机生成多个踏板
'''


def updatePedal(pedals, ai_settings, screen):
    # 新建基踏板并加入踏板中
    pedal = Pedal(ai_settings, screen)
    pedals.add(pedal)

    # 随机生成
    for num in range(ai_settings.pedal_num):
        pedal = Pedal(ai_settings, screen)

        # 左右随机
        pedal.rect.centerx = random.randint(0, ai_settings.screen_width)

        # 高度保证间隙距离
        pedal.rect.bottom = screen.get_rect().bottom - ai_settings.pedal_gap * num

        pedals.add(pedal)
    # 打印踏板
    print(pedals)


'''
    function name: updatePedals
    effect: 绘制出所有踏板，当涂鸦踏上该踏板后，
            将踏板删除，生成新的踏板
'''


def updatePedals(pedals, ai_settings, screen):
    for pedal in pedals:
        if pedal.rect.bottom > 600:
            # 从列表删除
            pedals.remove(pedal)
            new_pedal = Pedal(ai_settings, screen)
            # 随机生成
            new_pedal.rect.centerx = random.randint(0, ai_settings.screen_width)
            # 设为新的底
            new_pedal.rect.bottom = 0
            pedals.add(new_pedal)
