# Copyright 2018 Ori Ben-Moshe - All rights reserved.
from numpy import ndarray
import Geometry
from sys import version_info

if version_info[0] == 3:
    xrange = range


def validate(contour, target_amount):
    if contour is None:
        return False
    elif contour is []:
        return False
    elif type(contour) is ndarray and target_amount > 1:
        return False
    elif type(contour) is list and len(contour) < target_amount:
        return False
    else:
        return True


def xy_center_directions(contour, target_amount, img_size):
    w, h = img_size
    x_ratio = 2000 / w
    y_ratio = 2000 / h
    if not validate(contour, target_amount):
        return False
    if type(contour) is ndarray:
        contour = [contour]
    x_sum = 0
    y_sum = 0
    for currentContour in contour:
        x, y = Geometry.get_contour_center(currentContour)
        x_sum += x
        y_sum += y
    x_res = x_sum / len(contour)
    y_res = y_sum / len(contour)
    x_res *= x_ratio
    y_res *= y_ratio
    return str(x_res).zfill(4) + str(y_res).zfill(4)


def y_center_directions(contour, target_amount, img_size):
    _, h = img_size
    y_ratio = 2000 / h
    if not validate(contour, target_amount):
        return False
    if type(contour) is ndarray:
        contour = [contour]
    y_sum = 0
    for currentContour in contour:
        x, y = Geometry.get_contour_center(currentContour)
        y_sum += y
    y_res = y_sum / len(contour)
    return str(y_res * y_ratio).zfill(4)


def x_center_directions(contour, target_amount, img_size):
    w, _ = img_size
    x_ratio = 2000 / w
    if not validate(contour, target_amount):
        return False
    if type(contour) is ndarray:
        contour = [contour]
    x_sum = 0
    for currentContour in contour:
        x, y = Geometry.get_contour_center(currentContour)
        x_sum += x
    x_res = x_sum / len(contour)
    return str(x_res * x_ratio).zfill(4)
