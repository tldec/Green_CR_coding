import  numpy as np
epsilons=np.array([0.6])
timeSlots=100000
# 单位 秒(s)
tau=20
# 单位 W(瓦特) 0~7dBm
P_T=0.94
# J/bit
P_H=0.069

# 最大采集速率 2-6kb/s
dataArrival_max= 5
# 单位 dBi
gain=15
# 频率 900MHz
band=9e8
# 带宽 1MHz
bandWidth = 1
# 初始电池容量百分比
initCapacityRate = 0.75
# 2~15mW
EH_max=0.2
numOfL=14
numOfN=15
numOfCH=4
#
############### mark ###########
# epsilons=np.array([0.8])
# timeSlots=5000
# tau=60
# P_T=0.94
# # J/bit
# P_H=0.069
# P_max=3.5
# dataArrival_max=10
# gain=15
# band=9e8
# bandWidth = 1
# initCapacityRate = 0.75
# EH_max=0.2
# numOfL=14
# numOfN=15
# numOfCH=4
# maxSlop = 1
# beta = 1
# noise = 1e-5
# # 覆盖半径(m)
# radius = 80
# para = P_T*gain*gain*3e16/np.power((4*np.pi*band),2)
# weights=np.array(range(200,8000,200))
# 在上述条件确定的时候，weight最大到8000时utility开始收敛
############### mark over ###########
weights=np.array(range(800,4000,200))
# weights = np.array([600])
maxSlop = 1
beta = 1
noise = 1e-5
# 覆盖半径(m)
radius = 80
para = P_T*gain*gain*3e16/np.power((4*np.pi*band),2)
