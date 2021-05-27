"""
    file name: block.py
    effect: 构建踏板类
"""

from pygame.locals import *
from settings import *


class Block(pygame.sprite.Sprite):

    """构造函数"""
    def __init__(self, x, y, w, h, color, breakable=False, canJump=True, *groups):

        super().__init__(*groups)

        self.image = pygame.Surface((w, h))

        self.image.fill(color)

        self.rect = Rect(x, y, w, h)

        self.breakable = breakable
        self.canJump = canJump

