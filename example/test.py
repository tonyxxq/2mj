# encoding=utf-8
import tensorflow as tf
import numpy as np

# embeding = tf.contrib.layers.embed_sequence([1, 2, 1, 4], 5, 6)
# inputs = tf.nn.embedding_lookup(embeding, [1, 2])

# x = tf.Variable([[1.0, 2.0]])

# 构建全连接网络
# output_layer = tf.layers.dense(x, 3, kernel_initializer=tf.truncated_normal_initializer(mean=0.1, stddev=0.1))
# mask = tf.sequence_mask([1, 3, 2], 5, dtype=tf.int32)

# tf.placeholder(tf.float32, [None, 2])

# tf.train.Optimizer.compute_gradients(loss,var_list=None, gate_gradients=1,
#                                      aggregation_method=None,
#                                      colocate_gradients_with_ops=False, grad_loss=None)
# tf.train.Optimizer.apply_gradients(grads_and_vars, global_step=None, name=None)
# https://www.jianshu.com/p/de214abd6ee9
# https://blog.csdn.net/u014595019/article/details/52805444
import random

files = tf.train.string_input_producer([r'1.csv'], num_epochs=2, shuffle=True)

reader = tf.TextLineReader()
key, line_content = reader.read(files)

with tf.Session() as sess:
    sess.run(tf.local_variables_initializer())
    coord = tf.train.Coordinator()
    tf.train.start_queue_runners(sess=sess, coord=coord)
    for i in range(10):
        print(sess.run(line_content))
