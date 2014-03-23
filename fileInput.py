import fileinput
import re
#for line in fileinput.input(inplace=True):
#    line=line.rstrip('\n')
#    print '%s # %2d'%(line,fileinput.lineno())
for lines in fileinput.input(inplace=False):
    print lines
