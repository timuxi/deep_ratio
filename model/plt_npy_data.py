import os

import matplotlib.pyplot as plt
import numpy as np

path = 'data/train/npy/'
data_type = 'train'
test_data = np.load(os.path.join(path, data_type + '_sat.npy'))
test_labels = np.load(os.path.join(path, data_type + '_tag.npy'))
test_location = np.load(os.path.join(path, data_type + '_location.npy'))
n = len(test_data)

def plt_npy_data():
    for i in range(0, len(test_location), 10):
        if test_location[i][1] == 1:
            plt.scatter(i, test_location[i][5], color='b')
        else:
            plt.scatter(i, test_location[i][2], color='r')
    plt.title('origin')
    plt.show()
    for i in range(0, len(test_location), 10):
        if test_labels[i] == 1:
            plt.scatter(i, test_location[i][5], color='b')
        else:
            plt.scatter(i, test_location[i][2], color='r')
    fix_cnt = 0
    float_cnt = 0

    for i in range(0, len(test_location)):
        if test_labels[i] == 1 and test_location[i][1] == 0:
            fix_cnt = fix_cnt + 1
        elif test_labels[i] == 0 and test_location[i][1] == 1:
            float_cnt = float_cnt + 1

    print(fix_cnt, float_cnt)
    plt.title('lable')
    plt.show()

    print('down')

def ration_print():
    ration_n = 0
    for i in range(n):
        if test_data[i][151][0] <1.5 and test_labels[i] == 1:
            ration_n = ration_n +1
            print(test_data[i][151][0])
    print(ration_n)

if __name__ == "__main__":
    # ration_print()
    plt_npy_data()
