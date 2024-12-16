# encoding=utf-8
from PIL import ImageFile,Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

from ultralytics import YOLO
import os


if __name__=='__main__':
    # # Load a model
    # model = YOLO(r'E:\yyj_file\yolo8\结果\best.pt')
    # # model = YOLO(r'yolov8+ECA_c2f223.yaml')
    # model = YOLO(r'yolov8-obb-LKA-ACA.yaml')
    # # model = YOLO(r'E:\yyj_file\yolo8\结果\Conv_ECA_c2f2\weights\best.pt')
    # # model = YOLO(r'E:\yyj_file\yolo8\结果\Conv_ECA_c2f2\weights\best.pt')  # load a pretrained model (recommended for training)
    # #
    # # Train the model with GPU
    # results = model.train(data='ImageNet.yaml', batch=1,workers=0,epochs=1,device=0, imgsz=1024)
    # # results = model.train(data='DOTAv2_800x.yaml', batch=4,epochs=300,device=1, imgsz=800)

    model = YOLO(r'E:\yyj_file\yolo8\runs\obb\train126\weights\best.pt')
    # me=model.predict(source=r"E:\yyj_file\datasets\DOTA2.0obb\DOTA2-1024-split\images\val", save=True,save_conf=True,
    #               save_txt=True,name='output1')
    # print('ok')
    # from ultralytics import YOLO
    #
    # Load a model
    # model = YOLO(r'E:\yyj_file\yolo8\结果\best.pt')
    # results = model.val(data=r'DOTAv2obb.yaml')
    # # Validate the model

    metrics = model.val(data=r'SODA-A.yaml')
    print('haha')
    print(metrics.boxes.map)  # 查看目标检测 map50-95 的性能
    print(metrics.box.map50)  # 查看目标检测 map50 的性能
    print(metrics.box.map75)  # 查看目标检测 map75 的性能
    # metrics.box.maps  # 返回一个列表包含每一个类别的 map50-95

