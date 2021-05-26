"""
    file name: camera.py
    effect: 构建摄像机类，打造画面随着主角移动而移动
"""
from pygame import Rect

from settings import *


class Camera(object):
    def __init__(self, camera_func, width, height, speed):

        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
        self.lerpSpeed = speed

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def apply_rect(self, rect):
        return rect.move(self.state.topleft)

    # 更新函数
    def update(self, target):

        self.lerpSpeed = int(((HALF_HEIGHT - 70) - self.apply(target).y) / 8)

        if self.apply(target).y < HALF_HEIGHT - 70:
            self.state.y += self.lerpSpeed
