# coding=utf-8
"""
    file name: score.py
    effect: 显示涂鸦跳跃的得分
"""
import pygame.font

'''
    class name: Score
    effect: 涂鸦得分的类
'''


class Score:
    """构造函数"""

    def __init__(self, screen, stats, ai_settings):

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.ai_settings = ai_settings

        # 显示得分的字体参数
        self.text_color = (30, 30, 30)  # 颜色
        self.font = pygame.font.SysFont(None, 44)  # 字体

        # 初始化得分
        self.initScore()

    '''得分字符串转化为图像函数'''

    def initScore(self):
        # 提取得分字符串
        score_string = str(self.stats.score)
        self.score_image = self.font.render(score_string,
                                            True,
                                            self.text_color,
                                            self.ai_settings.background_color)

        # 得分显示在左上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.score_rect.right + 10
        self.score_rect.top = 20

    '''显示得分函数'''

    def showScore(self):
        self.screen.blit(self.score_image, self.score_rect)
        # print("show score")
