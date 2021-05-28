import random as ra
import json
import pickle


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


# 采用序列化
def saveTable():
    with open('QTable.txt', 'wb') as f:
        pickle.dump(brain, f)
    # 注意 json只能读取为字符型, 而self.action字典里的键值都是浮点型,
    with open('Qdict.json', 'w') as t:
        json.dump(brain.action, t)
    with open('Qdict.txt', 'wb') as q:
        pickle.dump(brain.action, q)


brain = Q_model()

# try:
#     f = open('QTable.txt', 'rb')
#     print("装载qtable")
#     brain = pickle.load(f)
#     f.close()
# except EOFError:
#     print("文件不存在或者文件无权限, 需要重新训练")
#     brain = Q_model()
#
# try:
#     # 不要装json, 因为json读取字典中都是字符, 而不是整形, 但self.action中需要是整型
#     table = open('Qdict.txt', 'rb')
#     brain.action = pickle.load(table)
#     table.close()
# except IOError or EOFError or TypeError or FileNotFoundError:
#     print("文件不存在或者文件无权限, 需要重新训练")
#     brain = Q_model()

# 目标平台的索引
previous_score = 0
isFirst = True
target_platform = None
states = {}
previous_player_height = 0
scale_reward_pos = 1 / 75




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

        if target_platform is not None and previous_collision is not None and isFirst is False:
            if player.dead:
                scale_death = 1 + score / 2000
                brain.reward(-500 * scale_death)
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
        if platforms[zz].posY() + 500 <= player.posY() <= platforms[zz].posY() - 500:
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
    # 设置y轴距离, 简化状态空间
    yDivision = 20
    # 设置x轴距离, 简化状态空间
    xDivision = 60
    # 建议设置 yDivision = 20, xDivision = 60 练习局数500不到, 就可以很好的预测.
    # 如果都设置为1, 状态空间太大, 练习时间估计超1小时.
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
