import random as ra


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

#  round the y distance to the nearest ydivision
ydivision = 10
xdivision = 40
previous_score = 0
# how does this happen sometimes
# the genie did it se c LLEOMLME L OLA DLOL OLOLOLOL
previous_collision = -1
target_platform = -2
base_score = 0


def get_states():
    state = []
