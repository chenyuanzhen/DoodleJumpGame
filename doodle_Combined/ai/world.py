"""
    file name: world.py
    effect: 构建游戏各种元素
"""

import random
from pygame import Rect
from . import block
from . import bonus
# from . import settings
from settings import *


class World:
    def __init__(self, startX, startY, colors, colorsBonus):

        # 普通踏板的长度、宽度、颜色
        self.widthPlatform = 80
        self.heightPlatform = 10
        self.colorPlatforms = colors

        # 弹簧长宽、颜色
        self.widthBonus = 12
        self.heightBonus = 12
        self.colorsBonus = colorsBonus
        # 弹簧可能性
        self.bonusSpawnChance = 10
        self.platformChanceBroken = 10

        self.minY = self.heightPlatform + 30
        self.maxY = 100
        self.startX, self.startY = startX, startY

        self.platforms = [
            block.Block(startX - 50, startY + 50, self.widthPlatform, self.heightPlatform, self.colorPlatforms[0])]
        self.bonuses = []

    # 更新函数
    def update(self, camera):

        # 更新踏板 and bonuses arrays
        for p in self.platforms:
            if camera.apply(p).y > AIYWIN or camera.apply(p).y < -400:
                self.platforms.remove(p)

        for b in self.bonuses:
            if camera.apply(b).y > AIYWIN or camera.apply(b).y < -400:
                self.bonuses.remove(b)

        self.generate(camera)

    # 生成踏板
    def generate(self, camera):
        if len(self.platforms) > 0:
            #  --generating all platform settings--

            # 选择x和y坐标
            x = random.randint(0, AIXWIN - self.widthPlatform)
            y = self.platforms[-1].rect.y - random.randint(self.minY, self.maxY)

            for i in range(len(self.platforms)):
                if i > 0 and self.platforms[-i].canJump:
                    y = self.platforms[-i].rect.y - random.randint(self.minY, self.maxY)
                    if y + self.heightPlatform < camera.apply(self.platforms[-1]).y \
                            or y > self.heightPlatform + camera.apply(self.platforms[-1]).y:
                        break
                    else:
                        y -= self.heightPlatform * 2
                        break
            # futur platform rect
            rect = Rect(x, y, self.widthPlatform, self.heightPlatform)

            # 随机生成踏板类型
            breack = random.randint(0, self.platformChanceBroken)
            randomBonus = random.randint(0, self.bonusSpawnChance)
            randomCanJump = random.randint(0, 6)

            breakable = False
            haveBonus = False
            canJump = True

            color = self.colorPlatforms[0]

            # can't jump on it
            if randomCanJump == 1 and self.platforms[-1].canJump:
                canJump = False
                color = self.colorPlatforms[2]
                breakable = True
            # can jump on it but destroy after collision
            elif breack == 1:
                color = self.colorPlatforms[1]
                breakable = True
            # have a bonus on it
            if randomBonus == 1 and breakable is False:
                haveBonus = True

            # create platform
            if camera.apply_rect(rect).y > -400:
                # 添加踏板
                self.platforms.append(block.Block(x, y, self.widthPlatform, self.heightPlatform, color, breakable, canJump))

                if haveBonus:
                    x = self.platforms[-1].rect.x + random.randint(0, self.widthPlatform - self.widthBonus)
                    y = self.platforms[-1].rect.y - self.heightBonus
                    self.bonuses.append(bonus.Bonus(x, y, self.widthBonus, self.heightBonus, 40, self.colorsBonus[0]))

        else:
            self.platforms = [bonus.Bonus(self.startX - 50,
                                    self.startY + 50,
                                    self.widthPlatform,
                                    self.heightPlatform,
                                    self.colorPlatforms[0])]
