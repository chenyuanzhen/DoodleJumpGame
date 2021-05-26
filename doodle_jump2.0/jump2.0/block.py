"""
    file name: block.py
    effect: 构建踏板类
"""

from pygame.locals import *
from settings import *


class Block(pygame.sprite.Sprite):
    predictScore = 0
    color = None

    def kind(self):
        # kind=0 表示普通平台
        # kind=1 表示只能跳一次的, 然后消失
        # kind=2 表示不能跳
        if self.breakable and self.canJump:
            return 1
        if self.canJump is False:
            return 2
        return 0

    def posX(self):
        return self.rect.left + self.rect.width / 2

    def posY(self):
        return self.rect.top + self.rect.height

    """构造函数"""
    def __init__(self, x, y, w, h, color, breakable=False, canJump=True, *groups):

        super().__init__(*groups)
        self.color = color
        self.image = pygame.Surface((w, h))

        self.breakable = breakable
        self.canJump = canJump
        self.image.fill(color)

        self.rect = Rect(x, y, w, h)

        self.breakable = breakable
        self.canJump = canJump

    def changeColor(self, color):
        self.image.fill(color)
