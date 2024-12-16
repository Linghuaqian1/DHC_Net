import matplotlib.pyplot as plt
#
# # 数据
# from matplotlib.ticker import MultipleLocator
# ["Precision","Recall","mAP50","mAP95"]
# models = ["No add", "LBN", "ACA+LBN", "LKA+LBN", "LKA+ACA+LBN"]
# Precision = [68.61, 67.98, 72.34, 66.54, 73.88]
# Recall = [50.01, 51.38, 51.69, 53.22, 52.06]
# mAP50 = [52.24, 53.63, 54.28, 55.25, 56.74]
# mAP95 = [34.57, 37.72, 37.95, 38.85, 39.68]
#
# # 设置柱状图的颜色和透明度
# colors = ['blue','blue','blue','blue' , 'red']
# alphas = [0.6, 0.6, 0.6, 0.6, 0.8]
#
# # 创建柱状图
# plt.figure(figsize=(5,4))
# bars = plt.bar(models, Precision, color=colors,width=0.8, align='center')
# # bars = plt.bar(models, Recall, color=colors,width=0.6, align='center')
# # bars = plt.bar(models, mAP50, color=colors,width=0.6, align='center')
# # bars = plt.bar(models, mAP95, color=colors,width=0.6, align='center')
#
# # 设置每个柱子的透明度
# for bar, alpha in zip(bars, alphas):
#     bar.set_alpha(alpha)
#
# # 添加标签，并调整字体
# # plt.xlabel('Models (%)', fontsize=14)
# plt.ylabel('Precision (%)', fontsize=14)
# # plt.ylabel('Recall (%)', fontsize=14)
# # plt.ylabel('mAP50 (%)', fontsize=14)
# # plt.ylabel('mAP95 (%)', fontsize=14)
# # plt.title('Precision by Different Models', fontsize=16)
# plt.ylim(50, 80)
# # 斜着显示x轴标签
# plt.xticks(rotation=45, ha='right', fontsize=12)
# plt.yticks(fontsize=12)
#
# # 给最后一个柱子添加边框
# # bars[-1].set_linewidth(2)
# # bars[-1].set_edgecolor('black')
# plt.gca().yaxis.set_major_locator(MultipleLocator(10))
# plt.tight_layout()
# plt.show()





labels = ["PL", "BD", "BR", "GTF", "SV", "LV", "SH", "TC", "BC", "ST", "SBF", "RA", "HA", "SP", "HC", "CC", "AP", "HL",
          "mAP50"]
networks = ["BFM", "HTC", "RT", "MR", "OR", "RRF", "FCOS-O", "PDACL", "ATSS-O", "O-Rep", "DCFL", "OASL", "R3Det",
            "YOLO8", "S2A-Net", "SASM", "Ours"]


# 网络名称列表
# networks = ["BFM", "HTC", "RT", "MR", "OR", "RRF", "FCOS-O", "PDACL", "ATSS-O", "O-Rep", "DCFL", "OASL", "R3Det", "YOLO8", "S2A-Net", "SASM", "Ours"]

#
# 颜色列表，每个类别使用不同的颜色
colors = ['b', 'g','navy',  'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink', 'olive', 'lime', 'cyan', 'teal',
          'indigo', 'gray', 'gold', 'r']




# accuracy = [58.69, 50.34, 53.64, 49.47, 53.28, 53.28, 48.51, 61.21, 49.57, 48.95, 57.66, 57.18, 47.26, 60.62, 49.86, 44.53, 66.26]
accuracy_mAP50 = [36.4, 35.3, 32.1, 42.9, 44.31, 48.1, 50.7, 51.8, 43.5, 44.8, 52.8]
accuracy_mAP50 = [36.4, 35.3, 32.1, 42.9, 44.31, 48.1, 50.7, 51.8, 43.5, 44.8, 52.8]



# networks = ['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7', 'Model8', 'Model9', 'Model10', 'Model11', 'Model12', 'Model13', 'Model14', 'Model15', 'Model16', 'Model17']

colors1 = [("#4865A9")] * (len(networks) - 1) + [("#EF8A43")]


plt.figure(figsize=(10, 6))
bars = plt.bar(networks, accuracy, color=colors1,alpha=0.6)

for bar, acc in zip(bars, accuracy):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{acc}', ha='center', va='bottom')

plt.title('mAP50 of All Class')
plt.xlabel('Models', labelpad=10)
plt.ylabel('mAP50 (%)')
plt.xticks(rotation=45, ha='right')
plt.ylim(min(accuracy) - 3, max(accuracy) + 5)

plt.tight_layout()
plt.show()







