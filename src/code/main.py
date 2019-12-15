# _*_coding:utf-8_*_
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
from code.greedy import greedy
from code.delalySensitive import delaySensitive
from code.randomAllocation import randomAllocation
import matplotlib.pyplot as plt
import random
import datetime
from code.plot import *

# 初始化结点能量队列
enQ = np.zeros((numOfN, timeSlots))
enQw = np.zeros((numOfN, timeSlots, len(weights)))
# 能量队列上界
enQ_max = np.zeros(len(weights))
# 初始化结点数据队列
dataQ = np.zeros_like(enQ)
dataQw = np.zeros_like(enQw)
# 数据队列上界
dataQ_max = np.zeros_like(enQ_max)
# 初始化结点虚拟队列
virtualQ = np.zeros_like(enQ)
virtualQw = np.zeros((numOfN, timeSlots, len(weights)))
# 虚拟队列上界
virtualQ_max = np.zeros_like(enQ_max)
# 初始化每个结点的网络效益
# sum_{n:N} f(h_n - d_n)
utility = np.zeros((numOfN, timeSlots))
# 平均网络效益-权重
aveUtility = np.zeros((len(weights)))
# 每个时结点之间的流量
trafficOverSlot = np.zeros((timeSlots, len(weights)))
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
state = np.zeros((numOfCH, 1, timeSlots, len(weights)))
chCap = np.zeros((numOfL, numOfCH, timeSlots, len(weights)))
# 数据丢弃上限
dropMax = np.zeros(len(epsilons))
# 记录每个时隙丢弃的数据量
dropMw = np.zeros((timeSlots, len(weights)))

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
    for e in range(len(epsilons)):
        epsilon = epsilons[e]
        dropMax[e] = max(epsilon, (dataArrival_max + chMax))
    W_1 = (chMax / P_T) * (weights * beta * maxSlop + epsilons + weights * maxSlop + chMax + 2 * dataArrival_max)
    W_2 = (1 / P_H) * (weights * maxSlop + dataArrival_max + chMax)
    for w in range(len(weights)):
        enQ_max[w] = max(W_1[w], W_2[w])
        dataQ_max[w] = weights[w] * maxSlop + 2 * dataArrival_max + chMax
    for e in range(len(epsilons)):
        epsilon = epsilons[e]
        for w in range((len(weights))):
            weight = weights[w]
            for n in range(numOfN):
                enQ[n, 0] = enQ_max[w] * initCapacityRate
            for t in range(timeSlots - 1):
                chState = np.random.choice(access, (numOfCH, 1), p)
                channelCapacity = bandWidth * (weight / 1000) * np.log2(
                    1 + P_T * (np.random.rand(numOfL, numOfCH) + 0.5) / \
                    ((distOfLink ** 2) * noise)) * chState.T
                state[:, :, t, w] = chState.reshape(state[:, :, t, w].shape)
                chCap[:, :, t, w] = channelCapacity.reshape(chCap[:, :, t, w].shape)

                enHarVec = computeEnHar(enQ, enQ_max[w], t)
                enHarM[:, t] = enHarVec.T

                dataHarVec = computeDataHar(dataQ, enQ, enQ_max[w], w, t)
                dataHarM[:, t] = dataHarVec.T
                # Edge, enQ, dataQ, virtualQ, links, chCap, batterCapacity, P_R, chState, P_max, alg, t
                caResults = channelAllocation(Edge, enQ, dataQ, virtualQ, link, channelCapacity, enQ_max[w], P_R,chState,P_max,"kmwis",t)
                dataTransVec, dataRecvVec = computeTransRecv(caResults, link, dist, channelCapacity, dataQ, t)

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
                updateEnQ(enQ, enHarVec, enConVec, enQ_max[w], t)
                updateDataQ(dataQ, dataHarVec, dataTransVec, dataRecvVec, dataDropVec, t)
                updateVirtualQ(virtualQ, dataQ, epsilon, dataTransVec, dataDropVec, chMax, t)
            aveUtility[w] = np.sum(np.average(utility, axis=1))
            enQw[:, :, w] = enQ
            dataQw[:, :, w] = dataQ
            # 只使用一个流队列
            virtualQw[:, :, w] = virtualQ
            print("w =", weight, "aveUtility =", aveUtility[w])
    np.savetxt('E:\\data\\utilityCompare_kmwis.csv', aveUtility, delimiter=',')
    np.savetxt('E:\\data\\trafficOverSlot_kmwis.csv', trafficOverSlot, delimiter=',')
    np.savetxt('E:\\data\\numOfCA_kmwis.csv', numofCA, delimiter=',')
    np.savetxt('E:\\data\\dataDrop_kmwis.csv', dropMw, delimiter=',')
    endKMWIS = datetime.datetime.now()
    print("KMWIS finished ! Time Spent : %s " % (endKMWIS - start))
    return state, chCap


