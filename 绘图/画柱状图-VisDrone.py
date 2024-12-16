import matplotlib.pyplot as plt



# networks50 = ["UTY5S", "IGUIT","DCFL", "IOD", "HIC-YOLOv5", "QueryDet", "CEASC", "DSH-Net","SAHI","EdgeYOLO", "Ours"]
networks95 = ["UTY5S", "IGUIT", "IOD", "HIC-YOLOv5", "QueryDet", "CEASC", "DSH-Net","Ours"]

# 颜色列表，每个类别使用不同的颜色
colors = ['b', 'g','navy',  'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink', 'olive', 'lime', 'cyan', 'teal',
          'indigo', 'gray', 'gold', 'r']

# accuracy_mAP50 = [36.41, 35.32, 32.14, 42.93, 44.32, 48.15, 50.74, 51.81, 43.59, 44.85, 52.87]
accuracy_mAP95 = [20.18, 20.04,  24.62, 25.95, 28.71, 28.46, 30.94, 33.92]


# colors1 = [("#75A4C9")] * (len(networks50) - 1) + [("#9D69B1")]

colors1 = [("#4865A9")] * (len(networks95) - 1) + [("#EF8A43")]

plt.figure(figsize=(7, 4))
bars = plt.bar(networks95, accuracy_mAP95, color=colors1,alpha=0.6,width=0.8)

for bar, acc in zip(bars, accuracy_mAP95):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{acc}', ha='center', va='bottom',fontsize=10)

plt.title('mAP95 of All Class',fontsize=14)
plt.xlabel('Models', labelpad=10,fontsize=14)
plt.ylabel('mAP95 (%)',fontsize=14)
plt.xticks(rotation=45, ha='right',fontsize=12)
plt.xticks(fontsize=10)
plt.ylim(min(accuracy_mAP95) - 3, max(accuracy_mAP95) + 5)

plt.tight_layout()
plt.show()







