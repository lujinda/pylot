class Queue:
    def __init__(self,size=0):
        self.size=size
        self.top=-1
        self.__queue=[]

    def setSize(self,size):
        self.size=size

    def getSize(self):
        return self.top+1

    def isFull(self):
        if self.size!=0 and self.top+1 == self.size:
            return True
        return False

    def isEmpty(self):
        if self.top==-1:
            return True
        return False

    def add(self,obj):
        if self.isFull():
            raise Exception("Queue is full")
        else:
            self.__queue.append(obj)
            self.top+=1

    def get(self):
        if self.isEmpty():
            raise Exception("Queue is emply")
        else:
            self.top-=1
            return self.__queue.pop(0)

    def show(self):
        print self.__queue

