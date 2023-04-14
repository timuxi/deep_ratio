import abc
import os
from cmath import cos, pi, sin
from math import sqrt

from matplotlib import pyplot as plt
from numpy import mean

from utils.gnss_process_util import latlon_to_meters


class BaseGnssHelper:

    def __init__(self, path: str, exclude: int):
        print("path=" + path)
        if not os.path.exists(path):
            print('path not exists,path=')
            exit()
        self.path = path

        with open(path, encoding='utf-8') as file:
            content = file.readlines()
            print(content[exclude][:len(content[exclude]) - 1])
            self.data_arr = content[exclude + 1:]

        self.lat = []
        self.lon = []
        self.height = []
        self.Q = []
        self.ns = []
        self.lon_ref = None
        self.lat_ref = None

    def getLatLonWithMeter(self, _lat_ref=None, _lon_ref=None):
        if _lat_ref is not None and _lon_ref is not None:
            lat_ref = _lat_ref
            lon_ref = _lon_ref
        else:
            lat_ref = mean(self.lat[120:])
            lon_ref = mean(self.lon[120:])
        x_arr = []
        y_arr = []
        for i in range(len(self.lat)):
            x, y = latlon_to_meters(self.lat[i], self.lon[i], lat_ref, lon_ref)
            x_arr.append(x)
            y_arr.append(y)
        return x_arr, y_arr

    def compute_float_fix(self):
        n = len(self.Q)
        float_num = 0
        fix_num = 0
        for q in self.Q:
            if q == 0 or q == 2:
                float_num = float_num + 1
            elif q == 1:
                fix_num = fix_num + 1
        print(" n=", n,
              " float_num=", float_num,
              " fix_num=", fix_num
              )
        print("float_num/n=", float_num / n,
              " fix_num/n=", fix_num / n
              )
        pass

    def plt_xy(self, data_start=60, scatter=False, color='black'):
        x, y = self.getLatLonWithMeter(self.lat_ref, self.lon_ref)
        x = x[data_start:]
        y = y[data_start:]

        if not scatter:
            plt.plot(x, y, c=color)
        else:
            for i in range(len(x)):
                plt.scatter(x[i], y[i], c=color)

    def plt_z(self, data_start=60, scatter=False, color='black'):
        z = self.height[data_start:]

        if not scatter:
            plt.plot(z, c=color)
        else:
            for i in range(len(z)):
                plt.scatter(i, z[i], c=color)

    def compute_xy_err(self):
        err = 0
        _x, _y = self.getLatLonWithMeter(self.lat_ref, self.lon_ref)
        for i in range(len(_x)):
            err = sqrt(pow(_x[i], 2) + pow(_y[i], 2))
        err = err / len(_x)
        return err

    def compute_z_err(self, ref_z):
        err = 0
        for _data in self.height:
            err = err + _data - ref_z
        err = err / len(self.height)
        return err
