"""
    file name: game.py
    effect: 控制游戏的主循环
"""

from function import *
from world import *
from player import *
from camera import Camera
from settings import *
import Qlearning as ql

import sqlite3
"""主函数"""



def resetGame(player, world, camera):
    player.__init__(300, 550, 0, 0, 25, 30, 12, COLORS[6])
    world.__init__(player.rect.x, player.rect.y, [COLORS[11], COLORS[10], COLORS[12]], [COLORS[9]])
    camera.__init__(simple_camera, XWIN, YWIN, 6.5)

def main():
    # start db connection
    conn = sqlite3.connect('DisplayScore/score.sqlite')
    c = conn.cursor()
    sql_update = "insert into info(score,is_added) values(?,0);"

    pygame.init()

    #  确定字体
    FONTS = [
        pygame.font.Font(None, 32),
        pygame.font.Font(None, 64),
        pygame.font.Font(None, 20)
    ]
    # 创建窗口
    window = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("doodle jump")

    # 追踪时间
    clock = pygame.time.Clock()

    # Variables
    camera = Camera(simple_camera, XWIN, YWIN, 6.5)
    # player = Player(300, 550, 0, 0, 25, 30, 12, COLORS[6])
    player = Player(300, 550, 0, 0, 25, 30, 12, COLORS[6])
    world = World(player.rect.x, player.rect.y, [COLORS[11], COLORS[10], COLORS[12]], [COLORS[9]])

    # 打开链表主循环
    loopGame = True
    # 标识位
    isCollision = False
    isBounce = False
    previous_collision = None
    maxScore = 0
    # keyState[0]表示加速, [1]表示减速, [2]表示保存QTable
    keyState = [False, False, False]
    # 记录总共玩的局数
    counter = 1

    # Main Game Loop
    while loopGame:
        taskManager(player)
        camera.update(player)
        world.update(camera)

        # 填充背景颜色
        window.fill(COLORS[13])

        for event in pygame.event.get():
            eventManager(event, player, world, camera, keyState)
        # 保存QTable
        if keyState[2]:
            ql.saveTable()
            keyState[2] = False

        # 涂鸦没有掉下去
        if not player.dead:
            text(25, 10, FONTS[0], COLORS[1], str(int(player.score * 0.02646)) + " m", window)
            playerState = []
            player.update(world.platforms, world.bonuses, camera, playerState)
            # 更新状态
            if playerState[0] is True:
                isCollision = playerState[0]
            if playerState[1] is True:
                isBounce = True
            if playerState[2] is not None:
                previous_collision = playerState[2]
            player.draw(window, camera)
        # 涂鸦掉下去，出现游戏结束画面
        else:
            counter += 1
            text(190, 200, FONTS[1], COLORS[2], "GAME OVER", window)
            text(200, 300, FONTS[1], COLORS[1], "SCORE: " + str(int(player.score * 0.02646)) + " m", window)

        # 碰到平台, 就进行预测
        if isCollision:
            isCollision = False
            ql.decide(world.platforms, player, player.score, previous_collision, counter)

        # 碰到弹簧, 且当玩家高度为0时, 预测
        if isBounce and player.sy == -15.0:
            ql.decide(world.platforms, player, player.score, previous_collision, counter, isBounce)
            isBounce = False

        #  根据预测的平台移动
        dire, target_platform = ql.direction(player)
        if dire == "left":
            if player.sx >= 0:
                player.sx = -1.5
                player.events[0] = 1
                player.events[1] = 0
        elif dire == "right":
            if player.sx <= 0:
                player.sx = 1.5
                player.events[0] = 0
                player.events[1] = 1
        else:
            player.sx = 0
            player.events[0] = 0
            player.events[1] = 0

        # 当到达目标平台时, 停止移动
        if target_platform is not None and target_platform.rect.x + 10 <= player.posX() <= target_platform.rect.x + target_platform.rect.width - 10:
            player.sx = 0
            player.events[0] = 0
            player.events[1] = 0

        # 更新踏板和弹簧
        for b in world.platforms:
            window.blit(b.image, camera.apply(b))
            # 如果是预测平台, 则涂为红色, 同时覆盖之前的分数字体
            if b is target_platform:
                b.image.fill(COLORS[2])
            # 不是, 要涂为原色
            else:
                b.image.fill(b.color)

            label = FONTS[2].render(str(b.predictScore), False, COLORS[1])
            b.image.blit(label, (20, 0))

        for b in world.bonuses:
            window.blit(b.image, camera.apply(b))

        # 重置循环 死亡给分有问题,
        if player.dead:
            isBounce = False
            isCollision = False
            ql.decide(world.platforms, player, player.score, previous_collision, counter)

            if player.score > maxScore:
                maxScore = player.score
                print("maxScore: " + str(maxScore))

            counter += 1
            if counter % 100 == 0:
                print("counter" + str(counter))
                print("保存QTable")
                ql.saveTable()
                # exit(0)

            player.sy = 0
            # 只能设置为-1或者0 防止发生list超出错误
            previous_collision = None
            player.dead = False

            ll = [int(player.score * 0.02646)]
            c.execute(sql_update, ll)
            conn.commit()
            resetGame(player, world, camera)

        # 修改游戏环境
        # 加速
        if keyState[0]:
            FPS = 500000
        # 放慢
        elif keyState[1]:
            pygame.display.update()
            FPS = 10
        # 正常
        else:
            pygame.display.update()
            FPS = 60

        clock.tick(FPS)
