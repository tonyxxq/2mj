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

sess = tf.InteractiveSession()

x = tf.constant([[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]])
print("before shape：", x.get_shape())
print(sess.run(x))

y = tf.squeeze(x)
print("after shape：", y.get_shape())
print(sess.run(y))

# 也可指定要移除的维度
z = tf.squeeze(x, [0])
print(sess.run(z))