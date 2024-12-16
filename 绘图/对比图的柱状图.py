#!/user/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import os
import numpy as np
#

# #
labels = ["PL", "BD", "BR", "GTF", "SV", "LV", "SH", "TC", "BC", "ST", "SBF", "RA", "HA", "SP", "HC", "CC", "AP", "HL",
          "mAP50"]
networks = ["HTC", "OR", "MR", "BFM","RT" , "ATSS-O","O-Rep","YOLO8","SASM","R3Det","S2A-Net","RRF", "FCOS-O", "RHINO", "OASL", "DCFL",
            "Ours"]

colors = ['b', 'g','navy',  'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink', 'olive', 'lime', 'cyan', 'teal',
          'indigo', 'gray', 'gold', 'r']

# 绘制折线图

accuracy = [50.34, 53.28, 49.47, 58.69, 53.64, 49.57, 48.95, 58.51, 44.53, 47.26, 49.86, 53.28, 48.51, 59.26, 57.18, 57.66, 60.85]
# networks = ['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7', 'Model8', 'Model9', 'Model10', 'Model11', 'Model12', 'Model13', 'Model14', 'Model15', 'Model16', 'Model17']

colors1 = ['c'] * (len(networks) - 1) + [(1, 0, 0, 0.6)]


plt.figure(figsize=(10, 6))
bars = plt.bar(networks, accuracy, color=colors1)

for bar, acc in zip(bars, accuracy):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{acc}', ha='center', va='bottom')

plt.title('mAP50 of All Class',fontsize=16)
# plt.xlabel('Models', labelpad=10,fontsize=16)
plt.ylabel('mAP50 (%)',fontsize=16)
plt.xticks(rotation=45, fontsize=12,ha='right')
plt.ylim(min(accuracy) - 3, max(accuracy) + 5)

plt.tight_layout()
plt.savefig(r'D:\syd迪马\孙煜东18个对比图\总map50.png')

plt.show()

