"""
    file name: game.py
    effect: 控制游戏的主循环
"""

import pygame
import ai
import human
from settings import *

"""主函数"""

def main():

    pygame.init()

    #  确定字体
    FONTS = [
        pygame.font.Font(None, 32),
        pygame.font.Font(None, 64),
        pygame.font.Font(None, 20)
    ]
    # 创建窗口
    # Window contained two factors
    window = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    # create two surfaces for each player
    ai_screen = pygame.Surface((AISHOW),FLAGS,DEPTH)
    human_screen = pygame.Surface((HUSHOW),FLAGS,DEPTH)
    pygame.display.set_caption("Doodle Jump -- AI Against Human")

    # 追踪时间
    clock = pygame.time.Clock()

    # Variables
    ai_camera = ai.camera.Camera(ai.function.simple_camera, AIXWIN, AIYWIN, 6.5)
    human_camera = human.camera.Camera(human.function.simple_camera, HUXWIN, HUYWIN, 6.5)
    ai_player = ai.player.Player(300, 550, 0, 0, 25, 30, 12, COLORS[6])
    human_player = human.player.Player(300, 550, 0, 0, 25, 30, 12, COLORS[6])
    ai_world = ai.world.World(ai_player.rect.x, ai_player.rect.y, [COLORS[11], COLORS[10], COLORS[12]], [COLORS[9]])
    human_world = ai.world.World(human_player.rect.x, human_player.rect.y, [COLORS[11], COLORS[10], COLORS[12]], [COLORS[9]])

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
        ai.function.taskManager(ai_player)
        ai_camera.update(ai_player)
        ai_world.update(ai_camera)
        human.function.taskManager(human_player)
        human_camera.update(human_player)
        human_world.update(human_camera)

        # 填充背景颜色
        ai_screen.fill(COLORS[13])
        human_screen.fill(COLORS[13])

        for event in pygame.event.get():
            ai.function.eventManager(event, ai_player, ai_world, ai_camera, keyState)
            human.function.eventManager(event, human_player, human_world, human_camera, keyState)
        # 保存QTable
        if keyState[2]:
            ai.Qlearning.saveTable()
            keyState[2] = False

        # 涂鸦没有掉下去
        if not ai_player.dead:
            ai.function.text(25, 10, FONTS[0], COLORS[1], str(int(ai_player.score * 0.02646)) + " m", ai_screen)
            playerState = []
            ai_player.update(ai_world.platforms, ai_world.bonuses, ai_camera, playerState)
            # 更新状态
            if playerState[0] is True:
                isCollision = playerState[0]
            if playerState[1] is True:
                isBounce = True
            if playerState[2] is not None:
                previous_collision = playerState[2]
            ai_player.draw(ai_screen, ai_camera)
        # 涂鸦掉下去，出现游戏结束画面
        else:
            counter += 1
            ai.function.text(190, 200, FONTS[1], COLORS[2], "GAME OVER", ai_screen)
            ai.function.text(200, 300, FONTS[1], COLORS[1], "SCORE: " + str(int(ai_player.score * 0.02646)) + " m", ai_screen)

        # 碰到弹簧, 且当玩家高度为0时, 预测
        if isBounce and ai_player.sy == -15.0:
            ai.Qlearning.decide(ai_world.platforms, ai_player, ai_player.score, previous_collision, counter, isBounce)
        # 碰到平台, 就进行预测
        elif isCollision:
            isCollision = False
            ai.Qlearning.decide(ai_world.platforms, ai_player, ai_player.score, previous_collision, counter, isBounce)
            isBounce = False

        #  根据预测的平台移动
        dire, target_platform = ai.Qlearning.direction(ai_player)
        if dire == "left":
            if ai_player.sx >= 0:
                ai_player.sx = -1.5
                ai_player.events[0] = 1
                ai_player.events[1] = 0
        elif dire == "right":
            if ai_player.sx <= 0:
                ai_player.sx = 1.5
                ai_player.events[0] = 0
                ai_player.events[1] = 1
        else:
            ai_player.sx = 0
            ai_player.events[0] = 0
            ai_player.events[1] = 0

        # 当到达目标平台时, 停止移动
        if target_platform is not None and target_platform.rect.x + 15 <= ai_player.posX() <= target_platform.rect.x + target_platform.rect.width - 15:
            ai_player.sx = 0
            ai_player.events[0] = 0
            ai_player.events[1] = 0

        # 更新踏板和弹簧
        for b in ai_world.platforms:
            ai_screen.blit(b.image, ai_camera.apply(b))
            # 如果是预测平台, 则涂为红色, 同时覆盖之前的分数字体
            if b is target_platform:
                b.image.fill(COLORS[2])
            elif b is previous_collision:
                if b.kind() == 2:
                    b.image.fill(COLORS[9])
                else:
                    b.image.fill(COLORS[1])
            # 不是, 要涂为原色
            else:
                b.image.fill(b.color)

            label = FONTS[2].render(str(b.predictScore), False, COLORS[1])
            b.image.blit(label, (20, 0))

        for b in ai_world.bonuses:
            ai_screen.blit(b.image, ai_camera.apply(b))

        # 重置循环
        if ai_player.dead:
            isBounce = False
            isCollision = False
            ai.Qlearning.decide(ai_world.platforms, ai_player, ai_player.score, previous_collision, counter)
            previous_collision = None

            if ai_player.score > maxScore:
                maxScore = ai_player.score
                print("maxScore: " + str(maxScore))

            counter += 1
            if counter % 100 == 0:
                print("counter" + str(counter))
            #     print("保存QTable")
            #     ai.Qlearning.saveTable()

        # FOR HUMAN
        # 更新踏板和弹簧
        for b in human_world.platforms:
            human_screen.blit(b.image, human_camera.apply(b))
        for b in human_world.bonuses:
            human_screen.blit(b.image, human_camera.apply(b))

        # 涂鸦没有掉下去
        if not human_player.dead:
            human.function.text(25, 10, FONTS[0], COLORS[1], str(int(human_player.score * 0.02646)) + " m", human_screen)
            human_player.update(human_world.platforms, human_world.bonuses, human_camera)
            human_player.draw(human_screen, human_camera)
        # 涂鸦掉下去，出现游戏结束画面
        else:
            human.function.text(190, 200, FONTS[1], COLORS[2], "GAME OVER", human_screen)
            human.function.text(200, 300, FONTS[1], COLORS[1], "SCORE: " + str(int(human_player.score * 0.02646)) + " m", human_screen)

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

        window.blit(ai_screen, (0, 0))
        window.blit(human_screen, (650, 0))
