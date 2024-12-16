import matplotlib.pyplot as plt
import numpy as np

# Networks and their respective accuracies
networks = ["UTY5S", "IGUIT","DCFL", "IOD", "HIC-YOLOv5", "QueryDet", "CEASC", "DSH-Net","SAHI","EdgeYOLO", "Ours"]
accuracy_mAP50 = [36.4, 35.3, 32.1, 42.9, 44.31, 48.1, 50.7, 51.8,43.5,44.8,52.8]
accuracy_mAP95 = [20.1, 20.0,0, 24.6, 25.9, 28.7, 28.4, 30.9, 0,0,33.9]

# Setting the positions and width for the bars
bar_width = 0.4
index = np.arange(len(networks))

# Colors for the bars
colors_mAP50 = [("#75A4C9")] * (len(networks) - 1) + [("#9D69B1")]
colors_mAP95 = [("#4865A9")] * (len(networks) - 1) + [("#EF8A43")]

# Plotting the bars
plt.figure(figsize=(10, 6))
bars1 = plt.bar(index, accuracy_mAP50, bar_width, color=colors_mAP50, alpha=0.6, label='mAP50')
bars2 = plt.bar(index + bar_width, accuracy_mAP95, bar_width, color=colors_mAP95, alpha=0.6, label='mAP95')

# Adding text labels above the bars
for bar, acc in zip(bars1, accuracy_mAP50):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{acc}', ha='center', va='bottom', fontsize=12)

for bar, acc in zip(bars2, accuracy_mAP95):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{acc}', ha='center', va='bottom', fontsize=12)

# Adding the title and labels
plt.title('mAP50 and mAP95 of All Class', fontsize=14)
plt.xlabel('Models', labelpad=10, fontsize=14)
plt.ylabel('Performance (%)', fontsize=14)
plt.xticks(index + bar_width / 2, networks, rotation=45, ha='right', fontsize=14)
plt.ylim(min(min(accuracy_mAP50), min(accuracy_mAP95)) - 3, max(max(accuracy_mAP50), max(accuracy_mAP95)) + 5)

# Adding the legend
plt.legend(fontsize=12)

# Adjusting the layout
plt.tight_layout()
plt.show()
