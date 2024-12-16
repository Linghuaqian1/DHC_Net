from ultralytics import YOLO


if __name__ == '__main__':
    # Load a model
    model = YOLO(r'E:/yyj_file/ultralytics-main/weight/yolov8n.pt')  # load an official model
    model = YOLO('E:/yyj_file/ultralytics-main/runscode/runs/train/exp55/weights/best.pt')  # load a custom model
    #E:\yyj_file\ultralytics - main\runscode\runs\train\exp55
    # Validate the model
    #metrics = model.val(data='ultralytics/cfg/datasets/DOTAv2_800_fog.yaml')  # no arguments needed, dataset and settings remembered
    metrics = model.val(
        data='ultralytics/cfg/datasets/hazeNet.yaml')  # no arguments needed, dataset and settings remembered
    metrics.box.map    # map50-95(B)
    metrics.box.map50  # map50(B)
    metrics.box.map75  # map75(B)
    metrics.box.maps   # a list contains map50-95(B) of each category