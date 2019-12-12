import  numpy as np
epsilons=np.array([0.8])
timeSlots=5000
# 单位 秒(s)
tau=60
# 单位 W(瓦特) 0~7dBm
P_T=0.94
# J/bit
P_H=0.069
P_max=3.5
# 最大采集速率 2-6kb/s
dataArrival_max=10
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
# weights=np.array([800])
weights=np.array(range(200,800,200))
maxSlop = 1
beta = 1
noise = 1e-5
# 覆盖半径(m)
radius = 80
para = P_T*gain*gain*3e16/np.power((4*np.pi*band),2)
