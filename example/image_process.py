# -*- coding: utf-8 -*-
import tensorflow as tf
import matplotlib.pyplot as plt


def show_img(image):
    plt.imshow(image)
    plt.show()


def write_image(img, file_name):
    img = tf.image.convert_image_dtype(img, dtype=tf.uint8)
    img = tf.image.encode_jpeg(img, 'rgb')
    with tf.gfile.GFile(file_name, 'wb') as f:
        f.write(img.eval())


# 读取图像数据
image_raw_data = tf.gfile.FastGFile("1.jpg", 'rb').read()

# 解码图片,获得三维矩阵
img_data = tf.image.decode_jpeg(image_raw_data, channels=3)

# 调整图像大小，采用双线性插值等技术，需要改变原来生成三维矩阵后里面元素的格式，即吧整形转换成 float32 类型
# converted_image = tf.image.convert_image_dtype(img_data, dtype=tf.float32)
# resized_img = tf.image.resize(converted_image, [100, 120])

# 图像翻转
# flip_image = tf.image.flip_left_right(img_data)
# flip_image = tf.image.random_flip_left_right(img_data) # 随机翻转
# flip_image = tf.image.random_flip_up_down(img_data) # 随机翻转
# flip_image = tf.image.flip_up_down(img_data)
# flip_image = tf.image.transpose_image(img_data)  # 沿对角线翻转

# 裁剪或填充
# img = tf.image.central_crop(img_data, 0.5) # 中心裁剪
# img = tf.image.resize_image_with_crop_or_pad(img_data, 300, 200)
# img = tf.image.resize_image_with_crop_or_pad(img_data, 3000, 2000)

# 图像色彩调整
# img = tf.image.adjust_brightness(img_data, -0.2)
# img = tf.image.random_brightness(img_data, 0.5)  # 在 -0.5 和　0.5 之间随机调整亮度
# img = tf.image.adjust_contrast(img_data, 10)
# img = tf.image.random_contrast(img_data, 0, 10) # 在 0 和 10 之间随机调整对比度
# img = tf.image.adjust_hue(img_data, 0.2)
# img = tf.image.random_hue(img_data, 0.5) # 在 -0.5 和 0.5 之间随机调整色相
# img = tf.image.adjust_saturation(img_data, 5)
# img = tf.image.random_saturation(img_data, 0, 5) # 在 -5 和 5 之间随机调整饱和度

# 图像的标准化
# img = tf.image.per_image_standardization(img_data)

# 处理标注框
# img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)  # 转换为实数
# # 把图像的像素调低一点，不然看不见标注框
# img_data = tf.image.resize(img_data, [700, 700])
# # 添加一个维度，因为标注狂输入数据为 4 维，输入的是一个批次的图像
# img_data = tf.expand_dims(img_data, 0)
# # 三维，多副图像，且每副图像可有多个标注框，分别代表左上角y, x　右下角 y, x
# boxes = tf.constant([[[0.1, 0.2, 0.4, 0.8], [0., 0.3, 0.4, 0.5]]])
# img = tf.image.draw_bounding_boxes(img_data, boxes)[0]

# 随机截取图像
# # 生成 bounding box，随机生成截取的 bounding box
# img_data = tf.image.resize(tf.image.convert_image_dtype(img_data, tf.float32), [500, 500])
# boxes = tf.constant([[[0.1, 0.2, 0.9, 0.8]]])
# begin, size, bbox_for_draw = tf.image.sample_distorted_bounding_box(tf.shape(img_data), bounding_boxes=boxes)
# # 可视化截取图像的位置
# batched_images = tf.expand_dims(img_data, 0)
# image_with_box = tf.image.draw_bounding_boxes(batched_images, bbox_for_draw)[0]
# # 截取图像
# img = tf.slice(img_data, begin, size)

with tf.Session() as sess:
    image_with_box_, begin_, size_, bbox_for_draw_, img_ = sess.run([image_with_box, begin, size, bbox_for_draw, img])
    show_img(image_with_box_)

    show_img(img_)
    write_image(img_, 'new_image.jpg')
