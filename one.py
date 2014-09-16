#coding:utf8
def countOne(n):
    divisor=1 # 主要来判断现在处于哪一位上。1是个位，10十位，类推
    count=0 
    while (n/divisor > 0):
        head=n/(divisor*10) # 取出头部（去低位），比如1234，刚开始是123 ，接下来是12,1,0
        pos=(n/divisor)%10 # 取出当位所在位的数字，比如1234，则是4,3,2,1
        if pos>=2:
            count+=(head+1)*divisor # 在个位数，计算的是个位上出现的1次数,类推
        elif pos==0:
            count+=head*divisor # 如果当前位是0，则当可以少算一次

        elif pos==1:
            t=(n%(divisor*10))-divisor #如果当前位是1,算出当前位与divisor的差值，再把它当pos=0算
            count+=head*divisor+t+1  # 因为到9就行了，0不是，所以要在计算差值的时候是多减了一个的，在这里补回去

        divisor*=10 # 移位

    return count

print countOne(11111111111)
