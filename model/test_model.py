import os
from math import sqrt

import numpy as np
import torch
from torch.utils.data import DataLoader
from matplotlib import pyplot as plt

from model.Resnet import getModel
from process.plt_all_data import read_fgo_data
from train import SatelliteDataset
from utils.gnss_process_util import RationFileUtil, FGOHelper, getLatLonWithMeter


def model_init(load_model_path):
    _model = getModel()
    _model.load_state_dict(torch.load(load_model_path))
    _model.eval()
    return _model


def read_data(path, st=300):
    ratio = RationFileUtil(path=path)
    print(ratio.get_avg())
    test_location = np.array(ratio.get_train_location_data()).astype(np.float64)[st:]
    test_data = np.array(ratio.sat_data).astype(np.float64)[st:]
    test_labels = np.array(ratio.get_opt_label())[st:]
    test_loader = DataLoader(SatelliteDataset(test_data, test_labels), batch_size=1, shuffle=False)
    return test_loader, test_location, test_labels


def test_model():
    res = []
    # 对测试集进行推理，并计算准确度
    with torch.no_grad():
        val_accuracy = 0
        for val_batch in data_loader:
            val_x, val_y = val_batch
            pred_y = model(val_x)
            pred_y = torch.argmax(pred_y, dim=1)
            val_accuracy += (pred_y == val_y.flatten()).sum().item()
            res.append(pred_y)

        val_accuracy /= len(data_loader.dataset)
        print("test_accuracy:", val_accuracy)
    return res


color_or = '#F27F32'
color_green = '#368A34'
color_blue = '#3586FF'


def plt_data(_location_data, _pred_data, inter=10):
    plt.xlabel('Latitude Err(m)')
    plt.ylabel('Longitude Err(m)')
    for i in range(0, len(_location_data), inter):
        # 绘制原始值
        if float(_location_data[i][8]) >= 1.5:
            plt.scatter(_location_data[i][5], _location_data[i][6], c='black')
        else:
            plt.scatter(_location_data[i][2], _location_data[i][3], c='black')
        # 绘制预测值
        if _pred_data[i] == 1:
            plt.scatter(_location_data[i][5], _location_data[i][6], c=color_blue, alpha=0.5)
        else:
            plt.scatter(_location_data[i][2], _location_data[i][3], c=color_blue, alpha=0.5)
    plt.show()


def compute_err(_location_data, _pred_data):
    deep_err = 0
    err = 0
    n = len(_location_data)
    for i in range(n):
        if float(_location_data[i][8]) >= 1.5:
            err = err + sqrt(pow(_location_data[i][5], 2) + pow(_location_data[i][6], 2))
        else:
            err = err + sqrt(pow(_location_data[i][2], 2) + pow(_location_data[i][3], 2))
        # 绘制预测值
        if _pred_data[i] == 1:
            deep_err = deep_err + sqrt(pow(_location_data[i][5], 2) + pow(_location_data[i][6], 2))
        else:
            deep_err = deep_err + sqrt(pow(_location_data[i][2], 2) + pow(_location_data[i][3], 2))
    print("err:", err / n)
    print("deep_err:", deep_err / n)


def compute_fgo_err(fgo_data: FGOHelper, _pred_data, st=300):
    deep_err = 0
    err = 0
    n = len(fgo_data.float_lon)
    # 经纬度转化为m为单位，参考点选择根据rtklib原始定位数据的平均值
    avg_x, avg_y = fgo_data.get_avg()
    float_x, float_y = getLatLonWithMeter(
        fgo_data.float_lat[st:], fgo_data.float_lon[st:], avg_x, avg_y)

    fix_x, fix_y = getLatLonWithMeter(
        fgo_data.fix_lat[st:], fgo_data.fix_lon[st:], avg_x, avg_y)

    ration = fgo_data.ration[st:]
    n = len(float_x)
    print("fgo_data_len:", n)
    for i in range(3502, 4202):
        if float(ration[i]) >= 1.5:
            err = err + sqrt(pow(fix_x[i], 2) + pow(fix_y[i], 2))
        else:
            err = err + sqrt(pow(float_x[i], 2) + pow(float_y[i], 2))
        # 绘制预测值
        if _pred_data[i] == 1:
            deep_err = deep_err + sqrt(pow(fix_x[i], 2) + pow(fix_y[i], 2))
        else:
            deep_err = deep_err + sqrt(pow(float_x[i], 2) + pow(float_y[i], 2))
    print("fgo_err:", err / 700)
    print("fgo_deep_err:", deep_err / 700)


def origin_deep_trans_cnt(_location_data, _pred_data):
    fix2float = 0
    float2fix = 0
    n = len(_location_data)
    for i in range(n):
        if float(_location_data[i][8]) >= 1.5 and _pred_data[i] == 0:
            fix2float = fix2float + 1
        if float(_location_data[i][8]) < 1.5 and _pred_data[i] == 1:
            float2fix = float2fix + 1
    print("fix2float_rate: ", fix2float / n)
    print("float2fix_rate: ", float2fix / n)


import torch


def write_list_to_file(lst, filename):
    with open(filename, 'w') as f:
        for tensor in lst:
            f.write(np.array2string(tensor.detach().numpy()) + '\n')


if __name__ == "__main__":
    model = model_init(load_model_path='model/ration_model_3.pth')
    data_loader, location_data, data_labels = read_data(
        'data/3-14/R3-14-1-ration.csv',
        st=0,
    )
    fgo = read_fgo_data("data/3-14/FGO_rtk_30_314h.csv")
    pred_data = test_model()

    write_list_to_file(pred_data, "R3-14-1-pred_data.txt")
    # compute_fgo_err(fgo, pred_data, st=0)
    # 计算结果
    # compute_err(location_data, pred_data)
    # origin_deep_trans_cnt(location_data, pred_data)

    # 画图
    # plt.grid(True, linestyle="--", alpha=0.5)
    # plt_data(location_data, pred_data, inter=10)
