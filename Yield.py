class Data(object):
    def __init__(self,*args):
        self._data=list(args)
    def __iter__(self):
        for x in self._data:
            yield x

d=Data(1,3,5,6)
for x in d:
    print x
