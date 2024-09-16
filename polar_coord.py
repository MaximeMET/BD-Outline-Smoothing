# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:04:05 2023

@author: maxim
"""
import math
import numpy as np

def cartesian_to_polar(x, y, origin):
    dx = x - origin[0]
    dy = y - origin[1]
    r = np.sqrt(dx**2 + dy**2)
    theta = np.arctan2(dy, dx)/math.pi*180
    return r, theta

def polar_to_cartesian(r, theta, origin):
    x = r * np.cos(theta/180*math.pi) + origin[0]
    y = r * np.sin(theta/180*math.pi) + origin[1]
    return x, y

# 读取数据文件
data = np.loadtxt('data.txt')

# 定义原点
origin = (600, 227)

# 将数据转换为极坐标
polar_data = []
for point in data:
    x, y = point
    r, theta = cartesian_to_polar(x, y, origin)
    polar_data.append([theta, r])
    
# 将极坐标数据写入新的文件
np.savetxt('polar_data.txt', polar_data, fmt='%.6f')

# 将极坐标数据转换为笛卡尔坐标
cartesian_data = []
for point in data:
    theta, r = point
    x, y = polar_to_cartesian(r, theta, origin)
    cartesian_data.append([x, y])

# 将笛卡尔坐标数据写入新的文件
np.savetxt('cartesian_data.txt', cartesian_data, fmt='%.6f')
