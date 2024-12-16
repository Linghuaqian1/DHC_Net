import numpy as np
import cv2
import torch

label_path = r"E:\datasets\labels\val\P0003__1024__0___0.txt"
image_path = r"E:\datasets\DOTAobb\val\images\P0007__1__0___0.png"

colors = (
    "FF3838", "FF9D97", "FF701F", "FFB21D", "CFD231", "48F90A", "92CC17", "3DDB86", "1A9334", "00D4BB",
    "2C99A8", "00C2FF", "344593", "6473FF", "0018EC", "8438FF", "520085", "CB38FF", "FF95C8", "FF37C7",
)
#坐标转换，原始存储的是YOLOv5格式
# Convert nx4 boxes from [x, y, w, h] normalized to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
def xywh2xyxy(x, w1, h1, img):
    labels = ['airplane', 'helicopter', 'small-vehicle',  'large-vehicle', 'ship',
              'container', 'storage-tank', 'swimming-pool', 'windmill', 'ignore']
    label, x1, y1, x2,y2,x3,y3,x4,y4 = x
    print("原图宽高:\nw1={}\nh1={}".format(w1, h1))
    #边界框反归一化
    # x_t = x*w1
    # y_t = y*h1
    # w_t = w*w1
    # h_t = h*h1
    #
    # print("反归一化后输出：\n第一个:{}\t第二个:{}\t第三个:{}\t第四个:{}\t\n\n".format(x_t,y_t,w_t,h_t))
    #计算坐标
    top_left_x = x1*w1
    top_left_y = y1*h1
    bottom_right_x = x3*w1
    bottom_right_y = y3*h1
    # print('标签:{}'.format(labels[int(label)]))
    # print("左上x坐标:{}".format(top_left_x))
    # print("左上y坐标:{}".format(top_left_y))
    # print("右下x坐标:{}".format(bottom_right_x))
    # print("右下y坐标:{}".format(bottom_right_y))

    # 绘图  rectangle()函数需要坐标为整数
    cv2.rectangle(img, (int(top_left_x), int(top_left_y)), (int(bottom_right_x), int(bottom_right_y)), (0, 255, 0), 2)
    cv2.imshow('show', img)
    cv2.imwrite('11.png',img)
    cv2.waitKey(0)  # 按键结束
    cv2.destroyAllWindows()
# 读取图像文件
img_ori = cv2.imread(str(image_path))
img=cv2.resize(img_ori,None,fx=0.3,fy=0.3,interpolation=cv2.INTER_LINEAR)
print(img)
h, w = img.shape[:2]


#读取 labels
with open(label_path, 'r') as f:
    lb = np.array([x.split() for x in f.read().strip().splitlines()], dtype=np.float32)  # labels
    print(lb)


for x in lb:
    # 反归一化并得到左上和右下坐标，画出矩形框
    xywh2xyxy(x, w, h, img)

#
# def draw_box_from_relative_coordinates(image_path, relative_coordinates):
#     # 读取图片
#     img = cv2.imread(image_path)
#
#     # 获取图片的宽度和高度
#     img_width = img.shape[1]
#     img_height = img.shape[0]
#
#     # 将相对坐标转换为绝对坐标
#     absolute_coordinates = [(int(point[0] * img_width), int(point[1] * img_height)) for point in relative_coordinates]
#
#     # 绘制多边形
#     cv2.polylines(img, [np.array(absolute_coordinates)], isClosed=True, color=(0, 0, 255), thickness=2)
#
#     # 显示图片
#     cv2.imshow('Image with Box', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#
# # 示例使用
# # image_path = 'path/to/your/image.jpg'
# # 以左上、右上、右下、左下的相对坐标为例
# relative_coordinates = [(0.197888, 0.0963567), (0.188111 ,0.0953979), (0.186547 ,0.0397891), (0.195933 ,0.0397891)]
#
# draw_box_from_relative_coordinates(image_path, relative_coordinates)


