from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
import os

class render():
    def __init__(self,path):
        self.templates={}
        self.path=path
        for filename,filepath in self.filter_file(path):
            self.templates[filename]=filepath
            self.add_func(filename)

    def filter_file(self,path):
        import re
        filelists=[]
        re_filename=re.compile(r"(.+)\.html?")
        for filename in os.listdir(path):
            filepath=os.path.join(path,filename)
            if os.path.isfile(filepath) and re_filename.search(filename):
                filelists.append((re_filename.findall(filename)[0],filepath)) 
        return filelists 

    def render_temp(self,filename):
        path=self.templates[filename]
        return open(path,'r').read()
            
    def add_func(self,filename):
        import functools
        self.__dict__[filename]=functools.partial(self.render_temp,filename=filename)
        



