import warnings

warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO(r'yolov3.yaml')
    #model.load(r'E:/yyj_file/ultralytics-main/weight/yolov8n.pt') # loading pretrain weights
    model.train(data='ultralytics/cfg/datasets/hazeNet.yaml',
                # 如果大家任务是其它的'ultralytics/cfg/default.yaml'找到这里修改task可以改成detect, segment, classify, pose
                cache=False,
                imgsz=1024,
                epochs=12,
                single_cls=False,  # 是否是单类别检测
                batch=4,
                close_mosaic=10,
                workers=1,
                device='1',
                optimizer='SGD',  # using SGD
                # resume='', # 如过想续训就设置last.pt的地址
                amp=False,  # 如果出现训练损失为Nan可以关闭amp
                project='runs/train',
                name='exp',
                )
