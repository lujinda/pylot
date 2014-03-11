import os,sys
def pname(name,n=2):
	for i in range(n):
		print ' ',
	print '%s'%(name)
os.chdir(sys.argv[1])
print sys.argv[1]
for i in os.listdir(sys.argv[1]):
	if os.path.isdir(i):
		pname(i + '/')
	else:
		pname(i)
