class Print():
    def __init__(self,value):
        self.value=value
    def __call__(self,other):
        return self.value*other
p=Print(10) # __init__
print Print(10) # __call__
