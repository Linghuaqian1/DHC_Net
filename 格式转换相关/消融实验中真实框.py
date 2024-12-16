# encoding=utf-8
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from PIL import Image
#

import numpy as np
import cv2

label_path = r"E:\datasets\labels\val\P0007__1024__0___0.txt"
image_path = r"E:\datasets\DOTAobb\val\images\P0007__1__0___0.png"
#     image_path = r"C:\Users\yyj\OneDrive\桌面\论文相关\小目标初稿\论文中实验图片\消融实验图片\P0206__1__0___303.png"
#     label_file = r"E:\datasets\labels\val\P0206__1024__0___303.txt"
# 颜色列表
colors = (
    "FF3838", "FF9D97", "FF701F", "FFB21D", "CFD231", "48F90A", "92CC17", "3DDB86", "1A9334", "00D4BB",
    "2C99A8", "00C2FF", "344593", "6473FF", "0018EC", "8438FF", "520085", "CB38FF", "FF95C8", "FF37C7",
)

# 标签列表
labels = ['PL',
               'SH',
               'ST',
               'BD',
               'TC',
               'BC',
               'GTF',
               'HB',
               'BR',
               'LV',
               'SV',
               'HC',
               'RA',
               'SBF',
               'SP',
               'CC',
               'AP',
               'HP'
               ]

# 将颜色转换为RGB格式
colors = [tuple(int(c[i:i+2], 16) for i in (0, 2, 4))[::-1] for c in colors]

# 读取图像文件
img_ori = cv2.imread(str(image_path))
img = cv2.resize(img_ori, None, fx=0.9, fy=0.9, interpolation=cv2.INTER_LINEAR)
h, w = img.shape[:2]

# 读取 labels
with open(label_path, 'r') as f:
    lb = np.array([x.split() for x in f.read().strip().splitlines()], dtype=np.float32)

# 反归一化并得到四个角的坐标，画出矩形框
def draw_boxes(x, w1, h1, img):
    label, x1, y1, x2, y2, x3, y3, x4, y4 = x
    color = colors[int(label)]

    # 反归一化坐标
    points = np.array([
        [x1 * w1, y1 * h1],
        [x2 * w1, y2 * h1],
        [x3 * w1, y3 * h1],
        [x4 * w1, y4 * h1]
    ], np.int32).reshape((-1, 1, 2))

    # 画多边形
    cv2.polylines(img, [points], isClosed=True, color=color, thickness=2)

    # 显示标签
    text = labels[int(label)]
    font_scale = 0.8  # 字体大小
    font_thickness = 2  # 字体粗细
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.putText(img, text, (int(x1 * w1), int(y1 * h1) - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness, lineType=cv2.LINE_AA)

for x in lb:
    draw_boxes(x, w, h, img)

# 显示结果
cv2.imshow('Result', img)
cv2.imwrite('result.png', img)
cv2.waitKey(0)  # 按键结束
cv2.destroyAllWindows()





