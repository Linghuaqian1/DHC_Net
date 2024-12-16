import matplotlib.pyplot as plt

# 数据
from matplotlib.ticker import MultipleLocator

models = ["(23,1)", "(3,1)+(5,1)\n+(7,1)+(9,1)", "(5,1)+(7,3)"]
# precision = [68.53, 70.90, 73.88]
# Recall = [50.47, 51.54, 52.06]
# mAP50 = [52.94, 54.45, 56.74]
# mAP95 = [32.68, 34.27, 39.68]
precision = [68.53, 70.90, 73.97]
# precision = [50.47, 51.54, 52.06]
# precision = [52.94, 54.45, 56.74]
# precision = [32.68, 34.27, 39.68]
colors = ['b', 'g', 'navy', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink', 'olive', 'lime', 'cyan', 'teal',
          'indigo', 'gray', 'gold', 'r']
# 创建折线图
plt.figure(figsize=(5, 4))
plt.plot(models, precision, marker='o', linestyle='-', alpha=0.7, color=colors[8])  # 前几个点和所有线使用蓝色
# plt.plot(models[-1], precision[-1], marker='o', linestyle='-', color='red')  # 最后一个点使用红色

# 添加最后一个点到折线图中
# plt.plot(models[-1], precision[-1], marker='o', linestyle='-', color='blue')  # 最后一个点使用蓝色
plt.plot(models[0], precision[0], marker='o', linestyle='-', color=colors[8])
plt.plot(models[1], precision[1], marker='o', linestyle='-', color=colors[8])
plt.plot(models[2], precision[2], marker='o', linestyle='-', color=colors[8])
# 添加标签，并调整字体
# plt.xlabel('Models', fontsize=14)
plt.ylabel('Precision (%)', fontsize=12)
# plt.title('Precision by Different Models', fontsize=16)
plt.ylim(65, 75)
plt.gca().yaxis.set_major_locator(MultipleLocator(5))

# 斜着显示x轴标签
plt.xticks(rotation=45, ha='right', fontsize=10)

plt.tight_layout()
plt.show()
