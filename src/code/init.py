#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/9 15:31
import numpy as np
from code.config import *
from math import inf
# 结点分布
nodeDistribution = np.loadtxt('../resources/node_distribution.csv', delimiter=',')
# 链路
link = np.loadtxt('../resources/links_std.csv', delimiter=',', dtype=np.int32)
# 计算结点之间距离
dist = np.zeros((numOfN, numOfN))
for i in range(len(dist)):
    dist[i, :] = np.sqrt(np.sum((nodeDistribution[i, :] - nodeDistribution) ** 2, axis=1))
# 节点到自身的距离设为无穷
dist[dist == 0] = inf
minDist = np.min(dist)
# 计算链路源节点和目标结点的距离
distOfLink = np.zeros((numOfL, 1))
for i in range(numOfL):
    distOfLink[i] = dist[link[i, 0], link[i, 1]]
# 生成干扰图
Edge = np.zeros((numOfL, numOfL), dtype=np.int8)

V = np.array([x for x in range(numOfL)])
# 对于每条链路考虑一下三种情况:
# 1. 以F为目标节点的链路
# 2. 以D为目标结点的链路
# 3. 以与F距离小于 radius的结点为目标节点的链路
for i in range(numOfL):
    Edge[i, i] = 1
    F = link[i, 0]
    D = link[i, 1]
    for j in range(numOfL):
        # 以F/D为目标结点的链路
        if link[j, 1] == F or link[j, 1] == D:
            Edge[i, j] = 1
            Edge[j, i] = 1
        #  以与F距离小于 radius的结点为目标节点的链路
        D_2 = link[j, 1]
        distance = dist[F, D_2]
        if distance < radius:
            Edge[i, j] = 1
            Edge[j, i] = 1



