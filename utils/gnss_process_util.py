import os.path
import re
import string
from cmath import pi
from math import cos, sin, sqrt

import numpy as np

from matplotlib import pyplot as plt
from numpy import mean


def detect_outliers(data, threshold=1):
    avg = mean(data)
    std = np.std(data)
    new_data = []
    for i in range(len(data)):
        z_score = (data[i] - avg) / std
        if np.abs(z_score) > threshold:
            continue
        else:
            new_data.append(data[i])
    return new_data


def train_data_post_process(location, sat, tag, origin, threshold=1):
    avg = mean(origin)
    std = np.std(origin)
    new_location = []
    new_sat = []
    new_tag = []
    for i in range(len(location)):
        z_score = (origin[i] - avg) / std
        if np.abs(z_score) > threshold:
            continue
        else:
            if location[i][5] == 0:
                print(i)
                continue
            new_location.append(location[i])
            new_sat.append(sat[i])
            new_tag.append(tag[i])
    # for i in range(len(new_sat)):
    #     if new_sat[i][151][0] > 5 and new_tag[i] == 0:
    #         new_tag[i] = 1
    #     if new_sat[i][151][0] < 1.1 and new_tag[i] == 1:
    #         new_tag[i] = 0

    return np.array(new_location), np.array(new_sat), np.array(new_tag)


def getRowdata(arr, index):
    return [row[index] for row in arr]


def FloatTrans(arr):
    return list(map(float, arr))


def latlon_to_meters(lat, lon, lat_ref, lon_ref):
    a = 6378137  # WGS-84椭球体长半轴，单位为米
    f = 1 / 298.257223563  # WGS-84椭球体扁率
    lat_ref = lat_ref  # 参考点的纬度
    lon_ref = lon_ref  # 参考点的经度

    # 计算赤道半径上的弧长
    eq_radius = a * cos(lat_ref * pi / 180)

    # 计算该纬度上的弧长
    meridian_radius = a * (1 - f) / (1 - f * sin(lat_ref * pi / 180) ** 2)
    x_ref = eq_radius * (lon_ref - lon_ref) * pi / 180
    y_ref = meridian_radius * (lat_ref - lat_ref) * pi / 180

    # 计算每个点的x和y坐标
    x = eq_radius * (lon - lon_ref) * pi / 180
    y = meridian_radius * (lat - lat_ref) * pi / 180

    # 将坐标转化为以米为单位
    x_meters = x * cos(lat_ref * pi / 180)
    y_meters = y

    return x_meters, y_meters


def getLatLonWithMeter(lat, lon, lat_ref, lon_ref):
    x_arr = []
    y_arr = []
    for i in range(len(lat)):
        x, y = latlon_to_meters(lat[i], lon[i], lat_ref, lon_ref)
        x_arr.append(x)
        y_arr.append(y)
    return x_arr, y_arr





