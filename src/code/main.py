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
from code.greedy import greedy
from code.delalySensitive import delaySensitive
from code.randomAllocation import randomAllocation
import matplotlib.pyplot as plt
import random
import datetime
from code.plot import *

algList = ["K-MWIS", "Random", "Delay-Sensitive", "Greedy"]
# 初始化结点能量队列
enQ = np.zeros((numOfN, timeSlots))
enQw = np.zeros((numOfN, timeSlots, len(weights),len(epsilons)))
# 能量队列上界
enQ_max = np.zeros(len(weights))
# 初始化结点数据队列
dataQ = np.zeros_like(enQ)
dataQw = np.zeros_like(enQw)
# 数据队列上界
dataQ_max = np.zeros_like(enQ_max)
# 初始化结点虚拟队列
virtualQ = np.zeros_like(enQ)
virtualQw = np.zeros_like(enQw)
# 虚拟队列上界
virtualQ_max = np.zeros_like(enQ_max)
# 初始化每个结点的网络效益
# sum_{n:N} f(h_n - d_n)
# 不同算法的网络效益
U = np.zeros((len(weights),len(algList)))
utility = np.zeros((numOfN, timeSlots))
# 平均网络效益-权重
aveUtility = np.zeros((len(weights),len(epsilons)))
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
# 最大信道容量
chMax = bandWidth * np.log2(1 + P_T * 1.5) / ((minDist ** 2) * noise) / 1000
# 数据丢弃上限
dropMax = dataArrival_max + chMax
# 记录每个时隙丢弃的数据量
dropMw = np.zeros((len(weights),len(epsilons)))
# 不同算法下IoT 结点平均丢弃数据
D = np.zeros((len(weights),len(algList)))
trafficOverSlotE = np.zeros((len(weights),len(epsilons)))
# 不同算法下IoT 结点平均发送数据
T = np.zeros((len(weights),len(algList)))
harMw =  np.zeros((len(weights),len(epsilons)))
# 不同算法下IoT 结点平均采集数据
H = np.zeros((len(weights),len(algList)))
# 信道可接入概率
# 主用户信道状态集 0 表示不可用 1 表示可用
access = [0, 1]
# 主用户可接入概率
p = [0.4, 0.6]
P_R = para / distOfLink
maxPR = np.max(P_R)
# 最大能耗
P_max = max(P_T * tau * 0.3, maxPR * tau * 0.3) + P_H * dataArrival_max

def KMWIS():
    start = datetime.datetime.now()
    print("KMWIS begins")
    # print("chMax", chMax)
    for e in range(len(epsilons)):
        epsilon = epsilons[e]
        W_1 = (chMax / P_T) * (weights * beta * maxSlop + epsilon + weights * maxSlop + chMax + 2 * dataArrival_max)
        W_2 = (1 / P_H) * (weights * maxSlop + dataArrival_max + chMax)
        epsilon = epsilons[e]
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
                state[:, :, t, w] = chState.reshape(state[:, :, t, w].shape)
                chCap[:, :, t, w] = channelCapacity.reshape(chCap[:, :, t, w].shape)

                enHarVec = computeEnHar(enQ, enQ_max[w], t)
                enHarM[:, t] = enHarVec.T

                dataHarVec = computeDataHar(dataQ, enQ, enQ_max[w], w, t)
                dataHarM[:, t] = dataHarVec.T
                # harMw[e] = np.sum(dataHarVec)

                # Edge, enQ, dataQ, virtualQ, links, chCap, batterCapacity, P_R, chState, P_max, alg, t
                caResults = channelAllocation(Edge, enQ, dataQ, virtualQ, link, channelCapacity, enQ_max[w], P_R,chState,P_max,"kmwis",t)
                dataTransVec, dataRecvVec = computeTransRecv(caResults, link, dist, channelCapacity, dataQ, t)
                trafficOverSlot[t,w] = np.average(dataTransVec)
                dataDropVec = computeDrop(virtualQ, dataQ, dataTransVec, weight, dropMax, t)
                dataDropM[:, t] = dataDropVec.T
                # dropMw[t,w,e] = np.sum(dataDropVec)
                enConVec = computeEnConsumption(caResults, link, distOfLink, dataHarVec)
                for n in range(numOfN):
                    if n != 0:
                        tmp = dataHarVec[n] - dataDropVec[n] + 1
                        # if tmp < 0:
                        #     utility[n, t] = 0
                        # else:
                        #     if np.log(tmp) < 0:
                        #         utility[n, t] = 0
                        #     else:
                        #         utility[n, t] = np.log(tmp)
                        if tmp < 0:
                            utility[n, t] = 0
                        else:
                            # if np.log(tmp) < 0:
                            #     utility[n, t] = 0
                            # else:
                            utility[n, t] = np.log(tmp)
                    else:
                        utility[0, t] = 0
                updateEnQ(enQ, enHarVec, enConVec, enQ_max[w], t)
                updateDataQ(dataQ, dataHarVec, dataTransVec, dataRecvVec, dataDropVec, t)
                updateVirtualQ(virtualQ, dataQ, epsilon, dataTransVec, dataDropVec, chMax, t)
            aveUtility[w,e] = np.sum(np.average(utility[1:,:], axis=1))
            enQw[:, :, w,e] = enQ
            dataQw[:, :,w, e] = dataQ
            # 只使用一个流队列
            virtualQw[:, :,w,e] = virtualQ
            # np.savetxt("{0}{1}_V_{2}_e_{3}.csv".format(fpath,"enQ",weights[w],epsilons[e]),
            #            enQ, delimiter=',')
            # np.savetxt("{0}{1}_V_{2}_e_{3}.csv".format(fpath, "dataQ", weights[w], epsilons[e]),
            #            enQ, delimiter=',')
            # np.savetxt("{0}{1}_V_{2}_e_{3}.csv".format(fpath,  "virtualQ", weights[w], epsilons[e]),
            #            enQ, delimiter=',')
            print("w =", weight, "aveUtility =", aveUtility[w,e])
        dropMw[w,e] = np.average(np.average(dataDropM[1:,:],axis=0))
        harMw[w,e] = np.average(np.average(dataHarM[1:,:],axis=0))
        trafficOverSlotE[w,e] = np.average(trafficOverSlot[:,0])
    np.savetxt("{0}{1}.csv".format(fpath,"utilityCompare_kmwis"), aveUtility, delimiter=',')
    np.savetxt("{0}{1}.csv".format(fpath,"trafficOverSlot_kmwis"), trafficOverSlotE, delimiter=',')
    np.savetxt("{0}{1}.csv".format(fpath,"dataHar_kmwis"), harMw, delimiter=',')
    np.savetxt("{0}{1}.csv".format(fpath,"dataDrop_kmwis"), dropMw, delimiter=',')
    endKMWIS = datetime.datetime.now()
    print("KMWIS finished ! Time Spent : %s " % (endKMWIS - start))
    return state, chCap
