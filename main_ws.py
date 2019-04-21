import random

from ws4py.client.threadedclient import WebSocketClient

from myplayer import MyPlayer
from game import Game
from wsplayer import WSPlayer
import times
import time


def main():
    """
    :param memory1: 吃碰杠胡的动作、状态、奖励列表
    :param memory2: 出牌的动作、状态、奖励列表
    """

    # 建立 websocket 连接
    ws = DummyClient('ws://localhost:8887')
    ws.connect()
    for i in range(10):
        # 初始化牌局，洗牌，初始化两个选手
        paiju = Game()
        myplayer = MyPlayer(paiju.fapai(), paiju)
        wsplayer = WSPlayer(paiju.fapai(), paiju, ws)

        # 确定庄、闲，摸牌的顺序，游戏没完成就循环执行, 要么有人胡，要么牌摸完了
        turn = random.random() >= 0.5
        if turn:
            myplayer.name = 'zhuang'
            wsplayer.name = 'xian'
        else:
            wsplayer.name = 'zhuang'
            myplayer.name = 'xian'

        while not paiju.finished:
            if turn:
                pai = myplayer.chupai_process()
                if paiju.finished:
                    wsplayer.score = -myplayer.score
                else:
                    wsplayer.oppo_pai = pai
            else:
                wsplayer.chupai_process(ws)
                if paiju.finished:
                    myplayer.score = -wsplayer.score
                else:
                    time.sleep(2)
                    myplayer.oppo_pai = wsplayer.last_chupai
                    print("---------------------------")
                    print("对家出牌：", paiju.type_pais[wsplayer.last_chupai])
                    # print("对家手上的牌", list(map(lambda p: paiju.type_pais[p], sorted(wsplayer.dynamic_pais))))
                    print("---------------------------")
            turn = not turn

        print("myplayer: data", times.restore_pais(myplayer.data), myplayer.fanzhong, "得分", myplayer.score)
        print("wsplayer: data", times.restore_pais(wsplayer.data), wsplayer.fanzhong, "得分", wsplayer.score)

    # webscoket 一直建立连接
    ws.run_forever()


class DummyClient(WebSocketClient):
    def opened(self):
        # print("connected")
        pass

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
