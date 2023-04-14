from gnssHelper.BaseGnssHelper import BaseGnssHelper
from utils.gnss_process_util import getRowdata, FloatTrans


class FGOHelper(BaseGnssHelper):

    def __init__(self, path: str, exclude=1):
        super().__init__(path, exclude)
        fgo_arr = []
        for i in range(len(self.data_arr)):
            fgo_arr.append(self.data_arr[i].split(','))

        self.time = getRowdata(fgo_arr, 0)
        self.float_lat = FloatTrans(getRowdata(fgo_arr, 1))
        self.float_lon = FloatTrans(getRowdata(fgo_arr, 2))
        self.float_height = FloatTrans(getRowdata(fgo_arr, 3))
        self.float_enu_x = FloatTrans(getRowdata(fgo_arr, 4))
        self.float_enu_y = FloatTrans(getRowdata(fgo_arr, 5))
        self.float_enu_z = FloatTrans(getRowdata(fgo_arr, 6))

        self.ration = FloatTrans(getRowdata(fgo_arr, 7))
        self.fix_lat = FloatTrans(getRowdata(fgo_arr, 8))
        self.fix_lon = FloatTrans(getRowdata(fgo_arr, 9))
        self.fix_height = FloatTrans(getRowdata(fgo_arr, 10))
        self.fix_enu_x = FloatTrans(getRowdata(fgo_arr, 11))
        self.fix_enu_y = FloatTrans(getRowdata(fgo_arr, 12))
        self.fix_enu_z = FloatTrans(getRowdata(fgo_arr, 13))

        self.lat = [self.float_lat[i] if self.ration[i] < 1.5 else self.fix_lat[i]
                    for i in range(len(self.ration))]
        self.lon = [self.float_lon[i] if self.ration[i] < 1.5 else self.fix_lon[i]
                    for i in range(len(self.ration))]
        self.height = [self.float_height[i] if self.ration[i] < 1.5 else self.fix_height[i]
                       for i in range(len(self.ration))]

        self.Q = [0 if self.ration[i] < 1.5 else 1
                  for i in range(len(self.ration))]
