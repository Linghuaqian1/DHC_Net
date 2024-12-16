from PIL import Image
import os

image_dir = r"E:\soda_test\dota_test\images"
label_dir = r"E:\soda_test\dota_test\label"
new_label_dir = r'E:\soda_test\dota_test\new'
if not (os.path.exists(new_label_dir)):
    os.mkdir(new_label_dir)
class_label = ['plane',
               'ship',
               'storage-tank',
               'baseball-diamond',
               'tennis-court',
               'basketball-court',
               'ground-track-field',
               'harbor',
               'bridge',
               'large-vehicle',
               'small-vehicle',
               'helicopter',
               'roundabout',
               'soccer-ball-field',
               'swimming-pool',
               'container-crane',
               'airport',
               'helipad'
               ]
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
            # x,y,w,h
            x_center=format((float(s_split[0])+float(s_split[4]))/2/width,'.6f')
            y_center=format((float(s_split[1])+float(s_split[5]))/2/height,'.6f')
            w=format(abs(float(s_split[4])-float(s_split[0]))/width,'.6f')
            h=format(abs(float(s_split[5])-float(s_split[1]))/height,'.6f')


            my_list.append(
                str(label) + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(w) + ' ' + str(h)+ '\n')

    with open(new_label_path, 'a') as f:
        for line in my_list:
            f.write(line)

print('ok')
