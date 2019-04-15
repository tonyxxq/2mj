# -*- coding:UTF-8 -*-


import tensorflow as tf


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.01)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.01, shape=shape)
    return tf.Variable(initial)


def conv2d(x, w, stride):
    return tf.nn.conv2d(x, w, strides=[1, stride, stride, 1], padding="SAME")


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")


def create_jp_network():
    """
    创建进牌神经网络结构
    """

    W_conv1 = weight_variable([4, 4, 6, 32])
    b_conv1 = bias_variable([32])

    W_conv2 = weight_variable([3, 3, 32, 64])
    b_conv2 = bias_variable([64])

    W_conv3 = weight_variable([2, 2, 64, 64])
    b_conv3 = bias_variable([64])

    W_fc1 = weight_variable([1024, 256])
    b_fc1 = bias_variable([256])

    W_fc2 = weight_variable([256, 5])
    b_fc2 = bias_variable([5])

    # input layer
    jp_status = tf.placeholder("float", [None, 16, 16, 6])

    # hidden layers
    h_conv1 = tf.nn.relu(conv2d(jp_status, W_conv1, 1) + b_conv1)

    h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2, 2) + b_conv2)

    h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3, 2) + b_conv3)

    h_conv3_flat = tf.reshape(h_conv3, [-1, 1024])

    h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, W_fc1) + b_fc1)

    jp_readout = tf.matmul(h_fc1, W_fc2) + b_fc2

    return jp_status, jp_readout


def create_cp_network():
    """
    创建出牌神经网络结构
    """

    W_conv1 = weight_variable([4, 4, 6, 32])
    b_conv1 = bias_variable([32])

    W_conv2 = weight_variable([3, 3, 32, 64])
    b_conv2 = bias_variable([64])

    W_conv3 = weight_variable([2, 2, 64, 64])
    b_conv3 = bias_variable([64])

    W_fc1 = weight_variable([1024, 256])
    b_fc1 = bias_variable([256])

    W_fc2 = weight_variable([256, 16])
    b_fc2 = bias_variable([16])

    # input layer
    cp_status = tf.placeholder("float", [None, 16, 16, 6])

    # hidden layers
    h_conv1 = tf.nn.relu(conv2d(cp_status, W_conv1, 1) + b_conv1)

    h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2, 2) + b_conv2)

    h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3, 2) + b_conv3)

    h_conv3_flat = tf.reshape(h_conv3, [-1, 1024])

    h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, W_fc1) + b_fc1)

    cp_readout = tf.matmul(h_fc1, W_fc2) + b_fc2

    return cp_status, cp_readout

