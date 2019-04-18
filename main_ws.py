import random

from ws4py.client.threadedclient import WebSocketClient

from aiplayer import AiPlayer
from game import Game
from wsplayer import WSPlayer
import time


def main():
    """
    :param memory1: 吃碰杠胡的动作、状态、奖励列表
    :param memory2: 出牌的动作、状态、奖励列表
    """

    # 建立 websocket 连接
    ws = DummyClient('ws://localhost:8887')
    ws.connect()

    # 初始化牌局，洗牌，初始化两个选手
    paiju = Game()
    player1 = AiPlayer(paiju.fapai(), paiju)
    wsplayer = WSPlayer(paiju.fapai(), paiju, ws)

    # 确定庄、闲，摸牌的顺序，游戏没完成就循环执行, 要么有人胡，要么牌摸完了
    turn = random.random() >= 0.5
    if turn:
        player1.name = 'zhuang'
        wsplayer.name = 'xian'
    else:
        wsplayer.name = 'zhuang'
        player1.name = 'xian'

    while not paiju.finished:
        if turn:
            pai = player1.chupai_process()
            if paiju.finished:
                wsplayer.score = -player1.score
            else:
                wsplayer.oppo_pai = pai
        else:
            pai = wsplayer.chupai_process(ws)
            # if paiju.finished:
            #     player1.score = -wsplayer.score
            # else:
            #     player1.oppo_pai = pai
        turn = not turn

    # webscoket 一直建立连接
    ws.run_forever()

    # print("player1: data", times.restore_pais(player1.data), player1.fanzhong)
    # print("player2: data", times.restore_pais(player1.data), player1.fanzhong)


class DummyClient(WebSocketClient):
    def opened(self):
        print("connected")

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        return message

if __name__ == '__main__':
    # start_time =time.time()
    # for i in range(1000):

    # ws = DummyClient('ws://localhost:8887')
    # ws.connect()
    # ws.send("xxx")
    # ws.received_message =xx
    # ws.run_forever()

    main()

    # end_time =time.time()
    # print(start_time - end_time)
