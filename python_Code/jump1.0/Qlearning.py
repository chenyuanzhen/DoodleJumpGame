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
    learning_rate = 1
    # 随机概率
    random = 1

    # 预测下一个状态
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
            # a为平台类型

            # 处理该平台下的y距离
            if j in self.action[i]:
                b = self.action[i]
                # 处理该该平台下y距离和x距离
                if k in b[j]:
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

    # 保存QTable 有问题, json可能会有重复的键
    def saveTable(self):
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
target_platform = -1
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
    if counter > 100 and counter % 1000 == 0:
        print("次数达1000次, 保存QTable")
        brain.saveTable()

    if target_platform >= 0 and previous_score >= 0 and isFirst is False:
        # print("target: " + str(target_platform) + " now: " + str(previous_collision))
        if player.dead:
            scale_death = 1 + score / 2000
            brain.reward(-100 * scale_death)
            previous_score = 0
            target_platform = -1
            isFirst = True
            # 重置游戏
            return
        else:
            # 防止越跳越低
            if previous_collision != target_platform:
                # state[target_platform][1] 获取target_platform的高度,
                if len(states) >= 2 and target_platform < len(states) and previous_collision < len(states) and states[target_platform][1] < states[previous_collision][1]:
                    brain.reward(-20)
            # 防止原地tp
            else:
                brain.reward(-10)
                if len(states) >= 2 and previous_collision < len(states):
                    brain.predict(states[previous_collision])
                    r = score - previous_score - 20
                    brain.reward(r)

    isFirst = False
    previous_score = score
    states = get_states(platforms, player)

    predictions = {}
    maxRewardIndex = 0
    # 遍历平台 并从总挑选预测分数最高的平台
    for zz in range(0, len(states)):
        predictions[zz] = brain.predict(states[zz])
        platforms[zz].predictScore = predictions[zz]
        if predictions[zz] > predictions[maxRewardIndex]:
            maxRewardIndex = zz

    # 记录目录平台
    target_platform = maxRewardIndex
    # 调用预测函数, 将当前平台更新为上一个平台
    brain.predict(states[target_platform])
    # 更新先前数据
    previous_player_height = player.rect.height
    return False


# 获取状态
def get_states(platforms, player):
    # 用于缩小数据范围
    yDivision = 10
    xDivision = 40
    state = []

    # 得到的是离图像最左开始算的x轴坐标, 即玩家的中心坐标
    for block in platforms:
        # 平台类型, 平台离玩家的y轴距离(高度差), 平台离玩家的x轴距离,
        state.append([block.kind(), block.posY() - player.posY(), block.posX() - player.posX()])

    return state


# 选择方向移动
# 挑选出最适合的平台, 比较player和该平台的x距离, 做出移动
# none 为不移动
def direction(platforms, player):
    dire = "none"
    try:
        pX = platforms[target_platform].posX()
        # 防止player跳过平台
        if pX < player.posX():
            dire = "left"
        elif pX > player.posX():
            dire = "right"
    except:
        pass

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
