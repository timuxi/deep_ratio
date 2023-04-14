import os

import numpy as np

from utils.gnss_process_util import RationFileUtil


if __name__ == "__main__":
    out_filename = "2-13-80min"
    # 去掉前2分钟的数据
    st = 600
    ratio = RationFileUtil(path='data/train/R2-13-08-54-80min-ration.csv')
    location_data = np.array(ratio.get_train_location_data()).astype(np.float64)[st:]
    sat_data = np.array(ratio.sat_data).astype(np.float64)[st:]
    tag_data = np.array(ratio.get_opt_label())[st:]
    path = 'data/npy/'+out_filename
    # 保存路径
    if not os.path.exists(path):
        os.makedirs(path)
    np.save(path+'/location_data.npy', location_data)
    np.save(path+'/sat_data.npy', sat_data)
    np.save(path+'/tag_data.npy', tag_data)
    print('save success')

