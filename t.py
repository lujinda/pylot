import fileinput
for line in fileinput.input():
    line=line.rstrip('\n')
    print '%s # %2d'%(line,fileinput.lineno())
