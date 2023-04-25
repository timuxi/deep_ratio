from math import sqrt

from matplotlib import pyplot as plt
from gnssHelper.FGOHelper import FGOHelper
from gnssHelper.NewFGOHelper import NewFGOHelper
from gnssHelper.RtklibHelper import RtklibHelper

if __name__ == '__main__':
    fgo = FGOHelper("./data/2-23-16-20-zdt-60min/0223_FGO_nopsr_100.csv")
    rtklib = RtklibHelper("./data/2-23-16-20-zdt-60min/rtklibResult.pos",
                          exclude=25,
                          from_fgo=True)
    fgo.plt_z(color='orange')
    rtklib.plt_z(color='green')
    plt.show()
