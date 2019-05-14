import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os

# 输入：1张图片，尺寸 28*28 高宽，通道数 3
x = np.ones((1, 28, 28, 3), dtype=np.float32)

# 卷积核尺寸 4x4 ，5表输出通道数，3代表输入通道数
w = np.ones((4, 4, 5, 3), dtype=np.float32)

# 扩大2倍
output = tf.nn.conv2d_transpose(x, w, (1, 84, 84, 5), [1, 3, 3, 1], padding='SAME')

with tf.Session() as sess:
    m = sess.run(output)
    print(m.shape)
