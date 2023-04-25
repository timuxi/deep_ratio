from gnssHelper.BaseGnssHelper import BaseGnssHelper
from utils.gnss_process_util import getRowdata, FloatTrans
import re


class RtklibHelper(BaseGnssHelper):

    def __init__(self, path: str, from_fgo, exclude=23):
        super().__init__(path, exclude)
        rtklib_data_arr = []
        for data in self.data_arr:
            if from_fgo:
                rtklib_data_arr.append([item.strip() for item in data.split(',')])
            else:
                rtklib_data_arr.append(re.split('\s+', str(data)))

        self.time = FloatTrans(getRowdata(rtklib_data_arr, 1))
        self.lat = FloatTrans(getRowdata(rtklib_data_arr, 2))
        self.lon = FloatTrans(getRowdata(rtklib_data_arr, 3))
        self.height = FloatTrans(getRowdata(rtklib_data_arr, 4))
        self.Q = FloatTrans(getRowdata(rtklib_data_arr, 5))
        self.ns = FloatTrans(getRowdata(rtklib_data_arr, 6))
