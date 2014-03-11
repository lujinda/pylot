from PIL import Image
import sys
import os
try:
	name=sys.argv[1]
	x=int(sys.argv[2])
	y=int(sys.argv[3])
	def reSize(filename,x,y):
		try:
			img = Image.open(filename)
			img=img.resize((x,y),1)
			img.save(os.path.basename(filename))
			return 0
		except Exception,e:
			print "Exception:%s" %(e)
			return 1
		
	def dreSize(name,x,y):
		try:
			dir=os.listdir(name)
			for i in dir:
				fileName=name + '/'  + i
				if os.path.isfile(fileName):
					if reSize(fileName,x,y) == 1:
						print fileName + ' ---resize error'
		except Exception,e:
			print "Exception:%s" %(e)
	if os.path.isfile(name):
		if reSize(name,x,y) == 1:
			print name + ' ---resize error'
	elif os.path.isdir(name):
		dreSize(name,x,y)
	else:
		print 'error file type'
except Exception,e:
	print "Exception:%s" %(e)
finally:
	sys.exit()
