import random
from game import Game
from deepplayer import DeepPlayer
from aiplayer import AiPlayer
import times
from collections import deque
import time
import dqn

GAME = '2mj'  # the name of the game being played for log files
ACTIONS = 4  # number of valid actions
GAMMA = 0.99  # decay rate of past observations
OBSERVE = 100000.  # timesteps to observe before training
EXPLORE = 2000000.  # frames over which to anneal epsilon
FINAL_EPSILON = 0.0001  # final value of epsilon
INITIAL_EPSILON = 0.0001  # starting value of epsilon
REPLAY_MEMORY = 50000  # number of previous transitions to remember
BATCH = 32  # size of minibatch


def main():
    """
    :param memory1: 吃碰杠胡的动作、状态、奖励列表
    :param memory2: 出牌的动作、状态、奖励列表
    """

    jp_memory = deque()
    cp_memory = deque()
    paiju, player1, player2, turn = init_paju()

    # 创建进牌和出牌神经网络
    sess = tf.InteractiveSession()
    jp_network = dqn.create_network()
    cp_network = dqn.create_network()

    cp_last_status, cp_last_actions, cp_last_reword = None, None, None
    while True:
        # 1. 牌局未开始或已经结束，重新开始游戏
        if paiju.finished:
            paiju, player1, player2, turn = init_paju()

        # 1. 存放状态、动作、奖励值
        # 2. 动作决策网络，动作正确正的奖励，动作错误负的奖励
        # 3. 出牌决策网络，对家胡了负的奖励，没有操作正的奖励
        if turn:
            pai = player1.chupai_process()
            if paiju.finished:
                player2.score = -player1.score
            else:
                player2.oppo_pai = pai

            # 深度学习学习玩家出过牌，那么就一定需要保存出牌的状态数据
            if player1.oppo_pai is not None:
                status = None
                cp_memory.append((cp_last_status, cp_last_actions, cp_last_reword, status, paiju.finished))
            else:
                cp_last_status, cp_last_actions, cp_last_reword = None, None, None
        else:
            # 往记忆中存储，计算奖励使用两个神经网络交替进行
            # 1. 当前牌局状态（输入数据）
            # 2. 输入到第一个神经网络，得到动作，执行得到动作结果状态
            # 3. 把上一个状态作为第二个神经网络的输入，得到结果并执行得到新的状态
            # 4. 把第一步和第二步的状态作为第一个神经网络的训练数据状态
            # 5. 把第二步和下一次第一步的状态作为第二个神经网络的训练数据状态

            status1 = None
            jp_actions = readout.eval(feed_dict={s: [status1]})[0]
            jp_actions = jp_network(status1)
            jp_action = actions[0]  # 得到最大的动作
            jp_reward = player2.jingpai_process(index)
            status2 = status()
            jp_memory.append((status1, jp_actions, jp_reward, status2, paiju.finished))

            # 把当前状态输入到下一个网络
            cp_actions = cp_network(status2)
            cp_action = cp_actions[0]
            cp_reward = player2.chupai_process(cp_action)
            cp_last_status, cp_last_actions, cp_last_reword = status2, cp_actions, cp_reward

            # 数据准备好了，开始训练



            if paiju.finished:
                player1.score = -player2.score
            else:
                player1.oppo_pai = pai
        turn = not turn

    print("player1: data", times.restore_pais(player1.data), player1.fanzhong)
    print("player2: data", times.restore_pais(player2.data), player2.fanzhong)


def init_paju():
    # 初始化牌局，洗牌
    paiju = Game()

    # 初始化两个选手，第一个选手是普通 AI 对手，第二个对手使用深度学习确定出牌规则的选手
    player1 = AiPlayer(paiju.fapai(), paiju)
    player2 = DeepPlayer(paiju.fapai(), paiju)

    # 确定庄、闲
    turn = random.random() >= 0.5
    if turn:
        player1.name = 'zhuang'
        player2.name = 'xian'
    else:
        player2.name = 'zhuang'
        player1.name = 'xian'

    return paiju, player1, player2, turn


if __name__ == '__main__':
    # start_time =time.time()
    # for i in range(1000):

    main()



    # end_time =time.time()
    # print(start_time - end_time)
