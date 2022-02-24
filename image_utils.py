import cv2
import numpy as np
import my_utils as mut

def crop_image_centered(image, new_width, new_height):
    image_h, image_w, __ = image.shape
    y = int(image_h / 2.) - new_height // 2
    yh = y + new_height
    x = int(image_w / 2.) - new_width // 2
    xw = x + new_width
    y, yh = mut.min_max_clamp(0, image_h, y, yh)
    x, xw = mut.min_max_clamp(0, image_w, x, xw)

    return image[y:yh, x:xw].copy()