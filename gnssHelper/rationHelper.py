from cmath import sqrt

import numpy as np
from matplotlib import pyplot as plt
from numpy import mean

from utils.BaseGnssHelper import BaseGnssHelper
from utils.gnss_process_util import getRowdata, FloatTrans, getLatLonWithMeter


def sat_data_init():
    return [[[0.] * 17 for _ in range(151)] for _ in range(3)]


class RationFileUtil(BaseGnssHelper):

    def __init__(self, path: str, exclude=0):
        super().__init__(path, exclude)
        location_data = []
        self.sat_data = []
        temp = sat_data_init()
        for data in self.data_arr:
            row = data.split(',')
            number = int(row[0])
            if number > 500:
                if temp != sat_data_init():
                    self.sat_data.append(temp)
                    temp = sat_data_init()
                location_data.append(row[:len(row) - 1])
            else:
                receive = int(row[2]) - 1
                data = list(map(float, row[:17]))
                temp[receive][number] = data

        self.sat_data.append(temp)
        self.location_data = location_data
        # 最后行加入ration
        for i in range(len(self.sat_data)):
            ration = location_data[i][len(location_data[0]) - 2]
            self.sat_data[i][2][0][0] = float(ration)
        self.sat_data = np.array(self.sat_data)

        self.time = getRowdata(location_data, 0)
        self.Q = FloatTrans(getRowdata(location_data, 1))

        self.float_lat = FloatTrans(getRowdata(location_data, 2))
        self.float_lon = FloatTrans(getRowdata(location_data, 3))
        self.float_height = FloatTrans(getRowdata(location_data, 4))

        self.fix_lat = FloatTrans(getRowdata(location_data, 5))
        self.fix_lon = FloatTrans(getRowdata(location_data, 6))
        self.fix_height = FloatTrans(getRowdata(location_data, 7))
        # self.ration = FloatTrans(getRowdata(location_data, 8))

        for i in range(len(location_data)):
            if self.Q[i] == 0:
                self.lat.append(self.float_lat[i])
                self.lon.append(self.float_lon[i])
                self.height.append(self.float_height[i])
            else:
                self.lat.append(self.fix_lat[i])
                self.lon.append(self.fix_lon[i])
                self.height.append(self.fix_height[i])

    def plt_float_data(self, st=120):
        for i in range(st, len(self.float_lon)):
            plt.scatter(i, self.float_lat[i], color='yellow')

    def plt_fix_data(self, st=120):
        for i in range(st, len(self.float_lon)):
            plt.scatter(i, self.fix_lat[i], color='green')

    def get_avg(self):
        st = 300
        process_x = self.lat[st:]
        process_y = self.lon[st:]
        process_z = self.height[st:]
        return mean(process_x), mean(process_y), mean(process_z)

    def get_opt_label(self):
        avg_x, avg_y, avg_z = self.get_avg()
        float_x, float_y = getLatLonWithMeter(self.float_lat, self.float_lon, avg_x, avg_y)
        fix_x, fix_y = getLatLonWithMeter(self.fix_lat, self.fix_lon, avg_x, avg_y)
        tag_arr = []
        for i in range(len(float_x)):
            float_err = sqrt(pow(float_x[i], 2) + pow(float_y[i], 2))
            fix_err = sqrt(pow(fix_x[i], 2) + pow(fix_y[i], 2))
            if float_err < fix_err:
                tag_arr.append(0)
            else:
                tag_arr.append(1)
        return tag_arr

    def get_train_location_data(self):
        avg_x, avg_y, avg_z = self.get_avg()
        float_x, float_y = getLatLonWithMeter(self.float_lat, self.float_lon, avg_x, avg_y)
        fix_x, fix_y = getLatLonWithMeter(self.fix_lat, self.fix_lon, avg_x, avg_y)
        train_location_data = self.location_data
        for i in range(len(float_x)):
            train_location_data[i][2] = float_x[i]
            train_location_data[i][3] = float_y[i]
            train_location_data[i][5] = fix_x[i]
            train_location_data[i][6] = fix_y[i]
        return train_location_data
