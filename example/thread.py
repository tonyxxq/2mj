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
fifo = tf.FIFOQueue(100, dtypes=tf.float32, shapes=[2, 1])

# 队列中加入随机数，随机数需要使用　tf.random，如果使用　random 类的随机数每次入队的值都相同
enqueue = fifo.enqueue(tf.random.truncated_normal([2, 1]))

# 第一个参数表示队列，第二个参数表示操作（下面启动了 5 个线程进行 enqueue 操作）
runner = tf.train.QueueRunner(fifo, [enqueue] * 5)

# 把　runner 加入 tf.GraphKeys.QUEUE_RUNNERS 集合
tf.train.add_queue_runner(runner)

# 获取队列元素，dequeue_many　必须指定 FIFOQueue 的 shape
dequeue = fifo.dequeue_many(10, "myDequeue")

with tf.Session() as sess:
    cood = tf.train.Coordinator()

    # 会自动从集合　tf.GraphKeys.QUEUE_RUNNERS　中获取 runner，且启动多个线程
    threads = tf.train.start_queue_runners(sess, coord=cood)

    # 进行出队列操作
    # for i in range(10):
    #     print(sess.run(dequeue))
    if fifo.size().eval() == 100:
        print(sess.run(dequeue))
        cood.request_stop()

    cood.join(threads)
