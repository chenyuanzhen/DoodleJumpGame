"""
    file name: player.py
    effect: 选手类的构建，即涂鸦
"""

from pygame.locals import *
from settings import *


class Player(pygame.sprite.Sprite):
    """构造函数"""

    def __init__(self, x, y, sx, sy, w, h, jumpforce, color, gravity=True, gravVelocity=0.5, mass=1):


        # 确定大小
        self.sx, self.sy = sx, sy
        self.imageLeft = pygame.transform.scale(pygame.image.load("images/roleLeft.png"), (40, 50))
        self.imageRight = pygame.transform.scale(pygame.image.load("images/roleRight.png"), (40, 50))
        # 初始化移动标记
        self.accelRight, self.accelLeft, self.decceler = False, False, False

        self.accelVelocity = 0.5 / mass
        self.deccelVelocity = 0.6 / mass

        # 获取涂鸦矩形
        self.rect = Rect(x, y, w, h)

        # 角色外观铸造
        self.color = color
        # self.image = pygame.Surface((w, h))
        # self.image.fill(self.color)
        self.image = pygame.transform.scale(pygame.image.load("images/roleLeft.png"), (40, 50))

        self.isGrounded = False
        self.maxSpeedX, self.maxSpeedY = 12, 25
        self.jumpforce = jumpforce
        self.gravity = gravity  # 重力
        self.mass = mass  # 质量
        self.gravVelocity = gravVelocity * mass

        self.events = [0, 0, 0]
        self.score = 0
        self.dead = False

    def collide(self, sx, sy, colliders, bonuses):
        for p in colliders:
            if pygame.sprite.collide_rect(self, p):
                # if sx > 0:
                #    self.rect.right = p.rect.left
                # if sx < 0:
                #    self.rect.left = p.rect.right
                if sy > -0.5:
                    # 踩到了陷阱踏板
                    if p.breakable:
                        colliders.remove(p)
                    if p.canJump:
                        self.rect.bottom = p.rect.top
                        self.isGrounded = True
                        self.sy = 0
            # if sy < 0:
            #    self.sy = 0.1
            #    self.rect.top = p.rect.bottom
        for b in bonuses:
            if pygame.sprite.collide_rect(self, b):
                if sy > -1:
                    self.sy = b.addForce
                    if b.duration > 1:
                        for i in range(b.duration):
                            self.sy += b.addForce

    # 更新地图
    def update(self, blocks, bonuses, camera):

        self.score = camera.state.y
        self.isGrounded = False
        if self.accelRight:
            self.image = self.imageRight
        if self.accelLeft:
            self.image = self.imageLeft
        if self.accelRight and self.sx < self.maxSpeedX:
            self.sx += self.accelVelocity
        if self.accelLeft and self.sx > -self.maxSpeedX:
            self.sx -= self.accelVelocity
        if self.decceler:
            if self.sx == 0:
                self.decceler = False
            if self.sx > 0:
                self.sx -= self.deccelVelocity
            if self.sx < 0:
                self.sx += self.deccelVelocity

        if camera.apply(self).y > HUYWIN:
            # self.isGrounded = True
            # self.rect.y = YWIN - self.rect.height
            self.dead = True

        if self.gravity:
            if self.isGrounded == False:
                self.sy += self.gravVelocity
                if self.sy > self.maxSpeedY:
                    self.sy = self.maxSpeedY

        self.rect.left = (self.rect.left + self.sx) % HUXWIN

        self.rect.top += self.sy
        self.collide(0, self.sy, blocks, bonuses)

    # 绘制涂鸦函数
    def draw(self, surface, camera=None):
        if camera is not None:
            a = camera.apply(self)
            a.bottom -= 13
            surface.blit(self.image, a)
        else:
            surface.blit(self.image, self.rect)
