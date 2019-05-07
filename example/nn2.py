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

w1 = tf.Variable(tf.truncated_normal((2, 1), stddev=0.1), name="w1")
b1 = tf.Variable(tf.zeros([1]))

layer_1 = tf.add(tf.matmul(x, w1), b1)
layer_1_r = tf.nn.relu(layer_1)

loss = tf.reduce_mean(tf.square(layer_1_r - y))
# 分解成两步
# train_op = tf.train.GradientDescentOptimizer(0.001).minimize(loss)
(gradient, variable) = tf.train.Optimizer.compute_gradients(loss=loss)

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    for epoch in range(5000):
        X, Y = get_batches()
        _, loss_ = sess.run([gradient, loss], feed_dict={x: X, y: Y})

        if epoch % 100 == 0:
            y_test = sess.run([layer_1_r], feed_dict={x: [[0.5, 0.5]]})
            y_real = pow(0.5, 2) + 2 * 0.5 + 1 + random.gauss(0, sigma=0.001)
            print(y_test, y_real, loss_)
