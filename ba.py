#coding:utf8
"""
    state 是一个tuple里面存放的是之前已经排好的一个位置，比如state[0]如果为1则表示为第0号行的第1号列
"""
def isOk(state,nextX):
    nextY=len(state) # Y，也就是行号是可以确定的
    if nextX in state:return True # 如果要判断的x，也就是列号，已经存在于state元组中的，则直接返回True
    for i in range(nextY): # 对已经存在的皇后位置做一个遍历
        if abs(state[i]-nextX) == nextY-i: # 如果行号为i的皇后的列号-将要放的皇后的列号==将要放在皇后的行号-行号为i的皇号的行号，也就是i,，则表示它们是处于对角线的(正方形的长宽相同)
            return True
    return False

def queens(num=8,state=()):
    for pos in range(num):  # 对每行的每格都进行遍历
        if not isOk(state,pos): # 如果当前这格与以前的皇后的位置都没有冲突的话
            if len(state)==num-1: # 如果当前是最后一行的时候
                print "last yield qian",pos 
                yield (pos,) # 当前的列以元组的形式yield给前一个调用的
                print "last yield hou",pos
            else:
                for result in queens(num,state+(pos,)):
                    print "yield qian",pos
                    yield (pos,)+result # 把这个元组（自己的元组+下一个函数返回的值） 类似于这样的情况 1+(2+(3+(4+(....))))
                    print "yield hou",pos
                    # 如果有多个结果的话，在完成了一次后，第二次，会从上一行开始执行，这时候的state是没有值的，是最外层的那个函数,然后再一层一层进去,最后一次会显示print "last yield hou",pos，但是它并不是最后一条执行的，最后一条应该是最外层queens函数的yield语句

def printident(data,num):
    for line in data:
            print "%s%s%s" %('* '*line,"Q ","* "*(num-1-line))

if __name__=="__main__":
    import random
    printident(random.choice(list(queens(8))),8)
