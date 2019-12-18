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
trafficOverSlotE = np.zeros((len(weights),len(epsilons)))
harMw =  np.zeros((len(weights),len(epsilons)))
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
            print("e = ",epsilons[e],"w =", weight, "aveUtility =", aveUtility[w,e])
        dropMw[w,e] = np.average(np.average(dataDropM[1:,:],axis=0))
        harMw[w,e] = np.average(np.average(dataHarM[1:,:],axis=0))
        trafficOverSlotE[w,e] = np.average(trafficOverSlot[:,0])
    np.savetxt("{0}{1}.csv".format(fpath,"utilityCompare"), aveUtility, delimiter=',')
    np.savetxt("{0}{1}.csv".format(fpath,"trafficOverSlot"), trafficOverSlotE, delimiter=',')
    np.savetxt("{0}{1}.csv".format(fpath,"dataHar"), harMw, delimiter=',')
    np.savetxt("{0}{1}.csv".format(fpath,"dataDrop"), dropMw, delimiter=',')
    endKMWIS = datetime.datetime.now()
    print("KMWIS finished ! Time Spent : %s " % (endKMWIS - start))
    return state, chCap

def compareEpsilon():
    print("Comparation begins")
    start = datetime.datetime.now()
    S, CHCAP = KMWIS()
    end = datetime.datetime.now()
    enQ_dict1 = {"title": "Energy Queue KMWIS", "para_name": "epsilon", "xlabel": "time slots",
                 "ylabel": "Energy Queue Length"}
    dataQ_dict1 = {"title": "Data Queue KMWIS", "para_name": "epsilon", "xlabel": "time slots", "ylabel": "Data Queue Length"}
    virtualQ_dict1 = {"title": "Virtual Queue KMWIS", "para_name": "epsilon", "xlabel": "time slots",
                      "ylabel": "Data Queue Length"}
    enQ_dict2 = {"title": "Energy Queue KMWIS", "para_name": "V", "xlabel": "time slots",
                 "ylabel": "Energy Queue Length"}
    dataQ_dict2 = {"title": "Data Queue KMWIS", "para_name": "V", "xlabel": "time slots", "ylabel": "Data Queue Length"}
    virtualQ_dict2 = {"title": "Virtual Queue KMWIS", "para_name": "V", "xlabel": "time slots",
                      "ylabel": "Data Queue Length"}
    enQ_dict1 = {"title": "Energy Queue KMWIS", "para_name": "V", "xlabel": "time slots",
                 "ylabel": "Energy Queue Length", "fname": "E:\\eQ_1.png"}
    dataQ_dict1 = {"title": "Data Queue KMWIS", "para_name": "V", "xlabel": "time slots", "ylabel": "Data Queue Length",
                   "fname": "E:\\dQ_1.png"}
    virtualQ_dict1 = {"title": "Virtual Queue KMWIS", "para_name": "V", "xlabel": "time slots",
                      "ylabel": "Data Queue Length", "fname": "E:\\vQ_1.png"}
    enQ_dict2 = {"title": "Energy Queue Greedy", "para_name": "V", "xlabel": "time slots",
                 "ylabel": "Energy Queue Length", "fname": "E:\\eQ_2.png"}
    dataQ_dict2 = {"title": "Data Queue Greedy", "para_name": "V", "xlabel": "time slots",
                   "ylabel": "Data Queue Length", "fname": "E:\\dQ_2.png"}
    virtualQ_dict2 = {"title": "Virtual Queue Greedy", "para_name": "V", "xlabel": "time slots",
                      "ylabel": "Data Queue Length", "fname": "E:\\VQ_2.png"}
    # utility_dict = {"title": "Utility-V", "para_name": "", "xlabel": "Value Of V", "ylabel": "Sum of Utility",
    #                 "fname": "E:\\Utility_V.png"}
    utility_dict2 = {"title": "Utility Compare", "xlabel": "Value Of epsilon",
                     "ylabel": "Sum of Utility"}
    # idx = int(len(weights)/2)
    # idx2 = int(len(epsilons)/2)
    # print(enQw[10, :,idx, :].shape)
    # plotOverSlot(timeSlots,enQw[10, :,idx, :], epsilons, enQ_dict1)
    # plotOverSlot(timeSlots,dataQw[10, :,idx, :], epsilons, dataQ_dict1)
    # plotOverSlot(timeSlots,virtualQw[10, :,idx, :], epsilons, virtualQ_dict1)
    # plotOverSlot(timeSlots,enQw[10, :,:,idx2 ], weights, enQ_dict2)
    # plotOverSlot(timeSlots,dataQw[10, :, :, idx2], weights, dataQ_dict2)
    har_epsilon_dict = {"xlabel":"time slots","ylabel":"Average Data Harvested","title":"Average Data Harvested Comparation under Epsilons"
                        }
    drop_epsilon_dict = {"xlabel": "time slots", "ylabel": "Average Data Dropped",
                        "title": "Average Data Dropping Comparation under Epsilons"
        }
    traffic_epsilon_dict = {"xlabel": "time slots", "ylabel": "Average Data Transmitted",
                         "title": "Average Data Transmitting Comparation under Epsilons"
       }
    print("\nComparation Finished! Time Spent: %s" % (end - start))
    plotUtilityOverWeights(epsilons,harMw, weights, har_epsilon_dict)
    plotUtilityOverWeights(epsilons,dropMw, weights, drop_epsilon_dict)
    plotUtilityOverWeights(epsilons,trafficOverSlotE, weights, traffic_epsilon_dict)
    plotUtilityOverWeights(epsilons,aveUtility, weights, utility_dict2)
