import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])

w1 = tf.Variable(tf.truncated_normal((784, 512), stddev=0.1))
b1 = tf.Variable(tf.zeros(512))

w2 = tf.Variable(tf.truncated_normal((512, 218), stddev=0.1))
b2 = tf.Variable(tf.zeros(218))

w3 = tf.Variable(tf.truncated_normal((218, 10), stddev=0.1))
b3 = tf.Variable(tf.zeros(10))

global_step = tf.Variable(0, dtype=tf.int32, trainable=False)

# 训练时使用原始变量
layer_1_t = tf.nn.relu(tf.add(tf.matmul(x, w1), b1))
layer_2_t = tf.nn.relu(tf.add(tf.matmul(layer_1_t, w2), b2))
logits = tf.add(tf.matmul(layer_2_t, w3), b3)
loss = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits))

# 加上正则化项
regularizer = tf.contrib.layers.l2_regularizer(0.001)
regularization = regularizer(w1) + regularizer(w2)
loss += regularization

# 学习率衰减
learning_rate = tf.train.exponential_decay(
    0.001,
    global_step,
    100,
    0.99,
    staircase=True
)

# minimize 的 global_step 会自动递增
train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

# 滑动模型
ema = tf.train.ExponentialMovingAverage(0.99, global_step)
op_average_variables = ema.apply(tf.trainable_variables())

# 预测时使用影子变量
layer_1_p = tf.nn.relu(tf.add(tf.matmul(x, ema.average(w1)), ema.average(b1)))
layer_2_p = tf.nn.relu(tf.add(tf.matmul(layer_1_p, ema.average(w2)), ema.average(b2)))
logits_average = tf.add(tf.matmul(layer_2_p, ema.average(w3)), ema.average(b3))

# 反向传播之后再更新每一个参数的滑动平均值
with tf.control_dependencies([train_step, op_average_variables]):
    train_op = tf.no_op("train")

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    for i in range(2000):
        xs, ys = mnist.train.next_batch(400)
        _, lr = sess.run([train_op, learning_rate], feed_dict={x: xs, y: ys})
        print(lr)
        # 验证
        if i % 100 == 0:
            xs_, ys_ = mnist.validation.images, mnist.validation.labels
            logits_ = sess.run(logits_average, feed_dict={x: xs_})
            correct_prediction = tf.equal(tf.argmax(ys_, 1), tf.argmax(logits_, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            print("训练次数 {}, 准确率 {:.3f}".format(i, accuracy.eval()))

            # 保存模型参数
            tf.train.Saver().save(sess, "save/mnist")

    # 测试
    xs_test, ys_test = mnist.test.images, mnist.test.labels
    logits_ = sess.run(logits_average, feed_dict={x: xs_test})
    correct_prediction = tf.equal(tf.argmax(ys_test, 1), tf.argmax(logits_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print("测试集准确率 {:.3f}".format(accuracy.eval()))


