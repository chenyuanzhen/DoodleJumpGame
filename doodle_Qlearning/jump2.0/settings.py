"""
    file name: settings.py
    effect: 游戏有关参数，常量的设定
"""

import pygame

# CONST
# 颜色常量
COLORS = [
    pygame.Color(255, 255, 255),  # white 00
    pygame.Color(0, 0, 0),  # black 01
    pygame.Color(255, 0, 0),  # red 02
    pygame.Color(0, 255, 0),  # green 03
    pygame.Color(0, 0, 255),  # blue 04
    pygame.Color(110, 110, 110),  # grey 05
    pygame.Color(182, 210, 45),  # Doddle 06  涂鸦角色颜色（已经贴图无需理会）
    pygame.Color(78, 180, 255),  # blue Sky 07  天蓝
    pygame.Color(50, 50, 50),  # dark grey 08  暗灰
    pygame.Color(120, 120, 120),  # light grey 09  弹簧的颜色
    pygame.Color(131, 252, 107),  # light green 10  一次性踏板的颜色
    pygame.Color(87, 189, 68),  # dark green 11  固定踏板的颜色
    pygame.Color(144, 238, 144),  # 浅绿色 12 陷阱踏板的颜色
    pygame.Color(255, 255, 224),  # rice white 13 游戏背景颜色
]

# 画面常量
XWIN, YWIN = 640, 700  # 窗口大小
HALF_WIDTH = int(XWIN / 2)  # 宽度的中点
HALF_HEIGHT = int(YWIN / 2)  # 高度的中点

DISPLAY = (XWIN, YWIN)  # 窗口
DEPTH = 32  # 深度
FLAGS = 0
CAMERA_SLACK = 30




