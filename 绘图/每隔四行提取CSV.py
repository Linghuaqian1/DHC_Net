#!/user/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

# 读取原始CSV文件
df = pd.read_csv(r"C:\Users\yyj\OneDrive\桌面\结果\obb\obbLKA_ACA_200e更好的\results.csv")

# 提取每隔4行的数据
new_df = df.iloc[::4]

# 保存提取后的数据到新的CSV文件
new_df.to_csv(r"C:\Users\yyj\OneDrive\桌面\结果\obb\obbLKA_ACA_200e更好的\results_new.csv", index=False)
