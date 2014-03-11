import profile

def profileTest():
    sum=0
    for i in xrange(1,10000000):
        sum+=i
if __name__=='__main__':
    profile.run('profileTest()')
    
