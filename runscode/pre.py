from ultralytics import YOLO
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

# Load a model
model = YOLO(r'weight/yolov8n-obb.pt')  # load an official model
model = YOLO(r'E:/yyj_file/ultralytics-main/runscode/runs/train/exp20/weights/best.pt')  # load a custom model

# Predict with the model
#E:/LQYY/dataset/dota2_800/images/val_fog
results = model.predict(r'E:/LQYY/dataset/dota2_800/images/val_fog',save=True)  # predict on an image
plot = results[0].plot()

# for result in results:
#     boxes = result.boxes  # Boxes object for bounding box outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     result.show()  # display to screen
#     result.save(filename='result6.jpg')  # save to disk