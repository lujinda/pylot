import threading
def Loop(sum):
    while 1:
        sum=sum*sum
        threading.Thread(target=Loop,args=(sum,)).start()


for i in range(1000):
    threading.Thread(target=Loop,args=(i,)).start()

