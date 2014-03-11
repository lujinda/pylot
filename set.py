from time import time
t=time()
listA=[1,2,3,4,5,6,7,8,34,54]
listB=[2,4,6,9,23]
intersection=[]
for i in xrange(1000000):
    intersection=list(set(listA)&set(listB))
print time()-t
print intersection

