import tensorflow as tf
import random


# 准备数据
def get_batches():
    X = []
    Y = []
    for i in range(5000):
        x1 = random.random()
        x2 = random.random()
        y = pow(x1, 2) + 2 * x2 + 1 + random.gauss(0, sigma=0.001)
        X.append([x1, x2])
        Y.append([y])
    return X, Y


# 创建计算图
x = tf.placeholder(tf.float32, [None, 2], name="x")
y = tf.placeholder(tf.float32, [None, 1], name="y")

w1 = tf.Variable(tf.truncated_normal((2, 3), stddev=0.1), name="w1")
b1 = tf.Variable(tf.zeros([3]))
w2 = tf.Variable(tf.truncated_normal((3, 10), stddev=0.1), name="w2")
b2 = tf.Variable(tf.zeros([10]))
w3 = tf.Variable(tf.truncated_normal((10, 1), stddev=0.1), name="w3")
b3 = tf.Variable(tf.zeros([1]))

layer_1 = tf.add(tf.matmul(x, w1), b1)
layer_1_r = tf.nn.relu(layer_1)

layer_2 = tf.add(tf.matmul(layer_1_r, w2), b2)
layer_2_r = tf.nn.relu(layer_2)
layer_2_d = tf.nn.dropout(layer_2_r, 0.5)

layer_3 = tf.add(tf.matmul(layer_2_d, w3), b3)
layer_3_r = tf.nn.relu(layer_3)

loss = tf.reduce_mean(tf.square(layer_3_r - y))
train_op = tf.train.GradientDescentOptimizer(0.001).minimize(loss)

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    for epoch in range(5000):
        X, Y = get_batches()
        _, loss_ = sess.run([train_op, loss], feed_dict={x: X, y: Y})

        if epoch % 100 == 0:
            y_test = sess.run([layer_3_r], feed_dict={x: [[0.5, 0.5]]})
            y_real = pow(0.5, 2) + 2 * 0.5 + 1 + random.gauss(0, sigma=0.001)
            print(y_test, y_real, loss_)
