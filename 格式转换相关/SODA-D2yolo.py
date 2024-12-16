import json
import os
from PIL import Image

image_dir = r"E:\soda_test\images"
label_path = r"E:\soda_test\labels\train.json"
new_label_dir = r'E:\soda_test\new'
if not (os.path.exists(new_label_dir)):
    os.mkdir(new_label_dir)
count=0

# 获取标签的完整路径
with open(label_path) as f:
    k = json.load(f)
    for i in k['images']:
        a = []
        img_name = i['file_name']
        img_height, img_width = i['height'], i['width']
        image_path = os.path.join(image_dir, img_name)
        ext=img_name.split('.')
        # x1,y1,w1,h1=k['annotations'][count]['bbox']
        for m in k['annotations']:
            if m['image_id'] == i['id']:
                x1,y1,w1,h1=m['bbox']
                label = m['category_id']
                x = format(x1 / img_width,'.8f')
                y = format(y1 / img_height,'.8f')
                w = format(w1 / img_width,'.8f')
                h = format(h1 / img_height,'.8f')
                a.append(str(label) + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n')
        # box = [m['bbox'] for m in k['annotations'] if m['image_id'] == i['id']]
        # label = [m['category_id'] for m in k['annotations'] if m['image_id'] == i['id']]
        # label=k['annotations'][count]["category_id"]
        # 获取图片的扩展名
        ext = os.path.splitext(img_name)[-1]
        # 根据扩展名替换成对应的label文件名
        new_label_name = img_name.replace(ext, ".txt")
        new_label_path=os.path.join(new_label_dir,new_label_name)
        with open(new_label_path, 'a') as f:
            print(new_label_path)
            for line in a:
                f.write(line)


    # 获取标签的扩展名
    # ext = os.path.splitext(label_name)[-1]
    # # 根据扩展名替换成对应的image文件名
    # image_name = label_name.replace(ext, ".jpg")
    # label_new_name=label_name.replace(ext, ".txt")
    # image_path = os.path.join(image_dir, image_name)
    # new_label_path = os.path.join(new_label_dir, label_new_name)
    # img = Image.open(image_path)
    # width, height = img.size

    # with open(label_path) as f:
    #     j = json.load(f)
    #     num = j['annotations'][-1]['id']
    #     for i in range(num):
    #         x = j['annotations'][i]['poly']
    #         label = j['annotations'][i]['category_id']
    #         x_cent = format(float(x[4] + x[0]) / 2 / width, '.8f')
    #         y_cent = format((x[5] + x[1]) / 2 / height, '.8f')
    #         w = abs(float(format((x[4] - x[0]) / width, '.8f')))
    #         h = abs(float(format((x[5] - x[1]) / height, '.8f')))
    #
    #
    #
    #         a.append(str(label) + ' ' + str(x_cent) + " " + str(y_cent) + " " + str(w) + " " + str(h) + "\n")
    #
    # with open(new_label_path, 'a') as f:
    #     print(new_label_path)
    #     for line in a:
    #         f.write(line)
