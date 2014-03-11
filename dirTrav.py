import os,sys
dirName=sys.argv[1]
for root,dirs,files in os.walk(dirName):
	print root
	for name in files:
		print os.path.join(root,name)
