# encoding=utf-8
from PIL import ImageFile,Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from ultralytics import YOLO

if __name__=='__main__':
    # Load a model
    # model = YOLO(r'yolov8+ECA_c2f223.yaml')
    # model = YOLO(r'yolov8-obb-ACA.yaml')
    # # model = YOLO(r'E:\yyj_file\yolo8\结果\Conv_ECA_c2f2\weights\best.pt')
    # # model = YOLO(r'E:\yyj_file\yolo8\结果\Conv_ECA_c2f2\weights\best.pt')  # load a pretrained model (recommended for training)
    #
    model = YOLO(r'E:\yyj_file\yolo8\runs\obb\train126\weights\best.pt')
    # model = YOLO(r'E:\yyj_file\yolo8\runs\obb\train55\weights\best.pt')  # load a pretrained model (recommended for training)
    metric = model.val(data="SODA-A-ori.yaml",imgsz=[4800,2800],iou=0.5,batch=1,workers=0,device=0,save_json=True)
    # # os.environ['CUDA_VISIBLE_DEVICES']='0,1'
    # # Train the model with GPU
    # results = model.train(data='SODA-A.yaml', batch=8,workers=4,epochs=12,device=1, imgsz=1024)



