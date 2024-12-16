# #!/user/bin/env python3
# # -*- coding: utf-8 -*-
#
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np
#
# # 假设这是你的三元组数据
# triplets = [
#     (0, 0, 0.9), (0, 1, 0.1), (1, 0, 0.2), (1, 1, 0.8),
#     (2, 2, 0.7), (2, 3, 0.3), (3, 2, 0.6), (3, 3, 0.4)
#     # 这里添加更多的三元组
# ]
#
# # 根据三元组创建一个空矩阵
# num_classes = 19  # 根据你的数据集设置类别数量
# matrix = np.zeros((num_classes, num_classes))
#
# # 将三元组中的值填入矩阵
# for x, y, value in triplets:
#     matrix[x, y] = value
#
# # 类别标签，根据你的数据集进行调整
# labels = ["plane", "ship", "storage-tank", "baseball-diamond", "tennis-court", "basketball-court",
#           "ground-track-field", "harbor", "bridge", "large-vehicle", "small-vehicle", "helicopter",
#           "roundabout", "soccer-ball-field", "swimming-pool", "container-crane", "airport", "helipad", "background"]
#
# # 确保标签长度与类别数量一致
# labels = labels[:num_classes]
#
# plt.figure(figsize=(12, 10))
# sns.heatmap(matrix, annot=True, fmt='.2f', cmap='Blues', xticklabels=labels, yticklabels=labels)
# plt.title('Confusion Matrix Normalized')
# plt.xlabel('True')
# plt.ylabel('Predicted')
# plt.show()
#
# !/user/bin/env python3
# -*- coding: utf-8 -*-

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 假设这是你的三元组数据
triplets = [
    (0, 0, 0.69), (0, 3, 0.04),(1,0,0.01),(1,1,0.45),(1,2,0.03),(1,3,0.16),(2,1,0.3),(2,2,0.86),
    (2,3,0.8),(3,0,0.3),(3,1,0.24),(3,2,0.11)
    # 这里添加更多的三元组
]

# 根据三元组创建一个空矩阵
num_classes = 4  # 根据你的数据集设置类别数量
matrix = np.zeros((num_classes, num_classes))

# 将三元组中的值填入矩阵
for x, y, value in triplets:
    matrix[x, y] = value
matrix[matrix == 0] = np.nan
# 类别标签，根据你的数据集进行调整
labels = ["Cows", "Rhinoceros", "Kudus","BG"]

# 确保标签长度与类别数量一致
labels = labels[:num_classes]

plt.figure(figsize=(12, 10))
sns.heatmap(matrix, annot=True, fmt='.2f', cmap='Blues', xticklabels=labels, yticklabels=labels,
            annot_kws={"size": 9})
plt.xticks(rotation=30, fontsize=13)
plt.yticks(rotation=0, fontsize=13)
plt.title('Confusion Matrix Normalized', fontsize=16)
plt.xlabel('True', fontsize=15)
plt.ylabel('Predicted', fontsize=15)
plt.savefig("D:\syd迪马\dongwuma.jpg")
plt.show()

