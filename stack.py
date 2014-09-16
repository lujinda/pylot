class Stack:
    def __init__(self,size=0):
        self.__stack=[]
        self.size=size
        self.top=-1

    def isEmpty(self):
        if self.top == -1:
            return True
        return False

    def isFull(self):
        if self.top == self.size:
            return True
        return False

    def push(self,obj):
        if self.size!=0 and self.isFull():
            raise Exception("Stack is Full")
        else:
            self.__stack.append(obj)
            self.top+=1

    def pop(self):
        if self.isEmpty():
            raise Exception("Stack is Empty")
        else:
            self.top-=1
            return self.__stack.pop()

    def getSize(self):
        return self.top+1

    def setSize(self,size):
        self.size=size

    def show(self):
        print self.__stack


