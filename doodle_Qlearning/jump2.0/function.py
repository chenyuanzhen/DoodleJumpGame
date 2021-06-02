"""
    file name: function.py
    effect:
"""
import sys

from pygame.constants import *
from pygame.rect import Rect
from settings import *


# ALL KIND OF CAMERA.
def simple_camera(camera, target_rect):

    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(0, -t + HALF_HEIGHT, w, h)


# Functions
def text(x, y, font, color, inText, surface):

    inText = font.render(inText, True, color)
    surface.blit(inText, (x, y))


def taskManager(player):
    # 向左移动
    if player.events[0] == 1:
        player.accelLeft = True
        player.accelRight = False
        player.decceler = False
    # 向右移动
    elif player.events[1] == 1:
        player.accelRight = True
        player.accelLeft = False
        player.decceler = False
    # 重力掉落
    else:
        player.decceler = True
        player.accelLeft = False
        player.accelRight = False

    player.events[2] = 1
    if player.events[2] == 1 and player.isGrounded:
        player.events[2] = 0
        player.isGrounded = False
        player.rect.y -= int(player.rect.height / 2)
        player.sy = -player.jumpforce


# keyState[0]表示加速, [1]表示减速, [2]表示保存QTable
def eventManager(event, player, world, camera, keyState=None):

    # 退出游戏事件
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        # 重开是吧
        if event.key == K_RETURN and player.dead:
            player.dead = False
            player.__init__(300, 550, 0, 0, 25, 30, 12, COLORS[6])
            world.__init__(player.rect.x, player.rect.y, [COLORS[11], COLORS[10], COLORS[12]], [COLORS[9]])
            camera.__init__(simple_camera, XWIN, YWIN, 6.5)
        # 想向左操作是吧
        if event.key == K_LEFT:
            player.sx = -1.5
            player.events[0] = 1
            player.events[1] = 0
        # 想向右操作是吧
        if event.key == K_RIGHT:
            player.sx = 1.5
            player.events[1] = 1
            player.events[0] = 0

        if event.key == K_SPACE:
            player.events[2] = 1
        # 加速训练
        if event.key == K_v:
            # print("0 : " + str(keyState[0]))
            if keyState[0] is False:
                keyState[0] = True
            else:
                keyState[0] = False

            # print("0 : " + str(keyState[0]))
        # 减缓速度
        if event.key == K_s:
            if keyState[1] is False:
                keyState[1] = True
            else:
                keyState[1] = False
            # print("1 : " + str(keyState[1]))
        # 保存
        if event.key == K_t:
            keyState[2] = True

    elif event.type == KEYUP:

        if event.key == K_LEFT:
            player.events[0] = 0

        if event.key == K_RIGHT:
            player.events[1] = 0
