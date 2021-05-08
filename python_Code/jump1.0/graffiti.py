# coding=utf-8
'''
    file name: graffiti.py
    effect: 创建涂鸦角色类
'''

import pygame
import time

'''
    class name: Graffiti
    effect: 操纵角色的类
'''


class Graffiti():
    '''构造函数'''

    def __init__(self, screen, ai_settings):

        self.screen = screen
        self.ai_settings = ai_settings

        # 读入操纵角色的头像，并调整合适的大小
        self.image = pygame.transform.scale(pygame.image.load("images/role.bmp"), (40, 55))
        # 获取涂鸦的矩形
        self.rect = self.image.get_rect()
        # 获取屏幕的矩形
        self.screen_rect = screen.get_rect()

        # 初始化时将角色放置至屏幕底部中间位置
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom \
                           - ai_settings.pedal_height

        # 将x值转化为浮点数，提高其精确度
        self.center = float(self.rect.centerx)

        # 涂鸦的左右移动标记
        self.moving_left = False
        self.moving_right = False
        # 涂鸦的跳跃标记
        self.moving_top = True
        # 本次跳跃的距离
        self.jump_distance = 0
        # 距离底部距离
        self.bottom_distance = 0

    '''涂鸦定位函数'''

    def setGraffiti(self):
        self.screen.blit(self.image, self.rect)

    '''涂鸦跳跃函数'''

    def jump(self, ai_settings, pedals, stats):
        # 踩到踏板，执行跳跃动作
        if self.moving_top:
            self.jump_distance += ai_settings.graffiti_jump_height
            # 更新底部位置
            self.rect.bottom = self.screen_rect.bottom \
                               - ai_settings.pedal_height \
                               - self.jump_distance \
                               - self.bottom_distance
            # 跳跃动作结束
            if round(self.jump_distance) == ai_settings.pedal_jump_height:
                self.moving_top = False

        # 没踩到踏板
        elif not self.moving_top:
            self.jump_distance -= ai_settings.graffiti_jump_height
            self.rect.bottom = self.screen_rect.bottom \
                               + ai_settings.pedal_height \
                               - self.jump_distance \
                               - self.bottom_distance

            # 调用sprite的碰撞检测方法看是否掉落至屏幕底部
            is_been_hit = pygame.sprite.spritecollideany(self, pedals, False)
            # 踩空了就令
            if is_been_hit:
                if self.rect.bottom == is_been_hit.rect.top + 1:
                    self.jump_distance = 0
                    self.bottom_distance = self.screen_rect.bottom \
                                           - self.rect.bottom
                    self.moving_top = True

                self.movePedalsDown(is_been_hit, pedals, ai_settings, stats)

    '''踏板向下移动,使得涂鸦向上移动'''

    def movePedalsDown(self, is_been_hit, pedals, ai_settings, stats):

        if is_been_hit.rect.bottom < ai_settings.screen_height * 0.8:

            for pedal in pedals:
                pedal.rect.bottom += ai_settings.pedal_jump_height
            # 添加相应分数
            stats.score += ai_settings.pedal_jump_height

    '''更新涂鸦位置函数'''

    def updateGraffiti(self, ai_settings, pedals, stats):

        self.jump(ai_settings, pedals, stats)

        # 按住左方向键时向左移动
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.graffiti_move_speed
        # 按住右方向键时向右移动
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.graffiti_move_speed

        # 当涂鸦移动到边界时，我们要让其在另一边界出现
        # 例：涂鸦在左边界再向左运动时，会出现在右边界

        # 向左移动
        elif self.moving_left and self.rect.left == 0:
            self.center = self.screen_rect.right
        # 向右移动
        elif self.moving_right and self.rect.right == self.screen_rect.right:
            self.center = 0

        # 赋值回去给centerx
        self.rect.centerx = self.center

        if self.rect.top > 600:
            stats.is_game_active = False
