import matplotlib.pyplot as plt
import numpy as np

# 定义数据
categories = ["Baseline+MDFA", "BL+MDFA+DFL", "BL+MDFA+IFSE", "Ours"]
indicators = ["cows", "black_rhinoceros", "kudus", "Recall","mAP50"]
# colors = [ 'g' , 'm', 'cyan',  'purple', 'r', 'brown', 'pink'   , 'teal',
#           'indigo', 'gray', 'gold']
# colors = []
colors = ['#F7CA9B', '#D8F7D1', '#8AA7E5', '#E5637B', '#F73E0D', '#9394e7', '#ef7a6d', '#54b345', '#c76da2', '#ffbe7a', '#fa7f6f', '#e7dad2', '#999999', '#9ac9db', '#ff8884', '#14517c', '#2f7fc1', '#e7effa', '#96c37d', '#f3d266', '#f7e1ed', '#f8f3f9', '#c497b2']

# colors = ['b', 'g','navy',  'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink', 'olive', 'lime', 'cyan', 'teal',
#           'indigo', 'gray', 'gold', 'r']
data = {
    "Baseline+MDFA": [40.6, 12, 61.6, 39.8,38.1],
    "BL+MDFA+DFL": [42.9,16.8,64.5,36.1,41.3],
    "BL+MDFA+IFSE": [42.1,26.1,65.2,43.2,44.4],

    "Ours": [44.7,26.5,68.4,44.5,46.5],

}

# 绘图
fig, ax = plt.subplots(figsize=(10, 6))
width = 0.17  # 柱子宽度

for i, category in enumerate(categories):
    x = np.arange(len(indicators)) + i * width
    y = data[category]
    ax.bar(x, y, width, label=category, edgecolor='#F5F5F5',alpha=0.9, color=colors[i])

# 添加细线的边框
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(0.5)

ax.set_xticks(np.arange(len(indicators)) + width * (len(categories) - 1) / 2)
ax.set_xticklabels(indicators,fontsize=14)
ax.legend(fontsize=10)
plt.xlabel('Evaluation Metrics',fontsize=14)
plt.ylabel('Scores (%)',fontsize=14)
plt.ylim(0, 70)
plt.savefig(r'D:\syd迪马\孙煜东18个对比图\多柱状图.png')

plt.show()
