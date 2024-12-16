import warnings

warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO(r'yolov8-unfog.yaml')
    model.load(r'E:/yyj_file/ultralytics-main/weight/yolov8n-obb.pt') # loading pretrain weights
    model.train(data='ultralytics/cfg/datasets/DOTAv2obbfog.yaml',
                # 如果大家任务是其它的'ultralytics/cfg/default.yaml'找到这里修改task可以改成detect, segment, classify, pose
                cache=False,
                imgsz=1024,
                epochs=200,
                single_cls=False,  # 是否是单类别检测
                batch=4,
                close_mosaic=10,
                workers=0,
                device='0',
                optimizer='SGD',  # using SGD
                #resume='E:/yyj_file/ultralytics-main/runscode/runs/train/exp21/weights/last.pt', # 如过想续训就设置last.pt的地址
                amp=False,  # 如果出现训练损失为Nan可以关闭amp
                project='runs/train1',
                name='exp',
                #project='runs/train_fog',
                )
