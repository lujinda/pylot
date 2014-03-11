import sys,os
import cv
from PIL import Image,ImageDraw

def detectObjects(image):
    storage=cv.CreateMemStorage()
    cascade=cv.Load('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
    faces=cv.HaarDetectObjects(image,cascade,storage)
    
    result=[]
    for (x,y,w,h),n in faces:
        result.append((x,y,x+w,y+h))
    return result

def process(infile,outfile):
    image=cv.LoadImage(infile)
    faces=detectObjects(image)
    im=Image.open(infile)
    if faces:
        draw=ImageDraw.Draw(im)
        for f in faces:
            draw.rectangle(f,outline=(0,255,0))
        im.save(outfile,"JPEG")
    
process('input.jpg','ouput.jpg')
