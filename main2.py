import random
from game import Game
from deepplayer import DeepPlayer
from aiplayer import AiPlayer
import times
from collections import deque
import time
import numpy as np
import tensorflow as tf
import nn

GAME = '2mj'  # the name of the game being played for log files
GAMMA = 0.99  # decay rate of past observations
OBSERVE = 100000.  # timesteps to observe before training
EPSILON = 0.001  # final value of epsilon
REPLAY_MEMORY = 2000  # number of previous transitions to remember
BATCH = 128  # size of minibatch


def main():
    """
    :param memory1: 吃碰杠胡的动作、状态、奖励列表
    :param memory2: 出牌的动作、状态、奖励列表
    """

    memory_jp = deque()
    memory_cp = deque()
    paiju, ai_player, deep_player, turn = init_paju()

    # 创建进牌和出牌神经网络
    pj_status, jp_readout, cp_readout = nn.create_network()

    # 损失函数
    jp_a = tf.placeholder("float", [None, 5])
    jp_y = tf.placeholder("float", [None])
    jp_readout_action = tf.reduce_sum(tf.multiply(jp_readout, jp_a), reduction_indices=1)
    jp_cost = tf.reduce_mean(tf.square(jp_y - jp_readout_action))
    jp_train_step = tf.train.AdamOptimizer(1e-6).minimize(jp_cost)

    cp_a = tf.placeholder("float", [None, 16])
    cp_y = tf.placeholder("float", [None])
    cp_readout_action = tf.reduce_sum(tf.multiply(cp_readout, cp_a), reduction_indices=1)
    cp_cost = tf.reduce_mean(tf.square(cp_y - cp_readout_action))
    cp_train_step = tf.train.AdamOptimizer(1e-6).minimize(cp_cost)

    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())

    print("创建网络完成")

    last_cp_status, last_cp_actions, last_cp_reward = None, None, None
    last_jp_status, last_jp_actions, last_cp_reward = None, None, None

    count = 0
    success = 0
    while True:

        if count == 10000:
            count = 0
            success = 0

        # 牌局已结束，重新开始游戏
        if paiju.finished:
            paiju, ai_player, deep_player, turn = init_paju()
            last_cp_status, last_cp_actions, last_cp_reward = None, None, None
            last_jp_status, last_jp_actions, last_cp_reward = None, None, None

        # 两位玩家依次出牌
        if turn:
            pai = ai_player.chupai_process()
            if paiju.finished:
                deep_player.score = -ai_player.score
            else:
                deep_player.oppo_pai = pai
        else:
            # 进牌状态
            jp_status = get_status(deep_player, ai_player, True)

            # 当前状态输入到神经网络，得到动作，执行得到动作结果状态和回报
            jp_actions = np.zeros([5])
            if len(memory_jp) < 500:
                jp_actions[random.randrange(5)] = 1
            else:
                jp_readout_ = jp_readout.eval(feed_dict={pj_status: [jp_status]})[0]
                jp_action_index = np.argmax(jp_readout_)
                jp_actions[jp_action_index] = 1

            # 动作的选择进行一些探索
            jp_action_index = np.argmax(jp_actions) if random.random() > EPSILON else random.randrange(6)

            # 执行结果得到奖励
            jp_reward = deep_player.jingpai_process(jp_action_index)

            count += 1
            if jp_reward > 0:
                success += 1

            print("总共：", count, "成功：", success)

            # 结合上一次状态存入记忆列表
            if last_jp_status is not None:
                memory_jp.append((last_jp_status, last_jp_actions, last_jp_reword, jp_status, True))

            # 牌局结束没有下一状态，直接存储到记忆中
            if paiju.finished:
                memory_jp.append((jp_status, jp_actions, jp_reward, jp_status, True))
            else:
                # 等到下次进牌的时候一起存入记忆中
                last_jp_status, last_jp_actions, last_jp_reword = jp_status, jp_actions, jp_reward

                # 状态切换到出牌状态
                cp_status = get_status(deep_player, ai_player, False)

                # 出牌状态输入到神经网络获取行动

                # 刚开始的时候随机获取动作
                cp_actions = np.zeros([16])
                if len(memory_jp) < 500:
                    cp_actions[random.randrange(16)] = 1
                else:
                    cp_readout_ = cp_readout.eval(feed_dict={pj_status: [cp_status]})[0]
                    cp_action_index = np.argmax(cp_readout_)
                    cp_actions[cp_action_index] = 1

                # 动作的选择进行一些探索
                cp_action_index = np.argmax(cp_actions) if random.random() > EPSILON else random.randrange(17)

                # 执行出牌动作获取奖励
                pai, cp_reward = deep_player.chupai_process(cp_action_index)

                # 结合上一次的出牌状态一起存入记忆中
                if last_cp_status is not None:
                    memory_cp.append((last_cp_status, last_cp_actions, last_cp_reward, cp_status, False))

                # 牌局结束直接保存状态，因为没有下一个状态了，否则等对家出完牌才知道
                if paiju.finished:
                    memory_cp.append((cp_status, cp_actions, cp_reward, cp_status, False))
                else:
                    last_jp_status, last_jp_actions, last_jp_reword = jp_status, jp_actions, jp_reward
                    ai_player.oppo_pai = pai

        # 训练进牌网络
        if len(memory_cp) > 500 and len(memory_jp) > 500:
            minibatch = random.sample(memory_jp, BATCH)

            s_j_batch = [d[0] for d in minibatch]
            a_batch = [d[1] for d in minibatch]
            r_batch = [d[2] for d in minibatch]
            s_j1_batch = [d[3] for d in minibatch]

            y_batch = []

            # 把状态输入给出牌网络
            readout_j1_batch = jp_readout.eval(feed_dict={pj_status: s_j1_batch})
            for i in range(0, len(minibatch)):
                terminal = minibatch[i][4]
                if terminal:
                    y_batch.append(r_batch[i])
                else:
                    y_batch.append(r_batch[i] + GAMMA * np.max(readout_j1_batch[i]))

            jp_train_step.run(feed_dict={jp_y: y_batch, jp_a: a_batch, pj_status: s_j_batch})

        # 训练出牌网络
        if len(memory_cp) > 500 and len(memory_jp) > 500:
            minibatch = random.sample(memory_cp, BATCH)

            s_j_batch = [d[0] for d in minibatch]
            a_batch = [d[1] for d in minibatch]
            r_batch = [d[2] for d in minibatch]
            s_j1_batch = [d[3] for d in minibatch]

            y_batch = []
            readout_j1_batch = cp_readout.eval(feed_dict={pj_status: s_j1_batch})
            for i in range(0, len(minibatch)):
                terminal = minibatch[i][4]
                if terminal:
                    y_batch.append(r_batch[i])
                else:
                    y_batch.append(r_batch[i] + GAMMA * np.max(readout_j1_batch[i]))

            cp_train_step.run(feed_dict={cp_y: y_batch, cp_a: a_batch, pj_status: s_j_batch})

        # 切换下家出牌
        turn = not turn


