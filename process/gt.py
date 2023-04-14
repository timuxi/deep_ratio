# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 20:25:35 2023

@author: guoch
"""

import math as m
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

def vel(a, t):
    vel = 0
    vel = vel + a*t
    return vel

def motion(f):
    """

    """
    
    A = 10 #振幅
    Am = 2*A 
    T = 1/f #周期
    t = T/4
    a = Am/m.pow((T/4),2)
    Tt = np.arange(0, T, 0.01)
    time = list(Tt)
    output = []
    for i in Tt:
        if 0 <= i < (T/4):
            s = 0.5*a*m.pow(i, 2)
            output.append(s)
        elif (T/4) <= i < (T/2):
            s = A+vel(a, t)*(i-t) + 0.5*(-a)*m.pow(i-t, 2)
            output.append(s)
        elif (T/2) <= i < (T*3/4):
            s = 2*A+0.5*(-a)*m.pow(i-2*t, 2)
            output.append(s)
        else:
            s = A - vel(a, t)*(i-3*t) + 0.5*a*m.pow(i-3*t, 2)
            output.append(s)
   
    # fig = plt.figure(figsize=(8, 4), dpi=300)
    # plt.plot(Tt, output)
    
    path = os.path.abspath('.//')
    fake = []
    fake.append(time)
    fake.append(output)
    fake = list(map(list, zip(*fake)))#转置
    fake= pd.DataFrame(fake)
    fake.to_csv(path + "//fakeharm"+str(f)+".csv",index=False,header=False)
    return output



