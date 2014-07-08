#coding:utf8
import optparse
import os
import subprocess
import re

def parse_args():
    usage="""usage: %prog[option] vedio-file"""
    parser=optparse.OptionParser(usage)
    options,args=parser.parse_args()

    if len(args)!=1:
        print parser.format_help()
        parser.exit()

    if not os.path.isfile(args[0]):
        parser.error("No such file: %s"%args[0])

    return options,args[0]

class CommandNotFound(Exception):pass

class GetVedioInfo():
    def __init__(self,path):
        import commands
        import webbrowser
        self.path=path
        if commands.getstatusoutput("type ffmpeg")[0]:
            webbrowser.open_new_tab("http://ffmpeg.org/")
            raise CommandNotFound,"ffmpeg is not install."
    
    def getLong(self):
        result=subprocess.Popen(["ffmpeg","-i",self.path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            result=result.stdout.read()
        except NoneType:
            result=result.stderr.read()

        import re
        longtime=re.findall(r"Duration:\s*?(\d+):(\d+):(\d+)",result)
        print longtime

def main():
    options,filepath=parse_args()
    vedio=GetVedioInfo(filepath)
    vedio.getLong()
    

if __name__=='__main__':
    main()
