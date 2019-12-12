import  numpy as np
epsilons=np.array([0.6])
timeSlots=20000
# 单位 秒(s)
tau=20
# 单位 W(瓦特) 0~7dBm
P_T=0.5
# J/bit
P_H=1.2
P_max=2.5
# 最大采集速率 2-6kb/s
dataArrival_max=2
# 单位 dBi
gain=15
# 频率 900MHz
band=9e8
# 带宽 1MHz
bandWidth = 1e6
# 2~15mW
EH_max=0.5
numOfL=14
numOfN=15
numOfCH=4
weights=np.array([100,200,300,400,500,600,700,800,900,1000])
maxSlop = 1
beta = 1
noise = 1e-5
# 覆盖半径(m)
radius = 60
para = P_T*gain*gain*3e16/np.power((4*np.pi*band),2)
