import tensorflow as tf

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
sess = tf.InteractiveSession()

x = tf.Variable(tf.truncated_normal((2, 2)))
global_step = tf.Variable(0, trainable=False)

ema = tf.train.ExponentialMovingAverage(0.99, global_step)

print(tf.trainable_variables())

ema.apply(tf.trainable_variables())
tf.global_variables_initializer().run()

print(x.eval())
print(ema.average(x).eval())

