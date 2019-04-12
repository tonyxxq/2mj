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
REPLAY_MEMORY = 200  # number of previous transitions to remember
BATCH = 64  # size of minibatch


def main():
    """
    :param memory1: 吃碰杠胡的动作、状态、奖励列表
    :param memory2: 出牌的动作、状态、奖励列表
    """

    memory_jp = deque()
    memory_cp = deque()
    paiju, ai_player, deep_player, turn = init_paju()

    # 创建进牌和出牌神经网络
    jp_s, jp_readout = nn.create_jp_network()
    cp_s, cp_readout = nn.create_cp_network()

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
    cp_all_reward, jp_all_reward, count_cp, count_jp = 0, 0, 0, 0
    while True:
        # 牌局已结束，重新开始游戏
        if paiju.finished:
            paiju, ai_player, deep_player, turn = init_paju()
            last_cp_status, last_cp_actions, last_cp_reward = None, None, None

        # 两位玩家依次出牌
        if turn:
            pai = ai_player.chupai_process()
            if paiju.finished:
                deep_player.score = -ai_player.score
            else:
                deep_player.oppo_pai = pai

            # 状态转存到记忆中
            if ai_player.oppo_pai is not None:
                cp_status = get_status(deep_player, ai_player, False)
                push_memory(memory_cp, last_cp_status, last_cp_actions, last_cp_reward, cp_status, False)
        else:
            # 进牌状态
            jp_status = get_status(deep_player, ai_player, True)

            # 进牌状态输入到进牌神经网络，得到动作列表，动作的选择进行一些探索
            jp_readout_ = jp_readout.eval(feed_dict={jp_s: [jp_status]})[0]
            jp_action_index = np.argmax(jp_readout_) if random.random() > EPSILON else random.randrange(5)

            # 动作列表转换为 one hot
            jp_actions = np.zeros([5])
            jp_actions[jp_action_index] = 1

            # 执行结果得到奖励
            jp_reward = deep_player.jingpai_process(jp_action_index)

            count_jp += 1

            if count_jp % 200 == 0:
                print("进牌总次数：", count_jp, "总奖励值：", jp_all_reward)
                jp_all_reward = 0
            else:
                jp_all_reward += jp_reward

            # 状态切换到出牌状态，并把进牌状态、奖励转存到记忆中
            cp_status = get_status(deep_player, ai_player, False)
            push_memory(memory_jp, jp_status, jp_actions, jp_reward, cp_status, paiju.finished)

            # 牌局没有结束，进行出牌动作
            if not paiju.finished:
                # 出牌状态输入到神经网络获取行动，并进行一些探索
                cp_readout_ = cp_readout.eval(feed_dict={cp_s: [cp_status]})[0]
                cp_action_index = np.argmax(cp_readout_) if random.random() > EPSILON else random.randrange(17)

                # 转化为 one hot
                cp_actions = np.zeros([16])
                cp_actions[cp_action_index] = 1

                # 执行出牌动作获取奖励
                pai, cp_reward = deep_player.chupai_process(cp_action_index)

                count_cp += 1

                if count_cp % 200 == 0:
                    print("出牌总次数：", count_cp, "总奖励值：", cp_all_reward)
                    cp_all_reward = 0
                else:
                    cp_all_reward += cp_reward

                jp_reward += cp_reward

                # 牌局结束直接保存状态，因为没有下一个状态了，否则等对家出完牌才知道
                if paiju.finished:
                    push_memory(memory_cp, cp_status, cp_actions, cp_reward, cp_status, True)
                else:
                    last_cp_status, last_cp_actions, last_cp_reward = cp_status, cp_actions, cp_reward
                    ai_player.oppo_pai = pai

        # 训练进牌网络
        if len(memory_jp) >= REPLAY_MEMORY:
            # 从进牌记忆数据中随机抽取一个批次的训练数据
            jp_batch = random.sample(memory_jp, BATCH)

            jp_s_ = [d[0] for d in jp_batch]
            jp_a_ = [d[1] for d in jp_batch]

            # 计算 Q 值
            jp_y_ = []
            for r in jp_batch:
                terminal = r[4]
                if terminal:
                    jp_y_.append(r[2])
                else:
                    # 把状态输入给出牌网络，获取 Q 值
                    cp_readout_ = cp_readout.eval(feed_dict={cp_s: [r[3]]})
                    jp_y_.append(r[2] + GAMMA * np.max(cp_readout_))

            jp_train_step.run(feed_dict={jp_s: jp_s_, jp_a: jp_a_, jp_y: jp_y_})

        # 训练出牌网络
        if len(memory_cp) >= REPLAY_MEMORY:
            # 从出牌记忆数据中随机抽取一个批次的训练数据
            cp_batch = np.array(random.sample(memory_cp, BATCH))

            cp_s_ = [d[0] for d in cp_batch]
            cp_a_ = [d[1] for d in cp_batch]

            # 计算 Q 值
            cp_y_ = []
            for r in cp_batch:
                terminal = r[4]
                if terminal:
                    cp_y_.append(r[2])
                else:
                    # 把状态输入给出牌网络，获取 Q 值
                    jp_readout_ = jp_readout.eval(feed_dict={jp_s: [r[3]]})
                    cp_y_.append(r[2] + GAMMA * np.max(jp_readout_))

            cp_train_step.run(feed_dict={cp_s: cp_s_, cp_a: cp_a_, cp_y: cp_y_})

        # 切换下家出牌
        turn = not turn


def push_memory(memory, status, actions, reward, next_status, terminal):
    """
    把状态和奖励值存入记忆列表
    """
    memory.append((status, actions, reward, next_status, terminal))

    if len(memory) > REPLAY_MEMORY:
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
