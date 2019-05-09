import tensorflow as tf
import pickle
import numpy as np
from skimage import io
import cv2 as cv


# 把数据都读取到内存中
def load_file(file):
    with open(file, "rb") as f:
        return pickle.load(f, encoding="bytes")


def inference(x, avg_class, w1, w2, w3, w4, b1, b2, b3, b4):
    if avg_class is None:
        layer1 = tf.nn.relu(tf.nn.conv2d(x, w1, strides=[1, 1, 1, 1], padding="SAME") + b1)
        tf.contrib.layers.batch_norm()
        layer1_d = tf.nn.dropout(layer1, 0.8)
        layer1_pool = tf.nn.max_pool(layer1_d, [1, 2, 2, 1], [1, 2, 2, 1], padding="VALID")

        layer2 = tf.nn.relu(tf.nn.conv2d(layer1_pool, w2, strides=[1, 1, 1, 1], padding="SAME") + b2)
        layer2_d = tf.nn.dropout(layer2, 0.5)
        layer2_pool = tf.nn.max_pool(layer2_d, [1, 2, 2, 1], [1, 2, 2, 1], padding="VALID")

        layer2_flat = tf.reshape(layer2_pool, [-1, 4096])

        layer3 = tf.nn.relu(tf.matmul(layer2_flat, w3) + b3)
        return tf.matmul(layer3, w4) + b4
    else:
        layer1_ = tf.nn.relu(
            tf.nn.conv2d(x, avg_class.average(w1), strides=[1, 1, 1, 1], padding="SAME") + avg_class.average(b1))
        layer1_d_ = tf.nn.dropout(layer1_, 0.8)
        layer1_pool_ = tf.nn.max_pool(layer1_d_, [1, 2, 2, 1], [1, 2, 2, 1], padding="VALID")

        layer2_ = tf.nn.relu(
            tf.nn.conv2d(layer1_pool_, avg_class.average(w2), strides=[1, 1, 1, 1], padding="SAME") + avg_class.average(
                b2))
        layer2_d_ = tf.nn.dropout(layer2_, 0.5)
        layer2_pool_ = tf.nn.max_pool(layer2_d_, [1, 2, 2, 1], [1, 2, 2, 1], padding="VALID")

        layer2_flat_ = tf.reshape(layer2_pool_, [-1, 4096])

        layer3_ = tf.nn.relu(tf.matmul(layer2_flat_, avg_class.average(w3)) + avg_class.average(b3))
        return tf.matmul(layer3_, avg_class.average(w4)) + avg_class.average(b4)


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

w4 = tf.Variable(tf.truncated_normal((256, 10), stddev=0.01))
b4 = tf.Variable(tf.zeros([10]))

global_step = tf.Variable(0, trainable=False)

logits = inference(x, None, w1, w2, w3, w4, b1, b2, b3, b4)

# 损失函数
regularizer = tf.contrib.layers.l2_regularizer(0.001)
regularization = regularizer(w1) + regularizer(w2) + regularizer(w3) + regularizer(w4)

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
logits_ = inference(x, ema, w1, w2, w3, w4, b1, b2, b3, b4)

# 判断准确率
correct_prediction = tf.equal(tf.cast(tf.arg_max(logits_, dimension=1), tf.int32), y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.control_dependencies([train_op_, op_average_variables]):
    train_op = tf.no_op("train")

EPOCH_NUM = 5
BATCH_SIZE = 64
with tf.Session() as sess:
    tf.global_variables_initializer().run()

    for epoch in range(EPOCH_NUM):
        for i in range(len(images) // BATCH_SIZE):
            images_, labels_ = images[i * BATCH_SIZE:(i + 1) * BATCH_SIZE], labels[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
            _m, _loss = sess.run([train_op, loss], feed_dict={x: images_, y: labels_})
            if i % 100 == 0:
                accuracy_ = sess.run([accuracy], feed_dict={x: images_, y: labels_})
                print(accuracy_)

    accuracy_ = sess.run(accuracy, feed_dict={x: test_images, y: test_labels})
    print("EPOCH {} 准确率：{:.3f}".format(epoch + 1, accuracy_))
