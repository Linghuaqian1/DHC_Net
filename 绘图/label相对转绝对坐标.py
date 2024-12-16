#!/user/bin/env python3
# -*- coding: utf-8 -*-

import os

# 设置文件夹路径和常量
folder_path = r"E:\yyj_file\datasets\SODA-A-1024\labels\val绝对"
constant = 1024

# 处理单个文件
def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            parts = line.strip().split()
            label = parts[0]
            coordinates = [float(coord) * constant for coord in parts[1:]]
            new_line = f"{label} {' '.join(f'{coord:.2f}' for coord in coordinates)}\n"
            file.write(new_line)

# 遍历文件夹中的所有txt文件并处理
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        process_file(file_path)

print("所有文件已处理完毕。")
