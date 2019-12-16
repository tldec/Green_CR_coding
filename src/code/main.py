#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:31
from math import inf
from code.config import *
from code.Graph import Graph
from code.init import *
from code.energyQModel import *
from code.dataQModel import *
from code.virtualQModel import *
from code.channelAllocationModel import *
from code.flowQModel import *
import matplotlib.pyplot as plt
import random
import datetime
from code.plot import *

# 初始化结点能量队列
enQ = np.zeros((numOfN, timeSlots))
enQe = np.zeros((numOfN, timeSlots, len(epsilons)))
# 能量队列上界
enQ_max = np.zeros(len(weights))
# 初始化结点数据队列
dataQ = np.zeros_like(enQ)
dataQe = np.zeros_like(enQe)
# 数据队列上界
dataQ_max = np.zeros_like(enQ_max)
# 初始化结点虚拟队列
virtualQ = np.zeros_like(enQ)
virtualQe = np.zeros((numOfN, timeSlots, len(weights)))
# 虚拟队列上界
virtualQ_max = np.zeros_like(enQ_max)
# 初始化每个结点的网络效益
# sum_{n:N} f(h_n - d_n)
utility = np.zeros((numOfN, timeSlots))
# 平均网络效益-权重
aveUtility = np.zeros((len(weights),len(epsilons)))
# 每个时结点之间的流量
trafficOverSlot = np.zeros((timeSlots, len(epsilons)))
# 记录每个时隙结点发送的数据
dataTransM = np.zeros((numOfN, timeSlots))
# 记录每个时隙结点接收的数据
dataRecvM = np.zeros_like(dataTransM)
# 记录每个结点收集的数据
dataHarM = np.zeros_like(dataTransM)
# 记录每个结点丢弃的数据
dataDropM = np.zeros_like(dataTransM)
# 记录每个结点采集的能量
enHarM = np.zeros_like(dataTransM)
# 记录每个结点消耗的能量
enConM = np.zeros_like(dataTransM)
# 记录信道分配结果
caResultM = np.zeros((numOfL, numOfCH, timeSlots))
# 每个时隙被分配信道的链路数
numofCA = np.zeros((timeSlots, len(weights)))
# 记录历史信道状态和信道容量
state = np.zeros((numOfCH, 1, timeSlots, len(epsilons)))
chCap = np.zeros((numOfL, numOfCH, timeSlots, len(epsilons)))
# 数据丢弃上限
dropMax = np.zeros(len(epsilons))
# 记录每个时隙丢弃的数据量
dropMe = np.zeros((timeSlots, len(epsilons)))

# 信道可接入概率
# 主用户信道状态集 0 表示不可用 1 表示可用
access = [0, 1]
# 主用户可接入概率
p = [0.4, 0.6]
P_R = para / distOfLink
maxPR = np.max(P_R)
# 最大能耗
P_max = max(P_T * tau * 0.3, maxPR * tau * 0.3) + P_H * dataArrival_max

