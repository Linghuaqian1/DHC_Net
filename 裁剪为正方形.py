#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
from PIL import Image


def crop_to_square(image_path):
    # 打开图片
    img = Image.open(image_path)

    # 获取图片的宽度和高度
    width, height = img.size

    # 确定短边长度
    min_side = min(width, height)

    # 计算裁剪区域的边界
    left = (width - min_side) / 2
    top = (height - min_side) / 2
    right = (width + min_side) / 2
    bottom = (height + min_side) / 2

    # 裁剪图片
    cropped_img = img.crop((left, top, right, bottom))

    # 返回裁剪后的图片对象
    return cropped_img


# 原始图片文件夹路径
folder_path = r"E:\yyj_file\datasets\DOTAv2\images\test"

# 裁剪后保存的文件夹路径
output_folder_path = r"E:\yyj_file\datasets\DOTAv2\images\test_square"

# 遍历文件夹中的所有图片文件
for filename in os.listdir(folder_path):
    # 检查文件是否为图片文件
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # 构建图片的完整路径
        image_path = os.path.join(folder_path, filename)

        # 进行裁剪
        cropped_image = crop_to_square(image_path)

        # 保存裁剪后的图片
        output_path = os.path.join(output_folder_path, filename)
        cropped_image.save(output_path)

print("裁剪完成！")