def compareAlg():
    print("Comparation begins")
    start = datetime.datetime.now()
    S, CHCAP = KMWIS()
    H = np.zeros_like(U)
    T = np.zeros_like(U)
    D = np.zeros_like(U)
    for w in range(len(weights)):
       U[w,0] =  aveUtility[w, 0]
       D[w,0] =  dropMw[w, 0]
       T[w,0] =  trafficOverSlotE[w, 0]
       H[w,0] =  harMw[w, 0]

    randomAllocation(CHCAP, S,U,T,H,D)
    delaySensitive(CHCAP, S,U,T,H,D)
    greedy(CHCAP, S,U,T,H,D)
    end = datetime.datetime.now()
    print("\nComparation Finished! Time Spent: %s" % (end - start))

    print("Network Utility")
    utility_dict = {}
    utility_dict['title'] = "Network Utility Comparation under Different Algrithm"
    utility_dict['xlabel'] = "Value Of V"
    utility_dict['ylabel'] = "Network Utility"
    plotUtilityOverWeights(weights,U, algList, utility_dict)
    print("Data Harvested")
    har_dict = {}
    drop_dict = {}
    traff_dict = {}
    har_dict["xlabel"] = "Value of V"
    har_dict["ylabel"] = "Average Data Harvested of IoT Nodes"
    har_dict["title"] = "Average Data Harvested By IoT Nodes under Different Algrithm "
    plotUtilityOverWeights(weights, H, algList, har_dict)
    print("Average Data-drops of IoT Nodes ")
    drop_dict["xlabel"] = "Value of Epsilons"
    drop_dict["ylabel"] = "Average Data-drops of IoT Nodes "
    drop_dict["title"] = "Dropped Data By IoT Nodes under Different Algrithm"
    plotUtilityOverWeights(weights, D, algList, drop_dict)
    print("Average Traffics")
    traff_dict["xlabel"] = "Value of Epsilons"
    traff_dict["ylabel"] = "Average Traffics of IoT Nodes"
    traff_dict["title"] = "Average Transmitted Data By IoT Nodes under Different Algrithm"
    plotUtilityOverWeights(weights, T, algList, traff_dict)

def compareWeights():
    print("Comparation begins")
    start = datetime.datetime.now()
    KMWIS()
    utility_dict = {}
    utility_dict["xlabel"] = "Value of Weights"
    utility_dict["ylabel"] = "Network Utility"
    utility_dict["title"] = "Network Utility under Different Weights"
    utility_dict["para_name"] = "V"
    plotUtilityOverWeights(weights, aveUtility, epsilons, utility_dict)
    end = datetime.datetime.now()
    print("\nComparation Finished! Time Spent: %s" % (end - start))
if __name__ == '__main__':
    compareAlg()

