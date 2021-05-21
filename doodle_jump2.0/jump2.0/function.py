"""
    file name: function.py
    effect:
"""

from function import *
from settings import *


# ALL KIND OF CAMERA.
def simple_camera(camera, target_rect):

    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(0, -t + HALF_HEIGHT, w, h)


# Functions
def text(x, y, font, color, text, surface):

    text = font.render(text, True, color)
    surface.blit(text, (x, y))


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


def eventManager(event, player):

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

    elif event.type == KEYUP:

        if event.key == K_LEFT:
            player.events[0] = 0

        if event.key == K_RIGHT:
            player.events[1] = 0
