import random
from game import game
from player import player


def main():
    # 初始化牌局，洗牌
    paiju = game()

    # 初始化两个选手
    player1 = player(paiju.fapai(), paiju)
    player2 = player(paiju.fapai(), paiju)

    # 摸牌的顺序，游戏没完成就循环执行, 要么有人胡，要么牌摸完了
    turn = random.random() >= 0.5
    while not paiju.finished:
        # 玩家 1 出牌
        if turn:
            pai = player1.chupai_process()
            if paiju.finished:
                player2.score = -player1.score
            else:
                player2.oppo_pai = pai

        # 玩家 2 出牌
        else:
            pai = player2.chupai_process()
            if paiju.finished:
                player1.score = -player2.score
            else:
                player1.oppo_pai = pai
        turn = not turn


    import times

    print(paiju.pais_finished)
    print("player1: data", times.restore_pais(player1.data), player1.data,player1.dynamic_pais, " score: ", player1.score)
    print("player2: data", times.restore_pais(player2.data), player2.data, player2.dynamic_pais, " score: ", player2.score)


if __name__ == '__main__':
    main()
