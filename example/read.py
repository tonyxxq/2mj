import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
import random
from tensorflow.examples.tutorials.mnist import input_data
import cv2


#
# # 输入：1张图片，尺寸 28*28 高宽，通道数 3
# x = np.ones((1, 28, 28, 3), dtype=np.float32)
#
# # 卷积核尺寸 4x4 ，5表输出通道数，3代表输入通道数
# w = np.ones((4, 4, 5, 3), dtype=np.float32)
#
# # 扩大2倍
# output = tf.nn.conv2d_transpose(x, w, (1, 84, 84, 5), [1, 3, 3, 1], padding='SAME')
#
# with tf.Session() as sess:
#     m = sess.run(output)
#     print(m.shape)

def _in64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


# # 读入 mnist 文件，转换为 TFRecord
# data = input_data.read_data_sets("MNIST_data", one_hot=False)

# # 把数据分成 4 部分
# images = np.reshape(data.train.images, [4, -1, 784])
# labels = np.reshape(data.train.labels, [4, -1])
#
# count = 1
# for image_batch, label_batch in zip(images, labels):
#     writer = tf.python_io.TFRecordWriter("mnist_tfr_{:}_of_4".format(count))
#     for image, label in zip(image_batch, label_batch):
#         example = tf.train.Example(
#             features=tf.train.Features(
#                 feature={
#                     'image_raw': _bytes_feature(image.tostring()),
#                     'label': _in64_feature(label)
#                 }))
#         writer.write(example.SerializeToString())
#     count += 1
#     writer.close()


# writer = tf.python_io.TFRecordWriter("mnist_tfr_test")
# for image, label in zip(data.test.images, data.test.labels):
#     example = tf.train.Example(
#         features=tf.train.Features(
#             feature={
#                 'image_raw': _bytes_feature(image.tostring()),
#                 'label': _in64_feature(label)
#             }))
#     writer.write(example.SerializeToString())
# writer.close()

def inference(images, reuse):
    """
    前向传播网络
    """
    with tf.variable_scope("layer1", reuse=reuse):
        w1 = tf.get_variable(name="w1", shape=(784, 512), initializer=tf.truncated_normal_initializer(stddev=0.1))
        b1 = tf.get_variable(name="b1", shape=(512,), initializer=tf.zeros_initializer())
        layer_1_t = tf.nn.relu(tf.add(tf.matmul(images, w1), b1))

    with tf.variable_scope("layer2", reuse=reuse):
        w2 = tf.get_variable(name="w2", shape=(512, 218), initializer=tf.truncated_normal_initializer(stddev=0.1))
        b2 = tf.get_variable(name="b2", shape=(218,), initializer=tf.zeros_initializer())
        layer_2_t = tf.nn.relu(tf.add(tf.matmul(layer_1_t, w2), b2))

    with tf.variable_scope("output", reuse=reuse):
        w3 = tf.get_variable(name="w3", shape=(218, 10), initializer=tf.truncated_normal_initializer(stddev=0.1))
        b3 = tf.get_variable(name="b3", shape=(10,), initializer=tf.zeros_initializer())
        logits = tf.add(tf.matmul(layer_2_t, w3), b3, name="logits")

    return logits


def read_tfr_data(path):
    """
    读取数据
    """
    files = tf.train.match_filenames_once(path)
    files_queue = tf.train.string_input_producer(files, shuffle=True, num_epochs=5)

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(files_queue)

    example = tf.parse_single_example(
        serialized=serialized_example,
        features={
            'image_raw': tf.FixedLenFeature([], tf.string),
            'label': tf.FixedLenFeature([], tf.int64)
        }
    )

    # string 必须进行 decode
    image = tf.decode_raw(example['image_raw'], tf.float32)
    label = tf.cast(example['label'], tf.int64)

    return image, label


# 训练数据
train_image, train_label = read_tfr_data("mnist_tfr_*")
processed_train_img = tf.reshape(train_image, (784,))
BATCH_SIZE = 128
capacity = 1000 + 3 * BATCH_SIZE
train_labels, train_images = tf.train.batch([train_label, processed_train_img], BATCH_SIZE, num_threads=1,
                                            capacity=capacity)
# 前向传播
train_logits = inference(train_images, False)

with tf.variable_scope("loss"):
    loss = tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=train_labels, logits=train_logits),
                         name="loss")

    # 加上正则化项
    # regularizer = tf.contrib.layers.l2_regularizer(0.001)
    # regularization = regularizer(w1) + regularizer(w2)
    # loss += regularization

# minimize 的 global_step 会自动递增
with tf.variable_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.001).minimize(loss)


# 测试数据
test_image, test_label = read_tfr_data("mnist_tfr_test")
processed_test_img = tf.reshape(test_image, (784,))
test_labels, test_images = tf.train.batch([test_label, processed_test_img], 5000, num_threads=1,
                                          capacity=5000)

test_logits = inference(test_images, True)

# 准确率
with tf.variable_scope("accuracy"):
    correct_prediction = tf.equal(test_labels, tf.argmax(test_logits, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    sess.run(tf.local_variables_initializer())
    tf.global_variables_initializer().run()

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord, sess=sess)

    # 训练
    try:
        while not coord.should_stop():
            sess.run(train_step)
    except tf.errors.OutOfRangeError:
        print("训练完成")
    finally:
        coord.request_stop()

    # 测试
    print("测试集准确率 {:.3f}".format(sess.run(accuracy)))

coord.join(threads)
