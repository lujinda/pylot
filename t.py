#coding:utf8

fd=open("t.t","r")
lines=fd.readlines()
for i in range(len(lines)):
    if i%2==0:
        print "%-70s" %lines[i][:-1],
    else:
        print "%-s" %lines[i][:-1],
    if (i+1)%2==0:
        print
    
