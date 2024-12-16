#!/user/bin/env python3
# -*- coding: utf-8 -*-
import random

import matplotlib.pyplot as plt
import numpy as np

# class_label = {'plane': 0,
#                'ship': 1,
#                'storage-tank': 2,
#                'baseball-diamond': 3,
#                'tennis-court': 4,
#                'basketball-court': 5,
#                'ground-track-field': 6,
#                'harbor': 7,
#                'bridge': 8,
#                'large-vehicle': 9,
#                'small-vehicle': 10,
#                'helicopter': 11,
#                'roundabout': 12,
#                'soccer-ball-field': 13,
#                'swimming-pool': 14,
#                'container-crane': 15,
#                'airport': 16,
#                'helipad': 17
#                }
class_label = ['plane',
               'ship',
               'storage-tank',
               'baseball-diamond',
               'tennis-court',
               'basketball-court',
               'ground-track-field',
               'harbor',
               'bridge',
               'large-vehicle',
               'small-vehicle',
               'helicopter',
               'roundabout',
               'soccer-ball-field',
               'swimming-pool',
               'container-crane',
               'airport',
               'helipad'
               ]
with open(r"C:\Users\yyj\OneDrive\桌面\param.txt", 'r') as f:
    lines = f.readlines()

    # 初始化空列表来保存坐标
x_coords = []
y_coords = []

# 遍历每一行，读取内容
for line in lines:
    parts = line.strip().split()
    pre_label = int(float(parts[0]))
    if len(parts) == 3:
        true_label = int(float(parts[1]))
        value = parts[2]
    elif len(parts) == 3:
        true_label = pre_label
        value = parts[1]
    else:
        continue

    # 原点坐标
    origin = [int(true_label),int(pre_label)]

    # 计算极坐标
    r = float(value)
    sign = random.choice([1, -1])
    # 将原始数与随机的正负号相乘
    r = r * sign

    # 将极坐标转换为直角坐标
    x = origin[0]
    y = origin[1] + r
    # 将坐标添加到列表中
    x_coords.append(x)
    y_coords.append(y)


# 生产所需的数据

border = 0.1
width = 0.5
height = 0.2
between = 0.02

# 散点图的四边
left_o = border
bottom_o = border
height_o = width
width_o = width

# 散点图上方的图
left_t = border
bottom_t = border + width_o + between
height_t = height
width_t = width

# 散点图右方的图
left_f = border + width_o + between
bottom_f = border
height_f = width
width_f = height

# 使用ply.axes需要传入的位置
ret1 = [left_o, bottom_o, width_o, height_o]
ret2 = [left_t, bottom_t, width_t, height_t]
ret3 = [left_f, bottom_f, width_f, height_f]

plt.style.use('seaborn-paper')
plt.figure()
p1 = plt.axes(ret1)
p2 = plt.axes(ret2)
p3 = plt.axes(ret3)

# 去掉重叠区域的标签
p2.set_xticks([])
p3.set_yticks([])
p1.set_xlabel('True')
p1.set_ylabel('Predicted')

p1.plot([0, 18], [0, 18], color='r', alpha=0.6, linestyle='-')
# 画散点图
p1.scatter(x_coords, y_coords, edgecolors='none',color='#008000', alpha=0.01, s=3)
# 画散点图上方的图
# plt.gca().yaxis.set_major_locator(MultipleLocator(5))这个是干嘛的
p1.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
p1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
bin_w = 0.4
# 因为上方和右方的图是同一批数据，上方的x和右方的范围一致
xy_margin = np.max([np.max(np.abs(x_coords)), np.max(np.fabs(y_coords))])
# 得出精确的宽度值
lim = int(xy_margin / bin_w + 1) * bin_w

# 设置直方图的轴范围
p2.set_xlim(0, lim)
p1.set_xlim(-0.5, 18.5) # 修改 x 轴范围
p1.set_ylim(-0.5, 18.5) # 修改 y 轴范围

p3.set_ylim(0, lim)
# p2.set_yticks([0, 20000, 40000])
# 设置 y 轴刻度标签
# p2.set_yticklabels(['0','20000', '40000'])
# p2.set_yscale('log')
# bins的范围
bins = np.arange(0, lim + bin_w, bin_w)
# 画出上方的图
p2.hist(x_coords, bins=bins, alpha=0.9, width=0.4)

# 将右方的图形水平放置
p3.hist(x_coords, bins=bins, alpha=0.9, height=0.4, orientation='horizontal')

plt.savefig("scatter_plot.svg")
plt.show()






