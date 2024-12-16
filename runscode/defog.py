import numpy as np
from PIL import Image


def dark_channel(image, window_size=15):
    """
    计算图像的暗通道图像
    """
    h, w, _ = image.shape
    pad = window_size // 2
    padded_image = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
    dark_channel_image = np.zeros((h, w))

    for y in range(h):
        for x in range(w):
            patch = padded_image[y:y + window_size, x:x + window_size, :]
            dark_channel_image[y, x] = np.min(patch.min(axis=2))

    return dark_channel_image


def estimate_atmospheric_light(image, dark_channel_image, percentile=0.001):
    """
    估计图像的大气光强度
    """
    h, w, _ = image.shape
    flat_dark_channel = dark_channel_image.ravel()
    flat_image = image.reshape(h * w, 3)
    flat_indices = np.argsort(-flat_dark_channel)
    num_pixels = int(percentile * h * w)
    brightest_pixels = flat_indices[:num_pixels]

    atmospheric_light = np.max(flat_image[brightest_pixels], axis=0)
    return atmospheric_light


def transmission_estimate(image, atmospheric_light, omega=0.95, window_size=15):
    """
    估计透射率
    """
    h, w, _ = image.shape
    transmission = np.zeros((h, w))
    for y in range(h):
        for x in range(w):
            transmission[y, x] = 1 - omega * np.min(image[y, x] / atmospheric_light)
    return transmission


def refine_transmission(image, transmission, window_size=15):
    """
    优化透射率
    """
    refined_transmission = np.zeros_like(transmission)
    padded_transmission = np.pad(transmission,
                                 ((window_size // 2, window_size // 2), (window_size // 2, window_size // 2)),
                                 mode='edge')
    for y in range(window_size // 2, image.shape[0] + window_size // 2):
        for x in range(window_size // 2, image.shape[1] + window_size // 2):
            patch = padded_transmission[y - window_size // 2:y + window_size // 2 + 1,
                    x - window_size // 2:x + window_size // 2 + 1]
            refined_transmission[y - window_size // 2, x - window_size // 2] = np.median(patch)
    return refined_transmission


def dehaze(image, omega=0.2, window_size=15, percentile=0.38):
    """
    对图像进行去雾处理
    """
    dark_channel_image = dark_channel(image, window_size)
    atmospheric_light = estimate_atmospheric_light(image, dark_channel_image, percentile)
    transmission = transmission_estimate(image, atmospheric_light, omega, window_size)
    refined_transmission = refine_transmission(image, transmission, window_size)
    dehazed_image = np.zeros_like(image)
    for c in range(3):
        dehazed_image[:, :, c] = (image[:, :, c] - atmospheric_light[c]) / refined_transmission + atmospheric_light[c]
    dehazed_image = np.clip(dehazed_image, 0, 255).astype(np.uint8)
    return dehazed_image


# 使用示例
input_image = np.array(Image.open('E:/LQYY/dataset/DOTA2-1024-split/images/train/P0010__1024__822___824.jpg'))  # 读取输入图像
output_image = dehaze(input_image)  # 进行去雾处理
Image.fromarray(output_image).show()  # 显示结果图像
