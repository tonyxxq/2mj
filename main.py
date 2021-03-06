import random
from game import Game
from deepplayer import DeepPlayer
from aiplayer import AiPlayer
import times
from collections import deque
import time
from ws4py.client.threadedclient import WebSocketClient


def main(memory1, memory2):
    """
    :param memory1: 吃碰杠胡的动作、状态、奖励列表
    :param memory2: 出牌的动作、状态、奖励列表
    """

    # 初始化牌局，洗牌，初始化两个选手
    paiju = Game()
    player1 = AiPlayer(paiju.fapai(), paiju)
    player2 = AiPlayer(paiju.fapai(), paiju)

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
            pai = player2.chupai_process()
            if paiju.finished:
                player2.score = -player1.score
            else:
                player2.oppo_pai = pai
        turn = not turn

    print("player1: data", times.restore_pais(player1.data), player1.fanzhong)
    print("player2: data", times.restore_pais(player2.data), player2.fanzhong)


if __name__ == '__main__':
    try:
        ws = DummyClient('ws://localhost:4567/', protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()

if __name__ == '__main__':
    # start_time =time.time()
    # for i in range(1000):

    main()

    # end_time =time.time()
    # print(start_time - end_time)
