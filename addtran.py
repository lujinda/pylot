#!/usr/bin/env python
#coding:utf8
import sys,base64,re,wx,chardet
def getThunder(url):
    url="AA%sZZ" %url
    return "thunder://" + base64.encodestring(url).replace('\n','')
def getQqdl(url):
    return "qqdl://" + base64.encodestring(url).replace('\n','')
def getFlashget(url):
    url="[FLASHGET]" + url +"[FLASHGET]"
    return "flashget://" + base64.encodestring(url).replace('\n','')+'&1926'
    
def getUrl(url):
    if url.lower().startswith('thunder://'):
        url=base64.decodestring(url[10:])
        url=url[2:-2]
    elif url.lower().startswith('flashget://'):
        url=base64.decodestring(url[11:url.find('&')])
        url=url[10:-10]
    elif url.lower().startswith('qqdl://'):
        url=base64.decodestring(url[7:])
    elif re.match(r'^(https?|ftp)://',url.lower()):
        url=url
    else:
        url=""
    return url
if __name__=='__main__':
    try:
        myurl=getUrl(sys.argv[1])
    except:
        print '使用方法:命令+地址（可以是旋风，快车，迅雷或真实地址）'
        sys.exit()
    if myurl:
        print '真实地址:%s\n旋风地址:%s\n快车地址:%s\n迅雷地址:%s' %(myurl,getQqdl(myurl),getFlashget(myurl),getThunder(myurl))
    else:
        print '您输入的地址格式不正确哦，请好好检查一下~~'
