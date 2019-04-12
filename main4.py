#!/bin/python
from roomai.common import *
from roomai.kuhn import KuhnPokerEnv
import random


class KuhnPokerExamplePlayer(AbstractPlayer):
    def receive_info(self, info):
        print(info)
        if info.person_state_history[-1].available_actions is not None:
            self.available_actions = info.person_state_history[-1].available_actions

    def take_action(self):
        values = self.available_actions.values()
        return list(values)[int(random.random() * len(values))]

    def reset(self):
        pass


if __name__ == "__main__":
    players = [KuhnPokerExamplePlayer() for i in range(2)] + [RandomPlayerChance()]
    # RandomChancePlayer is the chance player with the uniform distribution over every output
    env = KuhnPokerEnv()
    scores = env.compete(env, players)
    print(scores)
