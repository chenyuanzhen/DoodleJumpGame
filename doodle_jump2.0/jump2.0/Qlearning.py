import random as ra
import json


class Q_model:
    # 记录行动 使用字典
    action = {}
    # 记录探索的状态数
    explored = 0
    # 记录上一个状态
    last_state = [0, 0, 0]
    # 学习率
    learning_rate = 1
    # 随机概率
    random = 1

    # 预测下一个状态
    # 传入的是平台
    def predict(self, state):
        self.last_state = state
        # 平台类型
        i = state[0]
        # 平台的y距离
        j = state[1]
        # 平台的x距离
        k = state[2]

        #  处理已经见过的平台
        if i in self.action:
            # 处理该平台下的y距离
            if j in self.action[i]:
                # 处理该该平台下y距离和x距离
                if k in self.action[i][j]:
                    return self.action[i][j][k]
                else:
                    # 新的x距离 添加随机值
                    self.action[i][j][k] = 0
                    self.action[i][j][k] += ra.randint(0, 100)
                    self.explored += 1
                    return self.action[i][j][k]
            # 新的y距离
            else:
                self.action[i][j] = {}
                self.action[i][j][k] = 0
                self.action[i][j][k] += ra.randint(0, 100)
                self.explored += 1
                return self.action[i][j][k]
        # 新的平台类型
        else:
            self.action[i] = {}
            self.action[i][j] = {}
            self.action[i][j][k] = 0
            self.action[i][j][k] += ra.randint(0, 100)
            self.explored += 1
            return self.action[i][j][k]

    # 奖赏反馈
    def reward(self, amount):
        # positive为1, 随机执行
        positive = 0
        i = self.last_state[0]
        j = self.last_state[1]
        k = self.last_state[2]

        if self.action[i][j][k] > 0:
            positive = 1

        self.action[i][j][k] += self.learning_rate * amount

        # 随机执行
        if self.action[i][j][k] == 0 and positive == 1:
            self.action[i][j][k] -= 1

        # print("last_state y: " + str(j) + " x " + str(k) + " score: " + str(self.action[i][j][k]))

    # explored 也要保存
    # 保存QTable 有问题, json可能会有重复的键
    def saveTable(self):
        # if os.path.exists('LastQTable.json') is False:
        f = open('QTable.json', 'w')
        json.dump(self.action, f)
        f.close()

    def loadTable(self):
        try:
            print("装载qtable")
            f = open('QTable.json', 'r')
            self.action = json.load(f)
            f.close()
        except IOError:
            print("文件不存在或者文件无权限")


brain = Q_model()
# 目标平台的索引
previous_score = 0
isFirst = True
target_platform = None
states = {}
previous_player_height = 0
scale_reward_pos = 1 / 75


def saveTable():
    brain.saveTable()


# 装载Qtable
def loadTable():
    brain.loadTable()


lastTarget = None


# 遍历当前的所有平台, 然后预测每一个平台的分数
# previous_collision需要从外面更新, 因为target_platform不一定是当前平台
def decide(platforms, player, score, previous_collision, counter=1, isBounce=False):
    global lastTarget
    global isFirst
    global previous_score
    global states
    global target_platform
    global previous_player_height
    if isBounce is not True:
        if counter % 500 == 0 and counter != 0:
            print("探索的状态: " + str(brain.explored))
            print("局数到达500, 自动保存QTable")
            brain.saveTable()
            # exit(0)

        if target_platform is not None and previous_collision is not None and isFirst is False:
            if player.dead:
                scale_death = 1 + score / 2000
                brain.reward(-100 * scale_death)
                previous_score = 0
                target_platform = None
                isFirst = True
                return
            else:
                # 到达的平台不是目标平台
                if previous_collision != target_platform and previous_collision in states and target_platform in states:

                    if target_platform.posY() < previous_collision.posY():
                        brain.reward(-20)

                    # 目标平台与当前平台一直
                    else:
                        brain.reward(-10)

                if previous_collision is not None and previous_collision in states:
                    brain.predict(states[previous_collision])
                    r = score - previous_score - 20
                    previous_score = score
                    brain.reward(r)

    isFirst = False

    states = get_states(platforms, player)

    maxReward = -float('inf')

    # 遍历平台 并从总挑选预测分数最高的平台
    for zz in range(0, len(platforms)):
        # # 限定检查平台范围
        if platforms[zz].posY() + 500 <= player.posY():
            continue
        platforms[zz].predictScore = brain.predict(states[platforms[zz]])

        if maxReward < platforms[zz].predictScore:
            maxReward = platforms[zz].predictScore
            target_platform = platforms[zz]

    # 记录目录平台
    lastTarget = target_platform
    # 调用预测函数, 将当前平台更新为上一个平台
    if target_platform is not None:
        brain.predict(states[target_platform])
    # 更新先前数据
    previous_player_height = player.rect.height


# 获取状态
def get_states(platforms, player):
    state = {}
    yDivision = 20
    xDivision = 60
    for platform in platforms:
        state[platform] = [platform.kind(), round((platform.posY() - player.posY()) / yDivision),
                           abs(round((platform.posX() - player.posX()) / xDivision))]
    return state


# 选择方向移动
# 挑选出最适合的平台, 比较player和该平台的x距离, 做出移动
# none 为不移动
def direction(player):
    dire = "none"
    if target_platform is None:
        return dire, target_platform

    pX = target_platform.posX()
    # 防止player跳过平台
    if pX < player.posX():
        dire = "left"
    elif pX > player.posX():
        dire = "right"

    return dire, target_platform
