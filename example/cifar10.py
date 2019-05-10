import tensorflow as tf
import pickle
import numpy as np
import cv2 as cv
import random


# 把数据都读取到内存中
def load_file(file):
    with open(file, "rb") as f:
        return pickle.load(f, encoding="bytes")


def inference(x, avg_class, w1, w2, w3, w4, w5, b1, b2, b3, b4, b5):
    if avg_class is None:
        conv_1 = tf.nn.conv2d(x, w1, strides=[1, 1, 1, 1], padding="SAME")
        conv_1_bias = tf.nn.bias_add(conv_1, b1)
        conv_1_relu = tf.nn.relu(conv_1_bias)
        conv_1_pool = tf.nn.max_pool(conv_1_relu, [1, 2, 2, 1], [1, 2, 2, 1], padding="SAME")
        conv_1_bn = tf.contrib.layers.batch_norm(conv_1_pool)

        conv_2 = tf.nn.conv2d(conv_1_bn, w2, strides=[1, 1, 1, 1], padding="SAME")
        conv_2_bias = tf.nn.bias_add(conv_2, b2)
        conv_2_relu = tf.nn.relu(conv_2_bias)
        conv_2_pool = tf.nn.max_pool(conv_2_relu, [1, 2, 2, 1], [1, 2, 2, 1], padding="SAME")
        conv_2_bn = tf.contrib.layers.batch_norm(conv_2_pool)

        shape = conv_2_bn.get_shape().as_list()
        nodes = shape[1] * shape[2] * shape[3]
        fc_flat = tf.reshape(conv_2_bn, [-1, nodes])

        fc_1 = tf.matmul(fc_flat, w3) + b3
        fc_1_relu = tf.nn.relu(fc_1)
        fc_1_dropout = tf.nn.dropout(fc_1_relu, 0.8)
        fc_1_bn = tf.contrib.layers.batch_norm(fc_1_dropout)

        return tf.matmul(fc_1_bn, w4) + b4
    else:
        conv_1 = tf.nn.conv2d(x, avg_class.average(w1), strides=[1, 1, 1, 1], padding="SAME")
        conv_1_bias = tf.nn.bias_add(conv_1, avg_class.average(b1))
        conv_1_relu = tf.nn.relu(conv_1_bias)
        conv_1_pool = tf.nn.max_pool(conv_1_relu, [1, 2, 2, 1], [1, 2, 2, 1], padding="SAME")
        conv_1_bn = tf.contrib.layers.batch_norm(conv_1_pool)

        conv_2 = tf.nn.conv2d(conv_1_bn, avg_class.average(w2), strides=[1, 1, 1, 1], padding="SAME")
        conv_2_bias = tf.nn.bias_add(conv_2, avg_class.average(b2))
        conv_2_relu = tf.nn.relu(conv_2_bias)
        conv_2_pool = tf.nn.max_pool(conv_2_relu, [1, 2, 2, 1], [1, 2, 2, 1], padding="SAME")
        conv_2_bn = tf.contrib.layers.batch_norm(conv_2_pool)

        shape = conv_2_bn.get_shape().as_list()
        nodes = shape[1] * shape[2] * shape[3]
        fc_flat = tf.reshape(conv_2_bn, [-1, nodes])

        fc_1 = tf.matmul(fc_flat, avg_class.average(w3)) + avg_class.average(b3)
        fc_1_relu = tf.nn.relu(fc_1)
        fc_1_bn = tf.contrib.layers.batch_norm(fc_1_relu)

        return tf.matmul(fc_1_bn, avg_class.average(w4)) + avg_class.average(b4)


# 加载数据
b1 = load_file("./CIFAR10_data/data_batch_1")
b2 = load_file("./CIFAR10_data/data_batch_2")
b3 = load_file("./CIFAR10_data/data_batch_3")
b4 = load_file("./CIFAR10_data/data_batch_4")
b5 = load_file("./CIFAR10_data/data_batch_5")

images = np.concatenate((b1[b"data"], b2[b"data"], b3[b"data"], b4[b"data"], b5[b"data"]))
images = images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
labels = np.concatenate((b1[b"labels"], b2[b"labels"], b3[b"labels"], b4[b"labels"], b5[b"labels"]))

b_test = load_file("./CIFAR10_data/test_batch")
test_images = b_test[b"data"]
test_images = test_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
test_labels = b_test[b"labels"]

# cv.imshow("xx", images[0])
# cv.waitKey(0)

# 创建计算图
x = tf.placeholder(tf.float32, (None, 32, 32, 3))
y = tf.placeholder(tf.int32)

w1 = tf.Variable(tf.truncated_normal((3, 3, 3, 32), stddev=0.01))
b1 = tf.Variable(tf.zeros([32]))

w2 = tf.Variable(tf.truncated_normal((3, 3, 32, 64), stddev=0.01))
b2 = tf.Variable(tf.zeros([64]))

w3 = tf.Variable(tf.truncated_normal((4096, 256), stddev=0.01))
b3 = tf.Variable(tf.zeros([256]))

w4 = tf.Variable(tf.truncated_normal((256, 128), stddev=0.01))
b4 = tf.Variable(tf.zeros([128]))

w5 = tf.Variable(tf.truncated_normal((128, 10), stddev=0.01))
b5 = tf.Variable(tf.zeros([10]))

global_step = tf.Variable(0, trainable=False)

logits = inference(x, None, w1, w2, w3, w4, w5, b1, b2, b3, b4, b5)

# 损失函数
regularizer = tf.contrib.layers.l2_regularizer(0.001)
regularization = regularizer(w3) + regularizer(w4)

loss_ = tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits))
loss = loss_ + regularization

# 学习率衰减
learning_rate = tf.train.exponential_decay(
    0.0001,
    global_step,
    200,
    0.99,
    staircase=True
)

# 优化
train_op_ = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

# 滑动模型
ema = tf.train.ExponentialMovingAverage(0.99, global_step)
op_average_variables = ema.apply(tf.trainable_variables())

# 预测，使用影子变量
logits_ = inference(x, ema, w1, w2, w3, w4, w5, b1, b2, b3, b4, b5)

# 判断准确率
correct_prediction = tf.equal(tf.cast(tf.arg_max(logits_, dimension=1), tf.int32), y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
# with tf.control_dependencies(update_ops):
#     train_op = optimizer.minimize(loss)

with tf.control_dependencies([train_op_, op_average_variables]):
    train_op = tf.no_op("train")

EPOCH_NUM = 8
BATCH_SIZE = 64
with tf.Session() as sess:
    tf.global_variables_initializer().run()

    for epoch in range(EPOCH_NUM):
        # # 打乱顺序且保留对应关系
        # random.seed(epoch)
        # random.shuffle(images)
        #
        # random.seed(epoch)
        # random.shuffle(labels)
        for i in range(len(images) // BATCH_SIZE):
            images_, labels_ = images[i * BATCH_SIZE:(i + 1) * BATCH_SIZE], labels[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
            _m, _loss = sess.run([train_op, loss], feed_dict={x: images_, y: labels_})
            if i % 100 == 0:
                accuracy_ = sess.run([accuracy], feed_dict={x: images_, y: labels_})
                print(accuracy_)

    accuracy_ = sess.run(accuracy, feed_dict={x: test_images, y: test_labels})
    print("EPOCH {} 准确率：{:.2f}".format(epoch + 1, accuracy_))
