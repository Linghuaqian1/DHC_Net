import numpy as np
import matplotlib.pyplot as plt

# 准备数据
strategies = ['Strategy 1', 'Strategy 2', 'Strategy 3', 'Strategy 4']
indicators = ['Indicator 1', 'Indicator 2', 'Indicator 3', 'Indicator 4']
# 假设这里有一个4x4的矩阵，每行表示一个策略，每列表示一个指标
data = np.random.rand(4, 4)

# 创建雷达图
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
theta = np.linspace(0, 2 * np.pi, len(indicators), endpoint=False)

# 绘制每个策略的雷达图
for i in range(len(strategies)):
    values = data[i].tolist()
    ax.plot(theta, values, label=strategies[i])
    ax.fill(theta, values, alpha=0.25)

ax.set_xticks(theta)  # 设置角度刻度
ax.set_xticklabels(indicators)  # 设置指标标签
plt.title('Radar Chart of Different Strategies')  # 设置标题
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))  # 设置图例位置
plt.show()
