import numpy as np


def min_max_clamp(min_val, max_val, *vals):
    list = []
    for x in vals:
        x = min(max_val, x)
        x = max(min_val, x)
        list.append(x)
    return (*list,)


def scaled_image_dimensions(width, height, scale):
    new_width = int(width * scale)
    new_height = int(height * scale)
    return new_width, new_height
