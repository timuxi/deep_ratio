import random

import numpy as np

# 系统模型
def state_model(x):
    return np.array([x])

# 观测模型
def observation_model(x):
    return np.array([x])

# 初始化
def init():
    x = np.array([0.0])  # 状态向量
    P = np.array([1.0])  # 协方差矩阵
    F = np.array([1.0])  # 状态转移矩阵
    Q = np.array([0.01]) # 状态噪声协方差矩阵
    R = np.array([0.1])  # 观测噪声协方差矩阵
    return x, P, F, Q, R

# 卡尔曼滤波
def kalman_filter(z):
    x, P, F, Q, R = init()

    for i in range(len(z)):
        # 预测
        x = np.dot(F, x)
        P = np.dot(np.dot(F, P), F.T) + Q

        # 更新
        K = np.dot(P, (P + R))
        x = x + np.dot(K, z[i] - np.dot(observation_model(x), z[i]))
        P = np.dot((np.eye(len(x)) - np.dot(K, observation_model(x))), P)
        print(x[0])

    return x


test = []

for i in range(1000):
    r = random.uniform(-1, 1)
    test.append(1+r)

z = np.array(test)

# 运行卡尔曼滤波
x = kalman_filter(z)

print("估计的固定值为：", x[0])
