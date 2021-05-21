import os
import random as ra
import json

# import otherVersion as gameVersion


class Q_model:
    # 记录行动 使用字典
    action = {}
    # 记录探索的状态数
    explored = 0
    # 记录上一个状态
    last_state = [0, 0, 0]
    # 学习率
    learning_rate = 0.8
    # 随机概率
    random = 1

    # 预测下一个状态
    # 传入的是平台
    def predict(self, state):
        self.last_state = state
        # 平台类型
        i = state.kind()
        # 平台的y距离
        j = state.posY()
        # 平台的x距离
        k = state.posY()

        #  处理已经见过的平台
        if state.kind() in self.action:
            # a为平台类型

            # 处理该平台下的y距离
            if state.posY() in self.action[state.kind()]:
                # 处理该该平台下y距离和x距离
                if state.posX() in self.action[state.kind()][state.posY()]:

                    return self.action[i][j][k]
                else:
                    # 新的x距离 添加随机值
                    self.action[i][j][k] = ra.randint(0, 100)
                    self.explored += 1
                    return self.action[i][j][k]
            # 新的y距离
            else:
                self.action[i][j] = {}
                self.action[i][j][k] = ra.randint(0, 100)
                self.explored += 1
                return self.action[i][j][k]
        # 新的平台类型
        else:
            self.action[i] = {}
            self.action[i][j] = {}
            self.action[i][j][k] = ra.randint(0, 100)
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

    # explored 也要保存
    # 保存QTable 有问题, json可能会有重复的键
    def saveTable(self):
        # if os.path.exists('QTable.json') is False:
        f = open('QTable.json', 'w')
        json.dump(self.action, f)
        f.close()

    def loadTable(self):
        try:
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


# 装载Qtable
def loadTable():
    brain.loadTable()


# 遍历当前的所有平台, 然后预测每一个平台的分数
# previous_collision需要从外面更新, 因为target_platform不一定是当前平台
def decide(platforms, player, score, previous_collision, counter=1):
    global isFirst
    global previous_score
    global states
    global target_platform
    global previous_player_height
    if counter == 10000:
        print("10000, 自动退出, 保存QTable")
        brain.saveTable()
        exit(0)

    if target_platform is not None and previous_score is not None and isFirst is False:
        if player.dead:
            scale_death = 1 + score / 2000
            brain.reward(-100 * scale_death)
            previous_score = 0
            target_platform = None
            isFirst = True
        else:
            # 防止越跳越低
            if previous_collision.posX() != target_platform.posX() and previous_collision.posY() != target_platform.posY():
                if target_platform.posY() < previous_collision.posY():
                    brain.reward(-20)
                # 防止原地tp
                else:
                    brain.reward(-10)

            if previous_collision is not None:
                brain.predict(previous_collision)
                r = score - previous_score - 20
                brain.reward(r)
    # score要规定在100分之内, 而且要求player网上
    # print("score: " + str(score))
    isFirst = False
    previous_score = score
    states = get_states(platforms, player)

    maxRewardIndex = 0
    maxReward = 0
    # 遍历平台 并从总挑选预测分数最高的平台
    # 避免看的太远
    # 索引有问题, target_platform仅仅只是states里的索引, 但states的索引会变化, 导致其他地方对应不上
    for zz in range(0, min(len(states), 10)):
        platforms[zz].predictScore = brain.predict(states[zz])

        if maxReward < platforms[zz].predictScore:
            maxReward = platforms[zz].predictScore
            maxRewardIndex = zz

    # 记录目录平台
    target_platform = platforms[maxRewardIndex]
    # 调用预测函数, 将当前平台更新为上一个平台
    brain.predict(target_platform)
    # 更新先前数据
    previous_player_height = player.rect.height


# 获取状态
def get_states(platforms, player):
    # 用于缩小数据范围
    yDivision = 10
    xDivision = 40
    state = []

    # 得到的是离图像最左开始算的x轴坐标, 即玩家的中心坐标
    for block in platforms:
        # 平台类型, 平台离玩家的y轴距离(高度差), 平台离玩家的x轴距离,
        state.append([block.kind(),
                      round((block.posY() - player.posY())/yDivision * yDivision),
                      abs(round((block.posX() - player.posX())/xDivision * xDivision))])

    return state


# 选择方向移动
# 挑选出最适合的平台, 比较player和该平台的x距离, 做出移动
# none 为不移动
def direction(platforms, player):
    dire = "none"
    try:
        pX = target_platform.posX()
        # 防止player跳过平台
        if pX + 15 < player.posX():
            dire = "left"
        elif pX + 15 > player.posX():
            dire = "right"

    except:
        pass
    # print("dire: " + dire)
    return dire, target_platform

# brain = Q_model()

# 自动状态q_learning从磁盘, 不用重新学习
# //autoload brain from disk
# if(store.has('brain')) {
#   var storedBrain = store.get('brain');
#   brain.actions = storedBrain.actions;
#   brain.explored = storedBrain.explored;
#   //brain.last_state = storedBrain.last_state;
#   console.log('Brain has been loaded');
#   console.log('States explored:' + brain.explored);
# }