fpath = "E:\\data\\"
def KMWIS():
    start = datetime.datetime.now()
    print("KMWIS begins")
    chMax = bandWidth * np.log2(1 + P_T * 1.5) / ((minDist ** 2) * noise) / 1000
    # print("chMax", chMax)
    # for e in range(len(epsilons)):
    #     epsilon = epsilons[e]
    #     dropMax[e] = max(epsilon, (dataArrival_max + chMax))
    # W_1 = (chMax / P_T) * (weights * beta * maxSlop + epsilons + weights * maxSlop + chMax + 2 * dataArrival_max)
    # W_2 = (1 / P_H) * (weights * maxSlop + dataArrival_max + chMax)
    # for w in range(len(weights)):
    #     enQ_max[w] = max(W_1[w], W_2[w])
    #     dataQ_max[w] = weights[w] * maxSlop + 2 * dataArrival_max + chMax
    for e in range(len(epsilons)):
        epsilon = epsilons[e]
        dropMax[e] = max(epsilon, (dataArrival_max + chMax))
        W_1 = (chMax / P_T) * (weights * beta * maxSlop + epsilon + weights * maxSlop + chMax + 2 * dataArrival_max)
        W_2 = (1 / P_H) * (weights * maxSlop + dataArrival_max + chMax)
        for w in range((len(weights))):
            weight = weights[w]
            enQ_max[w] = max(W_1[w], W_2[w])
            dataQ_max[w] = weights[w] * maxSlop + 2 * dataArrival_max + chMax
            for n in range(numOfN):
                enQ[n, 0] = enQ_max[w] * initCapacityRate
            for t in range(timeSlots - 1):
                chState = np.random.choice(access, (numOfCH, 1), p)
                channelCapacity = bandWidth * (weight / 1000) * np.log2(
                    1 + P_T * (np.random.rand(numOfL, numOfCH) + 0.5) / \
                    ((distOfLink ** 2) * noise)) * chState.T
                state[:, :, t, e] = chState.reshape(state[:, :, t, e].shape)
                chCap[:, :, t, e] = channelCapacity.reshape(chCap[:, :, t, e].shape)

                enHarVec = computeEnHar(enQ, enQ_max[w], t)
                enHarM[:, t] = enHarVec.T

                dataHarVec = computeDataHar(dataQ, enQ, enQ_max[w], w, t)
                dataHarM[:, t] = dataHarVec.T
                # Edge, enQ, dataQ, virtualQ, links, chCap, batterCapacity, P_R, chState, P_max, alg, t
                caResults = channelAllocation(Edge, enQ, dataQ, virtualQ, link, channelCapacity, enQ_max[w], P_R,chState,P_max,"kmwis",t)
                dataTransVec, dataRecvVec = computeTransRecv(caResults, link, dist, channelCapacity, dataQ, t)
                numofCA[t,w] = np.sum(caResults)
                dataDropVec = computeDrop(virtualQ, dataQ, dataTransVec, weight, dropMax[e], t)
                dataDropM[:, t] = dataDropVec.T
                enConVec = computeEnConsumption(caResults, link, distOfLink, dataHarVec)
                for n in range(numOfN):
                    if n != 0:
                        tmp = dataHarVec[n] - dataDropVec[n] + 1
                        if tmp < 0:
                            utility[n, t] = 0
                        else:
                            if np.log(tmp) < 0:
                                utility[n, t] = 0
                            else:
                                utility[n, t] = np.log(tmp)
                    else:
                        utility[0, t] = 0
                updateEnQ(enQ, enHarVec, enConVec, enQ_max[e], t)
                updateDataQ(dataQ, dataHarVec, dataTransVec, dataRecvVec, dataDropVec, t)
                updateVirtualQ(virtualQ, dataQ, epsilon, dataTransVec, dataDropVec, chMax, t)
            aveUtility[w,e] = np.sum(np.average(utility, axis=1))
            enQe[:, :, e] = enQ
            dataQe[:, :, e] = dataQ
            # 只使用一个流队列
            virtualQe[:, :, e] = virtualQ
            print("e = ",epsilons[e],"w =", weight, "aveUtility =", aveUtility[w,e])
    np.savetxt('E:\\data1\\utilityCompare_kmwis.csv', aveUtility, delimiter=',')
    np.savetxt('E:\\data1\\trafficOverSlot_kmwis.csv', trafficOverSlot, delimiter=',')
    np.savetxt('E:\\data1\\numOfCA_kmwis.csv', numofCA, delimiter=',')
    np.savetxt('E:\\data1\\dataDrop_kmwis.csv', dropMe, delimiter=',')
    for w in range(len(epsilons)):
        np.savetxt("{0}_{1}.csv".format("E:\\data\\enQw_kmwis_e_", epsilons[w]), enQe[:, :, w], delimiter=',')
        np.savetxt("{0}_{1}.csv".format("E:\\data\\dataQw_kmwis_e_", epsilons[w]), dataQe[:, :, w], delimiter=',')
        np.savetxt("{0}_{1}.csv".format("E:\\data\\virtualQw_kmwis_e_", epsilons[w]), virtualQe[:, :, w], delimiter=',')
    endKMWIS = datetime.datetime.now()
    print("KMWIS finished ! Time Spent : %s " % (endKMWIS - start))
    return state, chCap

if __name__ == '__main__':
    print("Comparation begins")
    start = datetime.datetime.now()
    S, CHCAP = KMWIS()
    end  = datetime.datetime.now()
    print("\nComparation Finished! Time Spent: %s" %(end-start))
    enQ_dict1 = {"title": "Energy Queue KMWIS", "para_name": "epsilon", "xlabel": "time slots",
                 "ylabel": "Energy Queue Length"}
    dataQ_dict1 = {"title": "Data Queue KMWIS", "para_name": "epsilon", "xlabel": "time slots", "ylabel": "Data Queue Length"}
    virtualQ_dict1 = {"title": "Virtual Queue KMWIS", "para_name": "epsilon", "xlabel": "time slots",
                      "ylabel": "Data Queue Length"}
    utility_dict2 = {"title": "Utility Compare", "xlabel": "Value Of V", "ylabel": "Sum of Utility"}
    plotOverSlot(enQe[10, :, :], epsilons, enQ_dict1)
    plotOverSlot(dataQe[10, :, :], epsilons, dataQ_dict1)
    plotOverSlot(virtualQe[10, :, :], epsilons, virtualQ_dict1)
    plotUtilityOverWeights(aveUtility,epsilons,utility_dict2)







