import os
import sys
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
files=filter(lambda x:x.startswith("._cj_"),os.listdir('.'))
print files
