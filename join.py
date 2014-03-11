from time import time
t=time()
s=""
l=['e', 'xpc', 'ns', 'io', 'hyy', 'fbf', 'acf', 'a', 'zeh', 'orn']
for i in range(1000000):
    s+=''.join([x for x in l])
#    for k in l:
#        s+=k
print time()-t
print len(s)
