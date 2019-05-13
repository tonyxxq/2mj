import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


# # 写入 TFRecord
# mnist = input_data.read_data_sets("MNIST_data", dtype=tf.uint8, one_hot=True)
# images = mnist.train.images
# labels = mnist.train.labels
# pixels = images.shape[1]
# num_examples = mnist.train.num_examples
#
# filename = "output_tfrecords"
# writer = tf.python_io.TFRecordWriter(filename)
# for index in range(num_examples):
#     image_raw = images[index].tostring()
#     example = tf.train.Example(features=tf.train.Features(feature={
#         'pixels': _int64_feature(pixels),
#         'label': _int64_feature(np.argmax(labels[index])),
#         'image_raw': _bytes_feature(image_raw)
#     }))
#     writer.write(example.SerializeToString())
#
# writer.close()
#
# # 读取 TFRecord
# filenam_name = tf.train.string_input_producer(["output_tfrecords"])
#
# # 读取单个样例
# reader = tf.TFRecordReader()
# _, serialized_example = reader.read(filenam_name)
# features = tf.parse_single_example(
#     serialized_example,
#     features={
#         'image_raw': tf.FixedLenFeature([], tf.string),
#         'pixels': tf.FixedLenFeature([], tf.int64),
#         'label': tf.FixedLenFeature([], tf.int64),
#     }
# )
#
# # 解析字符串为对应的图像对应的像素数组
# images_ = tf.decode_raw(features['image_raw'], tf.uint8)
# images_r = tf.reshape(images_, (28, 28))
# pixels_ = tf.cast(features['pixels'], tf.int32)
# labels_ = tf.cast(features['label'], tf.int32)
#
# import matplotlib.pyplot as plt
#
# with tf.Session() as sess:
#     coord = tf.train.Coordinator()
#     threads = tf.train.start_queue_runners(sess=sess, coord=coord)
#     for i in range(10):
#         image, pixel, label = sess.run([images_r, pixels_, labels_])
#         plt.imshow(image, cmap='gray')
#         plt.show()

# 把 cifar 数据转为 tfrecord


