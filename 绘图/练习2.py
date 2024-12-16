import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
# np.random.seed(19680801)

# some random data
# x = np.random.randn(1000)
# y = np.random.randn(1000)
data = [
    (1, 1, 4328), (1, 12, 21),
    (2, 2, 21123), (2, 11, 31), (2, 10, 9), (2, 8, 31),
    (3, 3, 3453), (3, 9, 7), (3, 13, 2),
    (4, 4, 320), (4, 5, 4), (4, 13, 2),
    (5, 5, 1399), (5, 6, 7),
    (6, 6, 170), (6, 5, 4),
    (7, 7, 125), (7, 14, 4),
    (8, 2, 15), (8, 8, 3710), (8, 9, 1),
    (9, 2, 2), (9, 8, 1), (9, 9, 418),
    (10, 2, 55), (10, 10, 7693), (10, 11, 385),
    (11, 2, 101), (11, 10, 763), (11, 11, 46642), (11, 15, 2),
    (12, 1, 6), (12, 12, 70),
    (13, 13, 179),
    (14, 6, 6), (14, 7, 3), (14, 14, 107),
    (15, 2, 2), (15, 5, 4), (15, 15, 811),
    (16, 16, 2),
    (17, 17, 76),
    (18, 18, 0)
]

# x = [1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 12, 12, 13, 14, 14, 14, 15, 15, 15, 16, 17, 18]
# y = [1, 12, 2, 11, 10, 8, 3, 9, 13, 4, 5, 13, 5, 6, 6, 5, 7, 14, 2, 8, 9, 2, 8, 9, 2, 10, 11, 2, 10, 11, 15, 1, 12, 13, 6, 7, 14, 2, 5, 15, 16, 17, 18]
Count = [4328, 21, 21123, 31, 9, 31, 3453, 7, 2, 320, 4, 2, 1399, 7, 170, 4, 125, 4, 15, 3710, 1, 2, 1, 418, 55, 7693,
         385, 101, 763, 46642, 2, 6, 70, 179, 6, 3, 107, 2, 4, 811, 2, 76, 0]
x = [item[0] for item in data for _ in range(item[2])]
y = [item[1] for item in data for _ in range(item[2])]

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
p1.scatter(x, y, color='g', alpha=0.4, linewidths=2)
# 画散点图上方的图
bin_w = 0.4
# 因为上方和右方的图是同一批数据，上方的x和右方的范围一致
xy_margin = np.max([np.max(np.abs(x)), np.max(np.fabs(y))])
# 得出精确的宽度值
lim = int(xy_margin / bin_w + 1) * bin_w

# 设置直方图的轴范围
p2.set_xlim(0, lim)
p1.set_xlim(0, 18)
p1.set_ylim(0, 18)

p3.set_ylim(0, lim)
# p2.set_yticks([0, 20000, 40000])
# 设置 y 轴刻度标签
# p2.set_yticklabels(['0','20000', '40000'])
# p2.set_yscale('log')
# bins的范围
bins = np.arange(0, lim + bin_w, bin_w)
# 画出上方的图
p2.hist(x, bins=bins, alpha=0.9, width=0.8)

# 将右方的图形水平放置
p3.hist(x, bins=bins, alpha=0.9, height=0.8, orientation='horizontal')

plt.show()
