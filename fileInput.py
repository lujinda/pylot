import fileinput
import random
#for line in fileinput.input(inplace=True):
#    line=line.rstrip('\n')
#    print '%s # %2d'%(line,fileinput.lineno())
words=list(fileinput.input())
print random.choice(words),
