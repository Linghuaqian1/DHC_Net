#!/user/bin/env python3
# -*- coding: utf-8 -*-
from shapely.geometry import Polygon


def create_polygon(points):
    """
    创建一个Polygon对象。
    参数：
    points: list, 点的坐标 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)].

    返回：
    polygon: Polygon对象.
    """
    return Polygon(points)


def check_intersection_and_area(points1, points2):
    """
    检查两个旋转检测框是否相交，并计算重叠面积。
    参数：
    points1: list, 检测框1的点坐标 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)].
    points2: list, 检测框2的点坐标 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)].

    返回：
    is_intersect: bool, 是否相交.
    inter_area: float, 重叠面积.
    """
    polygon1 = create_polygon(points1)
    polygon2 = create_polygon(points2)

    intersection = polygon1.intersection(polygon2)
    inter_area = intersection.area

    is_intersect = not intersection.is_empty
    return is_intersect, inter_area


def parse_label_file(label_file_path):
    """
    解析标签文件，将其转换为ground_truths格式。

    参数：
    label_file_path: str, 标签文件的路径。

    返回：
    ground_truths: list, 每个元素为字典，包含真实类别和多边形坐标.
    """
    ground_truths = []

    with open(label_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            category_id = int(parts[0])  # 第一个值是类别ID
            poly = [(float(parts[i]), float(parts[i + 1])) for i in range(1, len(parts), 2)]  # 后面的值是多边形的坐标
            ground_truth = {
                "category_id": category_id,
                "poly": poly
            }
            ground_truths.append(ground_truth)

    return ground_truths


def parse_prediction_file(predictions_ori):
    predictions = []
    for prediction in predictions_ori:
        category_id = prediction['category_id']
        score = prediction['score']
        poly = [(prediction['poly'][i], prediction['poly'][i + 1]) for i in range(0, len(prediction['poly']), 2)]

        formatted_prediction = {
            "category_id": category_id,
            "score": score,
            "poly": poly
        }
        predictions.append(formatted_prediction)
    return predictions


if __name__ == '__main__':
    label_file_path = r"C:\Users\yyj\OneDrive\桌面\论文相关\论文LARS\第一次大改\SODA\labels\val\00012__1024__0___824.txt"  # 标签文件的路径
    ground_truths = parse_label_file(label_file_path)
    print(ground_truths)

