from PIL import Image
import os
import json

image_dir = r"E:\soda_test\soda-a\images"
label_dir = r"E:\soda_test\soda-a\labels"
new_label_dir = r'E:\soda_test\labels\new'
if not (os.path.exists(new_label_dir)):
    os.mkdir(new_label_dir)
# class_A_label = {'airplane': 0,
#                'helicopter': 1,
#                'small-vehicle': 2,
#                'large-vehicle': 3,
#                'ship': 4,
#                'container': 5,
#                'storage-tank': 6,
#                'swimming-pool': 7,
#                'windmill': 8,
#                'ignore':9
#                }
class_A_label = ['airplane', 'helicopter', 'small-vehicle',
                 'large-vehicle', 'ship',
                 'container', 'storage-tank',
                 'swimming-pool', 'windmill', 'ignore'
                 ]
class_D_label = {'people': 0,
                 'rider': 1,
                 'bicycle': 2,
                 'motor': 3,
                 'vehicle': 4,
                 'traffic-sign': 5,
                 'traffic-light': 6,
                 'traffic-camera': 7,
                 'warning-cone': 8
                 }
for label_name in os.listdir(label_dir):
    my_list = []
    # 获取标签的完整路径
    label_path = os.path.join(label_dir, label_name)
    # 获取标签的扩展名
    ext = os.path.splitext(label_name)[-1]
    # 根据扩展名替换成对应的image文件名
    image_name = label_name.replace(ext, ".jpg")
    new_label_name = label_name.replace(ext, ".txt")
    image_path = os.path.join(image_dir, image_name)
    new_label_path = os.path.join(new_label_dir, new_label_name)
    img = Image.open(image_path)
    width, height = img.size
    json_file = json.load(open(label_path, 'r'))
    for i in range(len(json_file["annotations"])):
        s_split = json_file["annotations"][i]["poly"]
        # label = class_A_label[json_file["annotations"][i]["category_id"]]
        label=json_file["annotations"][i]["category_id"]
        # x1 = format(float(s_split[0]) / width, '.6f')
        # y1 = format(float(s_split[1]) / height, '.6f')
        # x2 = format(float(s_split[2]) / width, '.6f')
        # y2 = format(float(s_split[3]) / height, '.6f')
        # x3 = format(float(s_split[4]) / width, '.6f')
        # y3 = format(float(s_split[5]) / height, '.6f')
        # x4 = format(float(s_split[6]) / width, '.6f')
        # y4 = format(float(s_split[7]) / height, '.6f')
        x1 = format(float(s_split[0]), '.6f')
        y1 = format(float(s_split[1]), '.6f')
        x2 = format(float(s_split[2]), '.6f')
        y2 = format(float(s_split[3]), '.6f')
        x3 = format(float(s_split[4]), '.6f')
        y3 = format(float(s_split[5]), '.6f')
        x4 = format(float(s_split[6]), '.6f')
        y4 = format(float(s_split[7]), '.6f')
        # my_list.append(
        #     str(label) + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(x3) + ' ' + str(
        #         y3) + ' ' + str(x4) + ' ' + str(y4) + '\n')

        my_list.append(
            str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(x3) + ' ' + str(
                y3) + ' ' + str(x4) + ' ' + str(y4) + ' ' + str(label) + ' ' + '\n')

    with open(new_label_path, 'a') as f:
        for line in my_list:
            f.write(line)
print('ok')
#     with open(label_path, 'r') as f:
#         for line in f:
#             s_split = line.split()
#             label = class_A_label[s_split[8]]
#             x1 = format(float(s_split[0]) / width, '.6f')
#             y1 = format(float(s_split[1]) / height, '.6f')n
#             x2 = format(float(s_split[2]) / width, '.6f')
#             y2 = format(float(s_split[3]) / height, '.6f')
#             x3 = format(float(s_split[4]) / width, '.6f')
#             y3 = format(float(s_split[5]) / height, '.6f')
#             x4 = format(float(s_split[6]) / width, '.6f')
#             y4 = format(float(s_split[7]) / height, '.6f')
#
#             my_list.append(
#                 str(label) + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(x3) + ' ' + str(
#                     y3) + ' ' + str(x4) + ' ' + str(y4) + '\n')
#
#     with open(new_label_path, 'a') as f:
#         for line in my_list:
#             f.write(line)
#
# print('ok')
#
#
# json_str = str.replace("'",'"')
# # json.loads() ,要求json串格式中必须的双引号！！转换为字典
# with open (r'E:\soda_test\labels\00002.json') as f:
#     json.load(r'on',)
# json_dict = json.loads(json_str)
# print(json_dict['pic_str'])
#
#
#
#
#
