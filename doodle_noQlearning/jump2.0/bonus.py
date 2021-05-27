"""
    file name: bonus.py
    effect: 包含弹簧类的构建
"""

import pygame, sys, os, random
from pygame.locals import *
from settings import *


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, addForce, color, duration=1):
        self.rect = Rect(x, y, w, h)

        self.color = color

        self.image = pygame.Surface((w, h))

        self.image.fill(self.color)

        self.addForce = -addForce
        self.duration = duration
