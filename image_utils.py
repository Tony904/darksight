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


def scale_by_largest_dim(image, window_w, window_h):
    w = image.shape[1]
    h = image.shape[0]
    sw = window_w / w
    sh = window_h / h
    if sw < sh:
        s = sw
    else:
        s = sh
    new_w = int(w * s)
    new_h = int(h * s)
    scaled_img = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    return scaled_img


def pad_image_to_square(src):
    image = src.copy()
    w = image.shape[1]
    h = image.shape[0]
    top_pad = 0
    bottom_pad = 0
    left_pad = 0
    right_pad = 0
    if w < h:
        right_pad = h - w
        print("Padding right: " + str(right_pad))
        padded = np.pad(image, ((top_pad, bottom_pad), (left_pad, right_pad), (0, 0)), mode='constant')
    elif h < w:
        bottom_pad = w - h
        print("Padding bottom: " + str(bottom_pad))
        padded = np.pad(image, ((top_pad, bottom_pad), (left_pad, right_pad), (0, 0)), mode='constant')
    else:
        # image is already square
        print("No padding. Image is already square.")
        pass
    return padded, bottom_pad, right_pad