def push_memory(memory, status, actions, reward, next_status, terminal):
    """
    把状态和奖励值存入记忆列表
    """
    memory.append((status, actions, reward, next_status, terminal))

    if memory > REPLAY_MEMORY:
        memory.popleft()


def get_status(my_player, oppo_player, is_jp):
    """
    结果是一个 16 x 16 x 6 的张量
    行作为每一张牌(不足补零, 多了裁掉)，列作为牌的大小（从１到１６）
    my_dynamic_pais  16 x 16  我的动态牌
    my_static_pais   16 x 16  我的静态牌
    my_output_pais   16 x 16  我出的所有牌
    oppo_static_pais 16 x 16  对手的静态牌
    oppo_output_pais 16 x 16  对手出的所有的牌
    oppo_pai         16 x 16　对家新出的牌
    
    :param my_player:   玩家自己
    :param oppo_player: 对家
    :return: 状态张量
    """

    status = np.zeros([16, 16, 6])
    for index, value in enumerate(sorted(my_player.dynamic_pais)):
        status[index, value - 1, 0] = 1

    for index, value in enumerate(sorted(times.restore_pais(my_player.data))):
        status[index, value - 1, 1] = 1

    for index, value in enumerate(sorted(my_player.output_pais)):
        if index < 16:
            status[index, value - 1, 2] = 1

    for index, value in enumerate(sorted(times.restore_pais(oppo_player.data))):
        status[index, value - 1, 3] = 1

    for index, value in enumerate(sorted(oppo_player.output_pais)):
        if index < 16:
            status[index, value - 1, 4] = 1

    if is_jp:
        status[index, 0, 5] = 1
    else:
        status[index, 1, 5] = 0

    return status


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
