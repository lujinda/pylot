#coding:utf8
import cv2
from cv2 import cv
import sys
import time

haar_face="/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml"
haar_mouth="/usr/share/opencv/haarcascades/haarcascade_mcs_mouth.xml"
haar_body="/usr/share/opencv/haarcascades/haarcascade_upperbody.xml"
c_f=cv.Load(haar_face)
c_m=cv.Load(haar_mouth)
c_b=cv.Load(haar_body)

count=0

def parseVedio(_,fd,filename):

    def ifFace(img,size):
        global count
        gray=cv.CreateImage(size,8,1)
        cv.CvtColor(img,gray,cv.CV_BGR2GRAY)
        newMem1=cv.CreateMemStorage(0)
        newMem2=cv.CreateMemStorage(0)
        newMem3=cv.CreateMemStorage(0)
        cv.EqualizeHist(gray,gray)
        face=cv.HaarDetectObjects(gray,c_f,newMem1,1.2,3,cv.CV_HAAR_DO_CANNY_PRUNING,(50,50))
        mouth=cv.HaarDetectObjects(gray,c_m,newMem2,1.2,2,cv.CV_HAAR_DO_CANNY_PRUNING,(10,10))
        body=cv.HaarDetectObjects(gray,c_m,newMem3,1.2,2,cv.CV_HAAR_DO_CANNY_PRUNING,(200,200))
        if face and mouth or body:
            count+=1
            if count >=5:
                cv.SaveImage(imgpath,img)
                return True
        return False

    capture=cv.CaptureFromFile(filename)
    width=cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH)
    height=cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT)
    size=(int(width),int(height))
    fps=30
    i=0

    while True:
        img=cv.QueryFrame(capture)
        if not img:break
        if int((i+1)%fps)==0:
            if ifFace(img,size):
                mess="%s:有脸"%filename
                imgname=time.strftime("%Y%M%d%H%m%s")+str(i)+'jpg'
                imgpath="img/%s"%imgname
                fd.write(mess+'\n')
                fd.flush()
                print mess
                return None
        i+=1
    mess="%s:无脸"%filename
    fd.write(mess+'\n')
    fd.flush()
    print mess

