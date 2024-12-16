import json
import os

from shapely import Polygon

from xiangjiaoshujv import parse_label_file, parse_prediction_file


def categorize_target(area):
    """
    根据面积分类目标。
    参数：
    area: float, 面积值.

    返回：
    category: str, 目标类别.
    """
    if area < 144:
        return 'es'
    elif 144 <= area < 400:
        return 'rs'
    elif 400 <= area < 1024:
        return 'gs'
    else:
        return 'N'
def calculate_iou(poly1, poly2):
    """
    计算两个多边形的IoU（交并比）。
    参数：
    poly1: list, 第一个多边形的坐标 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)].
    poly2: list, 第二个多边形的坐标 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)].

    返回：
    iou: float, IoU值.
    """
    polygon1 = Polygon(poly1)
    polygon2 = Polygon(poly2)

    if not polygon1.is_valid or not polygon2.is_valid:
        return 0

    inter_area = polygon1.intersection(polygon2).area
    union_area = polygon1.union(polygon2).area
    iou = inter_area / union_area
    return iou
def calculate_precision_recall_by_category(predictions, ground_truths, iou_threshold=0.5):
    """
    根据预测结果和真实标签计算每类目标的精度和召回率。
    参数：
    predictions: list, 每个元素为字典，包含预测类别、置信度得分和多边形坐标.
    ground_truths: list, 每个元素为字典，包含真实类别和多边形坐标.
    iou_threshold: float, IoU阈值，默认为0.5.

    返回：
    metrics_by_category: dict, 每类目标的精度和召回率.
    """
    predictions = sorted(predictions, key=lambda x: x['score'], reverse=True)

    categories = ['es', 'rs', 'gs', 'N']
    metrics_by_category = {category: {'tp': 0, 'fp': 0, 'fn': 0} for category in categories}

    for gt in predictions:
        gt_poly = gt['poly']
        gt_polygon = Polygon(gt_poly)
        area = gt_polygon.area
        category = categorize_target(area)
        metrics_by_category[category]['fn'] += 1

    for pred in predictions:
        pred_poly = pred['poly']
        pred_polygon = Polygon(pred_poly)
        pred_category = pred['category_id']
        area = pred_polygon.area
        category = categorize_target(area)

        best_iou = 0
        best_gt = None

        for gt in ground_truths:
            gt_poly = gt['poly']
            gt_category = gt['category_id']
            if pred_category == gt_category:
                iou = calculate_iou(pred_poly, gt_poly)
                if iou > best_iou:
                    best_iou = iou
                    best_gt = gt

        if best_iou >= iou_threshold and best_gt:
            metrics_by_category[category]['tp'] += 1
            metrics_by_category[category]['fn'] -= 1
        else:
            metrics_by_category[category]['fp'] += 1

    for category in metrics_by_category:
        tp = metrics_by_category[category]['tp']
        fp = metrics_by_category[category]['fp']
        fn = metrics_by_category[category]['fn']
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        metrics_by_category[category]['precision'] = precision
        metrics_by_category[category]['recall'] = recall

    return metrics_by_category
es_tp,rs_tp,gs_tp,N_tp =0,0,0,0
es_fp,rs_fp,gs_fp,N_fp =0,0,0,0
es_fn,rs_fn,gs_fn,N_fn =0,0,0,0
json_file = "E:/yyj_file/yolo8/runs/obb/val27/predictions.json"

with open(json_file, 'r') as f:
    predictions_json = json.load(f)
    image_id_tmp = '00012__1024__0___0'
pre_list = []
with open("E:/yyj_file/record2.txt",'a') as f:
    for i, prediction_main in enumerate(predictions_json):

        if prediction_main['image_id'] == image_id_tmp:
            pre_list.append(prediction_main)

        else:
            label_file_path = "E:/yyj_file/datasets/SODA-A-1024/labels/val绝对/" + image_id_tmp + ".txt"
            if os.path.exists(label_file_path):
                ground_truths = parse_label_file(label_file_path)
                predictions = parse_prediction_file(pre_list)
                metric = calculate_precision_recall_by_category(predictions, ground_truths)
                es_tp += metric['es']['tp']
                es_fp += metric['es']['fp']
                es_fn += metric['es']['fn']
                rs_tp += metric['rs']['tp']
                rs_fp += metric['rs']['fp']
                rs_fn += metric['rs']['fn']
                gs_tp += metric['gs']['tp']
                gs_fp += metric['gs']['fp']
                gs_fn += metric['gs']['fn']
                N_tp += metric['N']['tp']
                N_fp += metric['N']['fp']
                N_fn += metric['N']['fn']
                output = (metric['es']['precision'], metric['es']['recall'],
                          metric['rs']['precision'], metric['rs']['recall'],
                          metric['gs']['precision'], metric['gs']['recall'],
                          metric['N']['precision'], metric['N']['recall'])

                formatted_output = f"{output[0]}, {output[1]}, {output[2]}, {output[3]}, {output[4]}, {output[5]}, {output[6]}, {output[7]}\n"

                f.write(formatted_output)
            pre_list = []
        image_id_tmp = prediction_main['image_id']

    label_file_path = "E:/yyj_file/datasets/SODA-A-1024/labels/val绝对/" + image_id_tmp + ".txt"
    ground_truths = parse_label_file(label_file_path)
    predictions = parse_prediction_file(pre_list)
    metric = calculate_precision_recall_by_category(predictions, ground_truths)

    es_tp += metric['es']['tp']
    es_fp += metric['es']['fp']
    es_fn += metric['es']['fn']
    rs_tp += metric['rs']['tp']
    rs_fp += metric['rs']['fp']
    rs_fn += metric['rs']['fn']
    gs_tp += metric['gs']['tp']
    gs_fp += metric['gs']['fp']
    gs_fn += metric['gs']['fn']
    N_tp += metric['N']['tp']
    N_fp += metric['N']['fp']
    N_fn += metric['N']['fn']
    output = (metric['es']['precision'], metric['es']['recall'],
              metric['rs']['precision'], metric['rs']['recall'],
              metric['gs']['precision'], metric['gs']['recall'],
              metric['N']['precision'], metric['N']['recall'])

    formatted_output = f"{output[0]}, {output[1]}, {output[2]}, {output[3]}, {output[4]}, {output[5]}, {output[6]}, {output[7]}\n"

    f.write(formatted_output)

print('ok')
