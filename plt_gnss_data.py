from matplotlib import pyplot as plt
from gnssHelper.FGOHelper import FGOHelper
from gnssHelper.RtklibHelper import RtklibHelper

if __name__ == '__main__':
    fgo_icra = FGOHelper("./data/origin_2/orgin2_FGO_100.csv")
    rtklib = RtklibHelper(path="./data/origin_2/origin2_rtklibResult.pos",
                          exclude=25,
                          from_fgo=True
                          )
    fgo_icra.lat_ref = 22.299915404
    fgo_icra.lon_ref = 114.177707462
    rtklib.lat_ref = 22.299915404
    rtklib.lon_ref = 114.177707462

    fgo_icra.plt_xy(color='orange', scatter=True)
    print(fgo_icra.compute_xy_err())
    rtklib.plt_xy(color='green', scatter=True)
    print(rtklib.compute_xy_err())
    plt.show()
