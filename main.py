import random
from game import Game
from deepplayer import DeepPlayer
from aiplayer import AiPlayer
import times
from collections import deque
import time

GAME = '2mj'  # the name of the game being played for log files
ACTIONS = 4  # number of valid actions
GAMMA = 0.99  # decay rate of past observations
OBSERVE = 100000.  # timesteps to observe before training
EXPLORE = 2000000.  # frames over which to anneal epsilon
FINAL_EPSILON = 0.0001  # final value of epsilon
INITIAL_EPSILON = 0.0001  # starting value of epsilon
REPLAY_MEMORY = 50000  # number of previous transitions to remember
BATCH = 32  # size of minibatch

def main(memory1, memory2):
    """
    :param memory1: 吃碰杠胡的动作、状态、奖励列表
    :param memory2: 出牌的动作、状态、奖励列表
    """

    # 初始化牌局，洗牌
    paiju = Game()

    # 初始化两个选手，第一个选手是普通 AI 对手，第二个对手使用深度学习确定出牌规则的选手
    player1 = AiPlayer(paiju.fapai(), paiju)
    player2 = DeepPlayer(paiju.fapai(), paiju)

    # 1. 存放状态、动作、奖励值
    # 2. 动作决策网络，动作正确正的奖励，动作错误负的奖励
    # 3. 出牌决策网络，对家胡了负的奖励，没有操作正的奖励

    # 确定庄、闲，摸牌的顺序，游戏没完成就循环执行, 要么有人胡，要么牌摸完了
    turn = random.random() >= 0.5

    if turn:
        player1.name = 'zhuang'
        player2.name = 'xian'
    else:
        player2.name = 'zhuang'
        player1.name = 'xian'

    while not paiju.finished:
        if turn:
            pai = player1.chupai_process()
            if paiju.finished:
                player2.score = -player1.score
            else:
                player2.oppo_pai = pai
        else:
            # 往记忆中存储
            pai = player2.chupai_process(memory1, memory2)



            if paiju.finished:
                player1.score = -player2.score
            else:
                player1.oppo_pai = pai
        turn = not turn

    print("player1: data", times.restore_pais(player1.data), player1.fanzhong)
    print("player2: data", times.restore_pais(player2.data), player2.fanzhong)



if __name__ == '__main__':
    memory1 = deque()
    memory2 = deque()

    # start_time =time.time()
    # for i in range(1000):

    main(memory1, memory2)



    # end_time =time.time()
    # print(start_time - end_time)
