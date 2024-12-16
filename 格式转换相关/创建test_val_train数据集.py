import os
import random
from tqdm import tqdm

# 指定 images 文件夹路径
image_dir=r"E:\datasets\DOTA_data\split_ss_dota\trainval\images"
# 指定labels文件夹路径
label_dir=r"E:\datasets\DOTA_data\split_ss_dota\trainval\label_y"
#创建一个空列表来存储有效图片的路径
valid_images=[]
# 创建一个空列表来存储有效label的路径
valid_labels=[]

# 遍历images文件夹下的所有图片
for image_name in os.listdir(image_dir):
    # 获取图片的完整路径
    image_path=os.path.join(image_dir,image_name)
    # 获取图片的扩展名
    ext=os.path.splitext(image_name)[-1]
    # 根据扩展名替换成对应的label文件名
    label_name = image_name.replace(ext,".txt")
    # 获取对应label的完整路径
    label_path=os.path.join(label_dir,label_name)
    # 判断label是否存在
    if not os.path.exists(label_path):
        # 删除图片
        os.remove(image_path)
        print("deleted:",image_path)
    else:
        # 将图片路径添加到列表中
        valid_images.append(image_path)
        # 将label路径添加到列表中
        valid_labels.append(label_path)

# 遍历每个有效图片路径
for i in tqdm(range(len(valid_images))):
    image_path = valid_images[i]
    label_path = valid_labels[i]
    # 随机生成一个概率
    r=random.random()
    # 判断图片应该移动到哪个文件夹
    # 7：2：1

    if r < 0.3:
        # 移动到valid文件夹
        destination = r"E:\datasets\DOTA_data\split_ss_dota\trainval\valid"
    else:
        # 移动到train文件夹
        destination = r"E:\datasets\DOTA_data\split_ss_dota\trainval\train"

    # 生成目标文件夹中图片的新路径
    image_destination_path = os.path.join(destination,"images",os.path.basename(image_path))
    # 移动图片到目标文件夹
    os.rename(image_path,image_destination_path)
    # 生成目标文件夹中label的新路径
    label_destination_path = os.path.join(destination,"labels",os.path.basename(label_path))
    # 移动label到目标文件夹
    os.rename(label_path,label_destination_path)

# 输出有效的image和label路径列表
print("valid_images:",valid_images)

print("valid_labels:",valid_labels)









