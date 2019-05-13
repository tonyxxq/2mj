import tensorflow as tf
import threading
import random
import time


# 创建　FIFIQUEUE
# fifo = tf.FIFOQueue(100, tf.float32)
# init = fifo.enqueue_many(([[5., 6., 8.]],))
# x = fifo.dequeue() # RandomShuffleQueue 从列表中随机选择一个元素
# y = x + 1
# enq = fifo.enqueue([y])
#
# with tf.Session() as sess:
#     sess.run(init)
#     print(fifo.size().eval())
#     for i in range(5):
#         y_, _ = sess.run([y, enq])
#         print(y_)

# 多个线程协同完成任务　Coordinator 和　QueueRunner
# def my_loop(cood, workid):
#     while not cood.should_stop():
#         if random.random() < 0.1:
#             cood.request_stop()
#         else:
#             print("线程 {}".format(workid))
#         time.sleep(1)
#
#
# # Coordinator 协同多个线程
# cood = tf.train.Coordinator()
#
# # 创建读个线程
# threads = [threading.Thread(target=my_loop, args=(cood, i,)) for i in range(5)]
#
# # 启动线程
# for thread in threads:
#     thread.start()
#
# # 等待所有线程退出
# cood.join(threads)


# 使用 QueueRunner 启动多个线程操作同一个队列
# fifo = tf.FIFOQueue(100, tf.float32, shapes=[1])
# 复杂点的, shapes　表示队列中每个元素的　shape
# fifo = tf.FIFOQueue(100, dtypes=tf.float32, shapes=[2, 1])
#
# # 队列中加入随机数，随机数需要使用　tf.random，如果使用　random 类的随机数每次入队的值都相同
# enqueue = fifo.enqueue(tf.random.truncated_normal([2, 1]))
#
# # 第一个参数表示队列，第二个参数表示操作（下面启动了 5 个线程进行 enqueue 操作）
# runner = tf.train.QueueRunner(fifo, [enqueue] * 5)
#
# # 把　runner 加入 tf.GraphKeys.QUEUE_RUNNERS 集合
# tf.train.add_queue_runner(runner)
#
# # 获取队列元素，dequeue_many　必须指定 FIFOQueue 的 shape
# dequeue = fifo.dequeue_many(10, "myDequeue")
#
# with tf.Session() as sess:
#     cood = tf.train.Coordinator()
#
#     # 会自动从集合　tf.GraphKeys.QUEUE_RUNNERS　中获取 runner，且启动多个线程
#     threads = tf.train.start_queue_runners(sess, coord=cood)
#
#     # 进行出队列操作
#     # for i in range(10):
#     #     print(sess.run(dequeue))
#     if fifo.size().eval() == 100:
#         print(sess.run(dequeue))
#         cood.request_stop()
#
#     cood.join(threads)

# 输入文件队列
# TFRecord 帮助函数
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


# 模拟将数据写入不同的文件
num_shards = 2  # 文件个数
instance_per_shard = 2  # 每个文件数据的个数
for i in range(num_shards):
    filename = ('data.tfrecords-%.5d-of%.5d' % (i, num_shards))
    writer = tf.python_io.TFRecordWriter(filename)
    for j in range(instance_per_shard):
        example = tf.train.Example(features=tf.train.Features(feature={
            'i': _int64_feature(i),
            'j': _int64_feature(j)
        }))
        writer.write(example.SerializeToString())
    writer.close()

# 模糊匹配获取文件列表
files = tf.train.match_filenames_once("data.tfrecords-*")

# 创建输入队列, num_epochs: 一共遍历文件的次数, shuffle: 是否打乱顺序　
filename_queue = tf.train.string_input_producer(files, shuffle=False, num_epochs=2)

# 读取并解析一个样本
reader = tf.TFRecordReader()
_, serialized_example = reader.read(filename_queue)
features = tf.parse_single_example(  # 读取单个样本，一个文件可能多个样本
    serialized=serialized_example,
    features={
        'i': tf.FixedLenFeature([], tf.int64),
        'j': tf.FixedLenFeature([], tf.int64)
    }
)

# tf.train.shuffle_batch(num_threads=)

with tf.Session() as sess:
    # print(tf.get_collection(tf.GraphKeys.LOCAL_VARIABLES))
    # train.match_filenames_once() 作为局部变量
    # tf.global_variables_initializer 只初始化全局变量
    tf.initialize_local_variables().run()
    print(sess.run(files))

    # 声明 Coordinator，并启动多线程
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    # 多次执行获取数据操作
    for i in range(6):
        print(sess.run([features['i'], features['j']]))

    coord.request_stop()
    coord.join(threads)
