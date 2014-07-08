#coding:utf8
import cv2
from cv2 import cv
import sys

haar_face="/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml"
haar_mouth="/usr/share/opencv/haarcascades/haarcascade_mcs_mouth.xml"
c_f=cv.Load(haar_face)
c_m=cv.Load(haar_mouth)

def ifFace(img,size):
    gray=cv.CreateImage(size,8,1)
    cv.CvtColor(img,gray,cv.CV_BGR2GRAY)
    newMem=cv.CreateMemStorage(0)
    cv.EqualizeHist(gray,gray)
    face=cv.HaarDetectObjects(gray,c_f,newMem,1.2,3,cv.CV_HAAR_DO_CANNY_PRUNING,(50,50))
    mouth=cv.HaarDetectObjects(gray,c_m,newMem,1.2,2,cv.CV_HAAR_DO_CANNY_PRUNING,(0,0))
    if face and mouth:
        print "有脸"
        cv.SaveImage("img/out.jpg",img)
        sys.exit(0)


capture=cv.CaptureFromFile(sys.argv[1])
width=cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH)
height=cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT)
size=(int(width),int(height))
fps=30
i=0

while True:
    img=cv.QueryFrame(capture)
    if not img:break
    if int((i+1)%fps)==0:
 #       cv.SaveImage("img/%s.jpeg"%i,img)
        ifFace(img,size)
    i+=1

