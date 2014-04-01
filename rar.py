from rarfile import RarFile
from rarfile import BadRarFile
from rarfile import PasswordRequired
rar=RarFile("/home/ljd/1.rar")
filename=rar.namelist()[0]
for x in xrange(100000):
    try:
        rar.setpassword(str(x))
        rar.read(filename)
        print x   
        exit()
    except BadRarFile,PasswordRequired:
        pass
    