if __name__ == '__main__':
    print("Comparation begins")
    start = datetime.datetime.now()
    S, CHCAP = KMWIS()
    enQw2,dataQw2,virtualQw2 = greedy(CHCAP,S)
    enQw3,dataQw3,virtualQw3 = randomAllocation(CHCAP, S)
    enQw4,dataQw4,virtualQw4 = delaySensitive(CHCAP, S)
    end  = datetime.datetime.now()
    print("\nComparation Finished! Time Spent: %s"%(end-start))
    for w in range(len(weights)):
        np.savetxt("{0}_{1}.csv".format("E:\\data\\enQw_kmwis_V_",weights[w]),enQw[:,:,w],delimiter=',')
        np.savetxt("{0}_{1}.csv".format("E:\\data\\dataQw_kmwis_V_",weights[w]),dataQw[:,:,w],delimiter=',')
        np.savetxt("{0}_{1}.csv".format("E:\\data\\virtualQw_kmwis_V_",weights[w]),virtualQw[:,:,w],delimiter=',')

        np.savetxt("{0}_{1}.csv".format("E:\\data\\enQw_greedy_V_", weights[w]), enQw2[:, :, w], delimiter=',')
        np.savetxt("{0}_{1}.csv".format("E:\\data\\dataQw_greedy_V_", weights[w]), dataQw2[:, :, w], delimiter=',')
        np.savetxt("{0}_{1}.csv".format("E:\\data\\virtualQw_greedy_V_", weights[w]), virtualQw2[:, :, w], delimiter=',')

        np.savetxt("{0}_{1}.csv".format("E:\\data\\enQw_random_V_", weights[w]), enQw3[:, :, w], delimiter=',')
        np.savetxt("{0}_{1}.csv".format("E:\\data\\dataQw_random_V_", weights[w]), dataQw3[:, :, w], delimiter=',')
        np.savetxt("{0}_{1}.csv".format("E:\\data\\virtualQw_random_V_", weights[w]), virtualQw3[:, :, w], delimiter=',')

        np.savetxt("{0}_{1}.csv".format("E:\\data\\enQw_delay_V_", weights[w]), enQw4[:, :, w], delimiter=',')
        np.savetxt("{0}_{1}.csv".format("E:\\data\\dataQw_delay_V_", weights[w]), dataQw4[:, :, w], delimiter=',')
        np.savetxt("{0}_{1}.csv".format("E:\\data\\virtualQw_delay_V_", weights[w]), virtualQw4[:, :, w], delimiter=',')

    enQ_dict1 ={"title": "Energy Queue KMWIS", "para_name": "V", "xlabel": "time slots", "ylabel": "Energy Queue Length"}
    dataQ_dict1 = {"title": "Data Queue KMWIS", "para_name": "V", "xlabel": "time slots", "ylabel": "Data Queue Length"}
    virtualQ_dict1 = {"title": "Virtual Queue KMWIS", "para_name": "V", "xlabel": "time slots", "ylabel": "Data Queue Length"}
    enQ_dict2 = {"title": "Energy Queue Greedy", "para_name": "V", "xlabel": "time slots","ylabel": "Energy Queue Length"}
    dataQ_dict2 = {"title": "Data Queue Greedy", "para_name": "V", "xlabel": "time slots", "ylabel": "Data Queue Length"}
    virtualQ_dict2 = {"title": "Virtual Queue Greedy", "para_name": "V", "xlabel": "time slots", "ylabel": "Data Queue Length"}
    utility_dict = {"title": "Utility-V", "para_name": "", "xlabel": "Value Of V", "ylabel": "Sum of Utility"}
    utility_dict2 = {"title": "Utility Compare", "xlabel": "Value Of V", "ylabel": "Sum of Utility"}
    aveU = np.loadtxt('E:\\data\\utilityCompare_kmwis.csv', delimiter=',')
    aveU1 = np.loadtxt('E:\\data\\utilityCompare_random.csv', delimiter=',')
    aveU2 = np.loadtxt('E:\\data\\utilityCompare_delay.csv', delimiter=',')
    aveU3 = np.loadtxt('E:\\data\\utilityCompare_greedy.csv', delimiter=',')
    diff = ["K-MWIS","Random","Delay-Sensitive","Greedy",]
    # print(enQw[10, :, :].shape)
    plotOverSlot(enQw[10, :, :], weights, enQ_dict1)
    plotOverSlot(dataQw[10, :, :], weights, dataQ_dict1)
    plotOverSlot(virtualQw[10, :, :], weights, virtualQ_dict1)

    plotOverSlot(enQw2[10, :, :], weights, enQ_dict2)
    plotOverSlot(dataQw2[10, :, :], weights, dataQ_dict2)
    plotOverSlot(virtualQw2[10, :, :], weights, virtualQ_dict2)
    U = np.zeros((len(weights),4))
    U[:,0] = aveU
    U[:,1] = aveU1
    U[:,2] = aveU2
    U[:,3] = aveU3
    plotUtilityOverWeights(U, diff, utility_dict2)
