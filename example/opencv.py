import cv2
import numpy as np
import random


def show_img(name, img):
    """
    显示图像
    """
    cv2.imshow(name, img)
    cv2.waitKey(0)


# 载入、显示、翻转、保存图像
img = cv2.imread("1.jpg")
img = cv2.resize(img, (200, 200))
#
# # 创建新图像
# new_img = np.zeros(img.shape, np.uint8)
# #或直接复制
# #new_img = img.copy()
#
# # 正数水平翻转、0 垂直翻转、负数既水平又垂直
# cv2.flip(img, 0, new_img)
# show_img("img", new_img)
#
# # 保存
# cv2.imwrite("flip.jpg", new_img)

# 设置椒盐噪点
# rows = img.shape[0]
# cols = img.shape[1]
# channels = img.shape[2]
# for i in range(1000):
#     row = random.randint(0, 2000) % rows
#     col = random.randint(0, 2000) % cols
#     if len(img.shape) > 2:
#         img[row][col] = [0, 0, 0]
#     else:
#         img[row][col] = 0
# show_img("img", img)

# 给图像加文字
# cv2.putText(img, "good house", (50, 50), cv2.FONT_ITALIC, 0.8, (0, 0, 0), 2)

# 添加框
# cv2.rectangle(img, (50, 50), (100, 100), (0, 0, 255), 1)


# 二值化
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#
# # 中值滤波
# gray = cv2.medianBlur(gray, 3)
#
# # 扩充图像
# gray = cv2.copyMakeBorder(gray, 100, 100, 100, 100, cv2.BORDER_ISOLATED, value=0)
#
# # 旋转图像
# rotateMatrix = cv2.getRotationMatrix2D(center=(img.shape[1] / 2, img.shape[0] / 2), angle=-90, scale=0.5)
# rotImg = cv2.warpAffine(img, rotateMatrix, (img.shape[1], img.shape[0]))
# cv2.imwrite("mark.jpg", rotImg)
#
# #  查找轮廓
# contours_map, contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
# # 去掉轮廓面积小的轮廓
# contours = [contour for contour in contours if cv2.contourArea(contour) > 500]
#
# # 判断像素点是否在某一轮廓内
# # True：输出该像素点到轮廓最近距离，False，输出为正表示在轮廓内，0为轮廓上，负为轮廓外。
# result = cv2.pointPolygonTest(contours[0], (20, 30), False)
#
# # 在每个轮廓的中间添加轮廓的编号
# for idx, c in enumerate(contours):
#     # 获取中心点,质心
#     M = cv2.moments(c)
#     if M["m00"] > 0 and M["m00"] > 0:
#         cX = int(M["m10"] / M["m00"])
#         cY = int(M["m01"] / M["m00"])
#
#         # 在轮廓中兴中心写上标签值
#         # cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
#         cv2.putText(img, str(idx), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
#
# # 在图像上添加边框
# # 第一个参数表示需要添加轮廓的图像，可以是彩色图片
# # 第二个参数表示轮廓列表
# # 第三个表示需要天机的轮廓的 id，-1 表示添加所有
# # 第四个参数表示线条的粗细
# cv2.drawContours(img, contours, -1, (0, 255, 255), 2)
#
# # 包含轮廓的最小外接矩形
# # 返回的是最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
# # 注意：这一步返回的是 float 数据类型
# rect = cv2.minAreaRect(contours[0])
#
# # 获取最小外接矩形的 4 个顶点，且转换为 int 类型
# # np.int0 可以近似理解为 np.int64
# box = np.int0(cv2.boxPoints(rect))
# cv2.drawContours(img, [box], 0, (0, 255, 255), 2)

# 图像进行叠加
# 注意：图像叠加必须有相同的大小
img2 = cv2.imread("2.jpg")
img2 = cv2.resize(img2, (50, 50))

# 找到底图的 ROI，把 img2 叠加到 img 的正中间
img_shape = img.shape
img2_shape = img2.shape
roi_img = img[img_shape[0] // 2 - img2_shape[0] // 2:img_shape[0] // 2 + img2_shape[0] // 2,
          img_shape[1] // 2 - img2_shape[1] // 2:img_shape[1] // 2 + img2_shape[1] // 2]
cv2.addWeighted(roi_img, .5, img2, .8, 0., roi_img)

show_img("new_img", img)
cv2.imwrite("new_img.jpg", img)