def compareAlg():
    print("Comparation begins")
    start = datetime.datetime.now()
    S, CHCAP = KMWIS()
    enQw2, dataQw2, virtualQw2 = greedy(CHCAP, S)
    enQw3, dataQw3, virtualQw3 = randomAllocation(CHCAP, S)
    enQw4, dataQw4, virtualQw4 = delaySensitive(CHCAP, S)
    end = datetime.datetime.now()
    print("\nComparation Finished! Time Spent: %s" % (end - start))
    for w in range(len(weights)):
        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath,"enQw", "kmwis",weights[w]), enQw[:, :, w], delimiter=',')
        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath,"dataQw", "kmwis",weights[w]), dataQw[:, :, w], delimiter=',')
        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath,"virtualQw", "kmwis",weights[w]), virtualQw[:, :, w], delimiter=',')

        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath, "enQw", "greedy", weights[w]), enQw2[:, :, w], delimiter=',')
        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath, "dataQw", "greedy", weights[w]), dataQw2[:, :, w], delimiter=',')
        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath, "virtualQw", "greedy", weights[w]), virtualQw2[:, :, w],
                   delimiter=',')

        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath, "enQw", "random", weights[w]), enQw3[:, :, w], delimiter=',')
        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath, "dataQw", "random", weights[w]), dataQw3[:, :, w],
                   delimiter=',')
        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath, "virtualQw", "random", weights[w]), virtualQw3[:, :, w],
                   delimiter=',')
        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath, "enQw", "delay", weights[w]), enQw4[:, :, w], delimiter=',')
        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath, "dataQw", "delay", weights[w]), dataQw4[:, :, w],
                   delimiter=',')
        np.savetxt("{0}{1}_{2}_V_{3}.csv".format(fpath, "virtualQw", "delay", weights[w]), virtualQw4[:, :, w],
                   delimiter=',')

    enQ_dict1 = {"title": "Energy Queue KMWIS", "para_name": "V", "xlabel": "time slots",
                 "ylabel": "Energy Queue Length","fname":"E:\\eQ_1.png"}
    dataQ_dict1 = {"title": "Data Queue KMWIS", "para_name": "V", "xlabel": "time slots", "ylabel": "Data Queue Length","fname":"E:\\dQ_1.png"}
    virtualQ_dict1 = {"title": "Virtual Queue KMWIS", "para_name": "V", "xlabel": "time slots",
                      "ylabel": "Data Queue Length","fname":"E:\\vQ_1.png"}
    enQ_dict2 = {"title": "Energy Queue Greedy", "para_name": "V", "xlabel": "time slots",
                 "ylabel": "Energy Queue Length","fname":"E:\\eQ_2.png"}
    dataQ_dict2 = {"title": "Data Queue Greedy", "para_name": "V", "xlabel": "time slots",
                   "ylabel": "Data Queue Length","fname":"E:\\dQ_2.png"}
    virtualQ_dict2 = {"title": "Virtual Queue Greedy", "para_name": "V", "xlabel": "time slots",
                      "ylabel": "Data Queue Length","fname":"E:\\VQ_2.png"}
    utility_dict = {"title": "Utility-V", "para_name": "", "xlabel": "Value Of V", "ylabel": "Sum of Utility","fname":"E:\\Utility_V.png"}
    utility_dict2 = {"title": "Utility Compare", "para_name": "epsilon","xlabel": "Value Of V", "ylabel": "Sum of Utility","fname":"E:\\Utility_V.png"}
    diff = ["K-MWIS", "Random", "Delay-Sensitive", "Greedy", ]
    # print(enQw[10, :, :].shape)
    plotOverSlot(enQw[10, :, :], weights, enQ_dict1)
    plotOverSlot(dataQw[10, :, :], weights, dataQ_dict1)
    plotOverSlot(virtualQw[10, :, :], weights, virtualQ_dict1)

    plotOverSlot(enQw2[10, :, :], weights, enQ_dict2)
    plotOverSlot(dataQw2[10, :, :], weights, dataQ_dict2)
    plotOverSlot(virtualQw2[10, :, :], weights, virtualQ_dict2)
    U = np.zeros((len(weights), 4))
    plotUtilityOverWeights(U, diff, utility_dict2)

if __name__ == '__main__':
    # compareAlg()
    compareEpsilon()

