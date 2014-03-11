#!/usr/bin/env python
#coding:utf8
import random
def showRandom(obje,number,l):
    result=[]
    for i in range(0,number):
        s=""
        if not obje:
            s=int(random.random()*(10**l))
            
        elif len(obje)<27:
            for i in range(0,int(random.random()*l+1)):
                s+=str(random.choice(obje))
        else:
            l=int(random.random()*10+1)
            while len(s)<l:
                rand=int(random.random()*l/3+1)
                for i in range(0,rand):
                    s+=str(random.choice(obje[:10]))
                for i in range(0,int(random.random()*(l-rand))):
                    s+=random.choice(obje[10:])
                if l<len(s):s=s[:l]
        result.append(s)
    return result
    #print result
    
num=range(0,10)
letter=[chr(x) for x in range(97,123)]
print ('1.Generate a list of all-digital\n2.Generate a list of the full letter\n3.Generate a list of numbers and letters\n4.Generate a list of all-digtal(type:int)')
swit={'1':num,'2':letter,'3':num+letter,'4':None}
while True:
    index=raw_input('Please select the type of:')
    number=int(raw_input('Number of elements:'))
    l=int(raw_input('Length of each element:'))
    if index in swit and l >0 and number >0:
        break
    else:
        print 'Input error,please re-enter~~'
print showRandom(swit[index],number,l)
