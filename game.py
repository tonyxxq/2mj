# -*- coding:UTF-8 -*-


import random


class Game:
    def __init__(self):
        # 一共有多少种类型的牌
        self.pai_types = {'WAN_1': 1, 'WAN_2': 2, 'WAN_3': 3, 'WAN_4': 4, 'WAN_5': 5, 'WAN_6': 6, 'WAN_7': 7,
                          'WAN_8': 8, 'WAN_9': 9, 'DONGFENG': 10, 'NANFENG': 11, 'XIFENG': 12, 'BEIFENG': 13,
                          'BAIBAN': 14, 'FACAI': 15, 'HONGZHONG': 16}
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
