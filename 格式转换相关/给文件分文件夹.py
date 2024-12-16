import os
import shutil

# 指定 images 文件夹路径
image_dir = r"E:\datasets\small_target\AI-TOD\train\images"

# 指定labels文件夹路径
label_dir = r"E:\datasets\small_target\AI-TOD\train\labels"

current_path = r"E:\datasets\small_target\AI-TOD\class"
print('当前目录：' + current_path)
class_label = {0: 'airplane',
               1: 'bridge',
               2: 'storage-tank',
               3: 'ship',
               4: 'swimming-pool',
               5: 'vehicle',
               6: 'person',
               7: 'wind-mill'
               }

images_list = os.listdir(image_dir)

for image_name in images_list:
    image_path = os.path.join(image_dir, image_name)
    # 获取图片的扩展名
    ext = os.path.splitext(image_name)[-1]
    # 根据扩展名替换成对应的label文件名
    label_name = image_name.replace(ext, ".txt")
    label_path = os.path.join(label_dir, label_name)

    with open(label_path, 'r') as f:
        s = f.readline()
        dir_name=class_label[int(s[0])]

    try:
        os.mkdir(os.path.join(current_path,dir_name))
        print('创建文件夹'+dir_name)
    except:
        pass
    img_ab_name = os.path.join(current_path,dir_name,image_name)
    shutil.copy(image_path,img_ab_name)






#


#     try:
#         name1, name2 = filename.split('.')
#         if name2 == 'jpg' or name2 == 'png':
#
#             try:
#                 shutil.move(current_path+'\\'+filename,current_path+'\\'+name1[:-1])
#                 print(filename+'转移成功！')
#             except Exception as e:
#                 print('移动失败:' + e)
#     except:
#         pass
#
# print('整理完毕！')
