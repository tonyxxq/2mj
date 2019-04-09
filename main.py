import random
from game import Game
from player import Player
import times
import time


def main():
    # 初始化牌局，洗牌
    paiju = Game()

    # 初始化两个选手
    player1 = Player(paiju.fapai(), paiju)
    player2 = Player(paiju.fapai(), paiju)

    # 确定庄、闲，摸牌的顺序，游戏没完成就循环执行, 要么有人胡，要么牌摸完了
    turn = random.random() >= 0.5

    if turn:
        player1.name = 'zhuang'
    else:
        player2.name = 'xian'

    while not paiju.finished:
        # 庄出牌
        if turn:
            pai = player1.chupai_process()
            if paiju.finished:
                player2.score = -player1.score
            else:
                player2.oppo_pai = pai

        # 闲出牌
        else:
            pai = player2.chupai_process()
            if paiju.finished:
                player1.score = -player2.score
            else:
                player1.oppo_pai = pai
        turn = not turn

    print("player1: data", times.restore_pais(player1.data), player1.data, player1.dynamic_pais, " score: ",
          player1.score, player1.fanzhong)
    print("player2: data", times.restore_pais(player2.data), player2.data, player2.dynamic_pais, " score: ",
          player2.score, player2.fanzhong)


if __name__ == '__main__':
    start_time =time.time()
    for i in range(1000):
        main()
    end_time =time.time()
    print(start_time - end_time)
