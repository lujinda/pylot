#coding:utf8
def search(lower=0,upper=1000):
    middle=(lower+upper)//2
    if lower==upper:#when the lower equals upper,the return results
        return upper
    q=raw_input('请问您心中的数大于%d吗？'%middle)
    
    if q.startswith('y'):
        return search(middle+1,upper)#if NUM>middle,then lower=middle,upper=upper
    else:
        return search(lower,middle)#if NUM<=middle then upper=middle,lower=lower
print '我猜您心里的数肯定是:%d' %search()
