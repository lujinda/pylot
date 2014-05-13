import sys
import fileinput
def grep(line,searchtext):
    if searchtext in line:
        print line,

if __name__=="__main__":
    fd=open(sys.argv[1],"r");
    searchtext=sys.argv[2]
    for line in fd.readlines():
        grep(line,searchtext)
        

