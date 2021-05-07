# coding=utf-8
"""
    file name: end.py
    effect: 构建游戏结束的类，
            显示游戏结束时的画面
"""
import pygame.font

'''
    class name: GameEnd
    effect: 游戏结束时的类
'''


class GameEnd:
    """构造函数"""

    def __init__(self, screen, message):

        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 结束界面初始化
        self.height = 50
        self.width = 200
        self.over_color = (54, 140, 217)
        self.text_color = (255, 255, 25)
        self.font = pygame.font.SysFont(None, 48)

        # 创造界面，使其居中
        self.rect = pygame.Rect(0, 0,
                                self.width,
                                self.height)
        self.rect.center = self.screen_rect.center

        self.initMessage(message)

    '''结束信息转化为图像函数'''

    def initMessage(self, message):
        self.message_images = self.font.render(message,
                                               True,
                                               self.text_color,
                                               self.over_color)
        self.message_images_rect = self.message_images.get_rect()
        # 将图像放置在中间
        self.message_images_rect.center = self.rect.center

    '''显示结束函数'''

    def showEnd(self):
        self.screen.fill(self.over_color, self.rect)
        self.screen.blit(self.message_images,
                         self.message_images_rect)
