from time import time
t=time()
s=""
l=['e', 'xpc', 'ns', 'io', 'hyy', 'fbf', 'acf', 'a', 'zeh', 'orn']
for i in xrange(1000000):
    s+=''.join(l)
print time()-t
print len(s)
