from PIL import Image
import os

image_dir = r"E:\soda_test\dota_test\images"
label_dir = r"E:\soda_test\dota_test\label"
new_label_dir = r'E:\soda_test\dota_test\new'
if not (os.path.exists(new_label_dir)):
    os.mkdir(new_label_dir)
class_label = {'plane': 0,
               'ship': 1,
               'storage-tank': 2,
               'baseball-diamond': 3,
               'tennis-court': 4,
               'basketball-court': 5,
               'ground-track-field': 6,
               'harbor': 7,
               'bridge': 8,
               'large-vehicle': 9,
               'small-vehicle': 10,
               'helicopter': 11,
               'roundabout': 12,
               'soccer-ball-field': 13,
               'swimming-pool': 14,
               'container-crane': 15,
               'airport': 16,
               'helipad': 17
               }
a = [0, 0, 0, 0, 0, 0, 0, 0, 0]
for image_name in os.listdir(image_dir):
    my_list = []
    # 获取图片的完整路径
    image_path = os.path.join(image_dir, image_name)
    # 获取图片的扩展名
    ext = os.path.splitext(image_name)[-1]
    # 根据扩展名替换成对应的label文件名
    label_name = image_name.replace(ext, ".txt")
    label_path = os.path.join(label_dir, label_name)
    new_label_path = os.path.join(new_label_dir, label_name)
    img = Image.open(image_path)
    width, height = img.size

    with open(label_path, 'r') as f:
        for line in f:
            s_split = line.split()
            label = class_label[s_split[8]]
            x1 = format(float(s_split[0]) / width, '.6f')
            y1 = format(float(s_split[1]) / height, '.6f')
            x2 = format(float(s_split[2]) / width, '.6f')
            y2 = format(float(s_split[3]) / height, '.6f')
            x3 = format(float(s_split[4]) / width, '.6f')
            y3 = format(float(s_split[5]) / height, '.6f')
            x4 = format(float(s_split[6]) / width, '.6f')
            y4 = format(float(s_split[7]) / height, '.6f')

            my_list.append(
                str(label) + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(x3) + ' ' + str(
                    y3) + ' ' + str(x4) + ' ' + str(y4) + '\n')

    with open(new_label_path, 'a') as f:
        for line in my_list:
            f.write(line)

print('ok')
