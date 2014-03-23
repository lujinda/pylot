class Sample():
    def __init__(self):
        print 'in __init__'
        pass
    def __enter__(self):
        return 'ok'
    def __exit__(self,type,value,trace):
        print 'in __exit__'
with Sample() as sample:
    print sample
    
