import os
import shutil

image_dir = r"E:\soda_test\images"
label_dir = r"E:\soda_test\new"
new_image_dir = r'E:\soda_test\test'
if not (os.path.exists(new_image_dir)):
    os.mkdir(new_image_dir)
for label_name in os.listdir(label_dir):
    # a = []
    # # 获取标签的完整路径
    # label_path = os.path.join(label_dir, label_name)
    # 获取标签的扩展名
    ext = os.path.splitext(label_name)[-1]
    # 根据扩展名替换成对应的image文件名
    image_name = label_name.replace(ext, ".jpg")
    image_path = os.path.join(image_dir, image_name)
    new_image_name=os.path.join(new_image_dir,image_name)
    shutil.copy(image_path,new_image_name)













