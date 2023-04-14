import os

import matplotlib.pyplot as plt
import numpy as np
from numpy import mean, std

from gnssHelper.rationHelper import RationFileUtil
from utils.gnss_process_util import train_data_post_process

data_path = 'data/train'
files = os.listdir(data_path)
location_data = np.array([]).astype(np.float64)
sat_data = np.array([]).astype(np.float64)
tag_data = np.array([]).astype(np.float64)
st = 120
cnt = 0
for file in files:
    if file.endswith('.csv'):
        path = os.path.join(data_path, str(file))
        ratio = RationFileUtil(path=path)
        if cnt == 0:
            location_data = np.array(ratio.get_train_location_data()).astype(np.float64)[st:]
            sat_data = np.array(ratio.sat_data).astype(np.float64)[st:]
            tag_data = np.array(ratio.get_opt_label()).astype(np.float64)[st:]
            location_data, sat_data, tag_data = train_data_post_process(location_data, sat_data, tag_data,
                                                                        ratio.origin_x)
        else:
            temp1 = np.array(ratio.get_train_location_data()).astype(np.float64)[st:]
            temp2 = np.array(ratio.sat_data).astype(np.float64)[st:]
            temp3 = np.array(ratio.get_opt_label()).astype(np.float64)[st:]

            temp1, temp2, temp3 = train_data_post_process(temp1, temp2, temp3, ratio.origin_x)
            location_data = np.concatenate((location_data, temp1), axis=0)
            sat_data = np.concatenate((sat_data, temp2), axis=0)
            tag_data = np.concatenate((tag_data, temp3), axis=0)

        cnt = cnt + 1
        print(len(tag_data))
# 对数据进行划分，分为训练集、验证集和测试集
num_samples = location_data.shape[0]
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

train_idx = int(num_samples * train_ratio)
val_idx = int(num_samples * (train_ratio + val_ratio))

train_sat = sat_data[:train_idx]
val_sat = sat_data[train_idx:val_idx]
test_sat = sat_data[val_idx:]

train_tag = tag_data[:train_idx]
val_tag = tag_data[train_idx:val_idx]
test_tag = tag_data[val_idx:]

train_location = location_data[:train_idx]
val_location = location_data[train_idx:val_idx]
test_location = location_data[val_idx:]

if not os.path.exists('data/train/npy/'):
    os.makedirs('data/train/npy')
# 将数据保存为numpy数组
np.save('data/train/npy/train_sat.npy', train_sat)
np.save('data/train/npy/val_sat.npy', val_sat)
np.save('data/train/npy/test_sat.npy', test_sat)
np.save('data/train/npy/train_tag.npy', train_tag)
np.save('data/train/npy/val_tag.npy', val_tag)
np.save('data/train/npy/test_tag.npy', test_tag)
np.save('data/train/npy/train_location.npy', train_location)
np.save('data/train/npy/val_location.npy', val_location)
np.save('data/train/npy/test_location.npy', test_location)
print("train data save success")
