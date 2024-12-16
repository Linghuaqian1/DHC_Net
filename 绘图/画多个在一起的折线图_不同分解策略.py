import matplotlib.pyplot as plt
import numpy as np

# 定义数据
from matplotlib.ticker import MultipleLocator

settings = ["(23,1)", "(3,1)+(5,1)+(7,1)+(9,1)", "(5,1)+(7,3)"]
metrics = ["Precision", "Recall", "mAP50", "mAP95"]
data = {
    "Precision": [68.53, 70.90, 73.97],
    "Recall": [50.47, 51.54, 54.72],
    "mAP50": [52.94, 54.45, 57.34],
    "mAP95": [32.68, 34.27, 41.12]
}

# 设置每个类别的线条样式和标记
linestyles = ['-', '--', '-.', 'dotted']
markers = ['o', '^', 's', 'D']
colors = ['r','orange','g','b']
# 绘图
fig, ax = plt.subplots()

for i, metric in enumerate(metrics):
    x = np.arange(len(settings)) + 1
    y = [data[metric][i] for i in range(len(settings))]
    ax.plot(x, y, label=metric, color=colors[i],linestyle='-', marker=markers[i],markersize=8)

# 设置x轴刻度和标签
ax.set_xticks(np.arange(len(settings)) + 1)
ax.set_xticklabels(settings)
# 将图例设置为两行两列
ax.legend(loc='upper left', bbox_to_anchor=(0, 1), ncol=2)
# plt.xlabel('(k,d) Sequence')
plt.ylabel('Scores (%)')
# plt.title('Scores by (k,d) Sequence and Metrics')
plt.gca().yaxis.set_major_locator(MultipleLocator(20))
plt.ylim(20, 85)
plt.grid(True)
plt.show()
