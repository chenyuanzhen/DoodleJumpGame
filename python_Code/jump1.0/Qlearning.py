import random as ra
import otherVersion as gameVersion


class Q_model:
    # 记录行动
    action = []
    # 记录探索的状态数
    explored = 0
    # 记录上一个状态
    last_state = [0, 0]
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
        if self.action[i] is not None:
            # a为平台类型
            a = self.action[i]
            # 处理该平台下的y距离
            if a[j] is not None:
                b = a[j]
                # 处理该该平台下y距离和x距离
                if b[k] is not None:
                    return b[k]
                else:
                    # 新的x距离 添加随机值
                    self.action[i][j][k] = ra.randint(0, 100)
                    self.explored += 1
                    return self.action[i][j][k]
            # 新的y距离
            else:
                self.action[i][j] = []
                self.action[i][j][k] = ra.randint(0, 100)
                self.explored += 1
                return self.action[i][j][k]
        # 新的平台类型
        else:
            self.action[i] = []
            self.action[i][j] = []
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


brain = Q_model()
previous_score = 0
# how does this happen sometimes
# the genie did it se c LLEOMLME L OLA DLOL OLOLOLOL
previous_collision = -1
# 目标平台
target_platform = -2
base_score = 0
states = []
previous_player_height = 0
scale_reward_pos = 1 / 75
previous_collision2 = -3
previous_score = 0


# 遍历当前的所有平台, 然后预测每一个平台的分数
def decide(platform, player, score):
    global previous_score
    global previous_collision
    global states
    global target_platform
    global previous_player_height
    global previous_collision2

    if target_platform >= 0 and previous_score >= 0:
        if player.dead:
            scale_death = 1 + score / 2000
            brain.reward(-100 * scale_death)
            # 重置游戏
            gameVersion.resetGame()
        else:
            if previous_collision != target_platform:
                if states[target_platform][1] < states[previous_collision][1]:
                    brain.reward(-20)
                else:
                    brain.reward(-10)
            brain.predict(states[previous_collision])
            r = score - previous_score - 20
            brain.reward(r)

    previous_score = score
    states = get_states(platform, player)

    predictions = []
    maxReward = 0
    maxRewardIndex = 0
    # 遍历平台
    for zz in range(0, len(states)):
        predictions[zz] = brain.predict(states[zz])
        # 显示 platform[zz].reward(predictions)
        if predictions[zz] > predictions[maxRewardIndex]:
            maxReward = predictions[zz]
            maxRewardIndex = zz

    # 记录目录平台
    target_platform = maxRewardIndex
    # 预测
    brain.predict(states[target_platform])
    # 根据target确定要跳平台
    previous_player_height = player.height
    previous_collision2 = previous_collision2


# 获取状态
def get_states(platforms, player):
    yDivision = 10
    xDivision = 40
    state = []
    for block in platforms:
        playerX = player.rect.left + player.rect.width / 2
        playerY = player.rect.top + player.rect.height / 2
        blockX = block.rect.left + block.rect.width / 2
        blockY = block.rect.top + block.rect.height / 2
        # 平台类型, 平台离玩家的y轴距离(高度差), 平台离玩家的x轴距离,
        state.append([block.kind(), blockY - playerY, blockX - playerX])

    return state


# 选择方向移动
def direction(platforms, n, player):
    p = platforms[n]
    dir = "none"
    try:
        if p.xDivision + 25 < player.xDivision:
            dir = "left"
        elif player.xDivision < p.xDivision + 15:
            dir = "rigth"
    except:
        pass
    return dir

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
