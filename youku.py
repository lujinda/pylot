#coding:utf8
from BeautifulSoup import BeautifulSoup as bs
import sys
import urllib2 
from twisted.internet.defer import inlineCallbacks 
from twisted.internet import defer,reactor 
from twisted.web.client import getPage,downloadPage
import cv2
from cv2 import cv
import sys

yesfd=open('yesout.txt','w+')
nofd=open('noout.txt','w+')
errfd=open('errout.txt','w+')



haar_face="/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml"
haar_mouth="/usr/share/opencv/haarcascades/haarcascade_mcs_mouth.xml"
haar_body="/usr/share/opencv/haarcascades/haarcascade_upperbody.xml"
c_f=cv.Load(haar_face)
c_m=cv.Load(haar_mouth)
c_b=cv.Load(haar_body)


def parse_error(_,Id,name):
    print Id,name,"解析出错喽"
    print _
    errfd.write("%s %s\n"%(Id,name))
    errfd.flush()
    

def parse_finished(_):
    print "视频均分析完成"
    fd.close()
    reactor.stop()
    

def readUrl():
    fd=open("list.txt")
    url_list=fd.readlines()
    fd.close()
    return url_list


class YouKu():
    hds={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (K    HTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"}
    def __init__(self):
        pass
        
    def parse_url(self,result):
        result=result.decode("gbk")
        soup=bs(result)
        filename=soup("input",attrs={"name":"name"})[0]['value']
        fileurl=soup("input",attrs={"name":"inf"})[0]['value']
        fileurl=fileurl[:-1]
        
        return filename.encode("utf-8"),fileurl.encode("utf-8")
        
    def down_url(self,_,Id,url):
        filename,fileurl=_
        filename=filename+'.flv'
        d=downloadPage(fileurl,filename)
        d.addCallback(parseVedio,filename,Id,url)
        return d

@inlineCallbacks
def handler():
    dlist=[]
    count=0
    for line in readUrl():
        Id,url=line.split()
        count+=1
        url=url.strip()
        d=getPage("http://www.flvcd.com/parse.php?format=&kw="+url)
        d.addCallback(youku.parse_url)
        d.addCallback(youku.down_url,Id,url)
        d.addErrback(parse_error,Id,url)
        dlist.append(d)

        if count%5==0:
            print "正在处理五个任务，其他任务稍等"
            ds=defer.DeferredList(dlist,consumeErrors=True)
            yield ds
            dlist=[]
    ds=defer.DeferredList(dlist,consumeErrors=True)
    yield ds



def parseVedio(_,filename,Id,url):

    def ifFace(img,size):
        gray=cv.CreateImage(size,8,1)
        cv.CvtColor(img,gray,cv.CV_BGR2GRAY)
        newMem1=cv.CreateMemStorage(0)
        newMem2=cv.CreateMemStorage(0)
        newMem3=cv.CreateMemStorage(0)
        cv.EqualizeHist(gray,gray)
        face=cv.HaarDetectObjects(gray,c_f,newMem1,1.2,3,cv.CV_HAAR_DO_CANNY_PRUNING,(50,50))
        mouth=cv.HaarDetectObjects(gray,c_m,newMem2,1.2,2,cv.CV_HAAR_DO_CANNY_PRUNING,(10,10))
        body=cv.HaarDetectObjects(gray,c_m,newMem3,1.2,2,cv.CV_HAAR_DO_CANNY_PRUNING,(100,100))
        if face and mouth or body:
            cv.SaveImage("img/out.jpg",img)
            return 1
        else:
            return 0

    capture=cv.CaptureFromFile(filename)
    width=cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH)
    height=cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT)
    size=(int(width),int(height))
    fps=15
    i=0
    count=[0]

    def scanFaces(src):
        total=0
        c=cv.CloneImage(src)
        frams=[]
        frams.append(src)  # 原图

        cv.Flip(c,None,0) 
        frams.append(c)  # 水平翻转后的

        dst=cv.CreateImage((src.height,src.width),
                src.depth,src.channels)
        cv.Transpose(src,dst)
        cv.Flip(dst,None,0)
        frams.append(dst) # 逆时针90
        
        c2=cv.CloneImage(src)
        cv.Flip(c2,None,0) 
        dst=cv.CreateImage((src.height,src.width),
                src.depth,src.channels)
        cv.Transpose(c2,dst)
        frams.append(dst) # 顺时针90

        for i,img in enumerate(frams):
            count[0]+=ifFace(img,(img.width,img.height))

        if count[0]>=15:
            return True
        else:
            return False
            

    while True:
        img=cv.QueryFrame(capture)
        if not img:break
        if int((i+1)%fps)==0:
            if scanFaces(img):
                mess="%s:有脸"%filename
                yesfd.write("%s %s\n"%(Id,url))
                yesfd.flush()
                print mess
                return None
        i+=1
    mess="%s:无脸"%filename
    nofd.write("%s %s\n"%(Id,url))
    nofd.flush()
    print mess

        
if __name__=="__main__":
    youku=YouKu()
    d=handler()
    d.addBoth(parse_finished)

    reactor.run()
