#!/user/bin/env python3
# -*- coding: utf-8 -*-
# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

# Set data
# 设定数据
df = pd.DataFrame({
    "metric": ["Precision","Recall","mAP50","mAP95"],
    "(23,1)": [68.53,50.47,52.94,32.68],
    "(3,1)+(5,1)\n+(7,1)+(9,1)": [70.90,51.54,54.45,34.27],
    "(5,1)+(7,3)": [73.97,54.72,57.34,41.12],
    # 'var5': [28, 15, 32, 14]
})







# number of variable
# 变量类别
categories = list(df)[1:]
# 变量类别个数
N = len(categories)

# plot the first line of the data frame.
# 绘制数据的第一行
values = df.loc[0].drop("metric").values.flatten().tolist()
# 将第一个值放到最后，以封闭图形
values += values[:1]
print(values)

# 设置每个点的角度值
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
# 初始化极坐标网格
ax = plt.subplot(111, polar=True)

# Draw one axe per variable + add labels labels yet
# 设置x轴的标签
plt.xticks(angles[:-1], categories, color='grey', size=8)

# Draw ylabels
# 设置标签显示位置
# 具体见https://www.bbsmax.com/A/x9J2DRwNd6/
ax.set_rlabel_position(0)
# 设置y轴的标签
plt.yticks([20, 40, 60], ["20", "40", "60"], color="grey", size=7)
plt.ylim(0, 80)

# Plot data
# 画图
ax.plot(angles, values, linewidth=1, linestyle='solid')

# Fill area
# 填充区域
ax.fill(angles, values, 'b', alpha=0.1);

plt.show();
