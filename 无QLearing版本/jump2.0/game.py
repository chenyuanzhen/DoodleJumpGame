"""
    file name: game.py
    effect: 控制游戏的主循环
"""

from function import *
from world import *
from player import *
from camera import Camera
from settings import *

"""主函数"""


def main():
    pygame.init()

    #  确定字体
    FONTS = [
        pygame.font.Font(None, 32),
        pygame.font.Font(None, 64),
    ]

    # 创建窗口
    window = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("doodle jump")

    # 追踪时间
    clock = pygame.time.Clock()

    # Variables
    camera = Camera(simple_camera, XWIN, YWIN, 6.5)
    player = Player(300, 550, 0, 0, 25, 30, 12, COLORS[6])
    world = World(player.rect.x, player.rect.y, [COLORS[11], COLORS[10], COLORS[12]], [COLORS[9]])

    # 打开链表主循环
    loopGame = True
    # Main Game Loop
    while loopGame:

        for event in pygame.event.get():
            eventManager(event, player)
        taskManager(player)

        camera.update(player)
        world.update(camera)

        # 填充背景颜色
        window.fill(COLORS[13])

        # 更新踏板和弹簧
        for b in world.platforms:
            # 这里如果能换成镇哥想要的椭圆就好了，目前还没什么办法
            window.blit(b.image, camera.apply(b))
        for b in world.bonuses:
            window.blit(b.image, camera.apply(b))

        # 涂鸦没有掉下去
        if not player.dead:
            text(25, 10, FONTS[0], COLORS[1], str(int(player.score * 0.02646)) + " m", window)
            player.update(world.platforms, world.bonuses, camera)
            player.draw(window, camera)
        # 涂鸦掉下去，出现游戏结束画面
        else:
            text(190, 200, FONTS[1], COLORS[2], "GAME OVER", window)
            text(200, 300, FONTS[1], COLORS[1], "SCORE: " + str(int(player.score * 0.02646)) + " m", window)

        pygame.display.update()
        clock.tick(FPS)
