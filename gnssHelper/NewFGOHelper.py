from gnssHelper.BaseGnssHelper import BaseGnssHelper
from utils.gnss_process_util import getRowdata, FloatTrans


class NewFGOHelper(BaseGnssHelper):

    def __init__(self, path: str, exclude=1):
        super().__init__(path, exclude)
        fgo_arr = []
        for i in range(len(self.data_arr)):
            row = self.data_arr[i].split(',')
            if row[1] == '-nan':
                continue
            else:
                fgo_arr.append(row)

        self.time = getRowdata(fgo_arr, 0)
        self.float_lon = FloatTrans(getRowdata(fgo_arr, 1))
        self.float_lat = FloatTrans(getRowdata(fgo_arr, 2))
        self.float_height = FloatTrans(getRowdata(fgo_arr, 3))

        self.ration = FloatTrans(getRowdata(fgo_arr, 4))
        self.fix_lon = FloatTrans(getRowdata(fgo_arr, 5))
        self.fix_lat = FloatTrans(getRowdata(fgo_arr, 6))
        self.fix_height = FloatTrans(getRowdata(fgo_arr, 7))

        self.lat = [self.float_lat[i] if self.ration[i] < 1.5 else self.fix_lat[i]
                    for i in range(len(self.ration))]
        self.lon = [self.float_lon[i] if self.ration[i] < 1.5 else self.fix_lon[i]
                    for i in range(len(self.ration))]
        self.height = [self.float_height[i] if self.ration[i] < 1.5 else self.fix_height[i]
                       for i in range(len(self.ration))]

        self.Q = [0 if self.ration[i] < 1.5 else 1
                  for i in range(len(self.ration))]
