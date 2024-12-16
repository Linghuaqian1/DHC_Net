# encoding=utf-8
import os

from PIL import ImageFile,Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from ultralytics import YOLO

if __name__=='__main__':
    # Load a model
    model = YOLO(r'yolov8-obb-LBN.yaml')
    # model = YOLO(r'yolov8n-obb.pt')
    # model = YOLO(r'E:\yyj_file\best.pt')
    # # model = YOLO(r'E:\yyj_file\yolo8\结果\Conv_ECA_c2f2\weights\best.pt')  # load a pretrained model (recommended for training)
    #
    # # os.environ['CUDA_VISIBLE_DEVICES']='0,1'
    # # Train the model with GPU
    results = model.train(pretrained=r'E:\yyj_file\best.pt' ,data='DOTAv2obb.yaml', batch=6,workers=2,epochs=50,device=0, imgsz=1024)
    # results = model.train(data='DOTAv2_800x.yaml', batch=4,epochs=300,device=1, imgsz=800)

