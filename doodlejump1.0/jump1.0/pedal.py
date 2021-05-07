# coding=utf-8
"""
    file name: pedal.py
    effect: 构建踏板类
"""

import pygame
from pygame.sprite import Sprite

'''
    class name: Pedal
    effect: 基于Sprite的踏板类，用于涂鸦进行跳跃
'''
class Pedal(Sprite):
    """构造函数"""
    def __init__(self, ai_settings, screen):

        super().__init__()

        self.screen = screen

        # (0,0)处生成初始踏板
        self.rect = pygame.Rect(0, 0,
                                ai_settings.pedal_width,
                                ai_settings.pedal_height)
        self.rect.centerx = screen.get_rect().centerx
        self.rect.bottom = self.screen.get_rect().bottom
        # 颜色
        self.color = ai_settings.pedal_color

    '''绘制踏板函数(令踏板为椭圆形)'''
    def drawPedal(self):
        pygame.draw.ellipse(self.screen, self.color, self.rect)