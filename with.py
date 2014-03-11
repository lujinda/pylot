class Sample():
    def __init__(self):
        pass
    def __enter__(self):
        return 'ok'
    def __exit__(self,type,value,trace):
        print 'in __exit__'
with Sample() as sample:
    print sample
    
