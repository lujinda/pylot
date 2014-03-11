import time
import heapq
import copy
t=time.time()
data=[292, 63, 207, 736, 267, 669, 635, 252, 196, 0, 622, 244, 275, 817, 828, 466, 933, 169, 962, 205]
heapq.heapify(data)

for i in range(1000000):
    Min=heapq.heappop(copy.copy(data))
print Min
print time.time()-t
