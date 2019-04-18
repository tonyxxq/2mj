# -*- coding:UTF-8 -*-


import random


class Game:
    def __init__(self):
        # 一共有多少种类型的牌
        self.pai_types = {'1万': 1, '2万': 2, '3万': 3, '4万': 4, '5万': 5, '6万': 6, '7万': 7,
                          '8万': 8, '9万': 9, '东': 10, '南': 11, '西': 12, '北': 13,
                          '白': 14, '发': 15, '中': 16}
        self.type_pais = {item[1]: item[0] for item in self.pai_types.items()}
        self.pais = self.gengerate_pais()  # 生成一副牌
        self.finished = False  # 结束，有人胡或没有牌了
        self.pais_finished = False  # 没有牌了结束

    def gengerate_pais(self):
        """
        生成一副牌
        """
        pais = [v for v in list(self.pai_types.values()) for i in range(0, 4)]
        random.shuffle(pais)
        return pais

    def mopai(self):
        """
        摸牌
        """
        return self.pais.pop()

    def fapai(self):
        """
        首次发牌，一共 13 张
        """
        return [self.pais.pop() for i in range(0, 13)]

    def num2Str(self, tiles):
        """
        把编号转换为指定的牌名
        """
        return ','.join([self.type_pais[tile] for tile in tiles])


if __name__ == '__main__':
    game = Game()
    print(game.num2Str([1, 2, 3, 16]))
