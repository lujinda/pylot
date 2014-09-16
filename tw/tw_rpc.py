import os
import subprocess
from twisted.spread import pb
from twisted.internet import reactor

allow_cmds=("ls","cat","ifconfig")

class PBDirLister(pb.Root):
    def remote_do(self,cmd):
        try:
            if cmd[0].strip()\
                    not in allow_cmds:return ' '.join(cmd)+" not is a allow cmd"
            result=subprocess.Popen(cmd,stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            error=result.stderr.read().strip()
            out=result.stdout.read().strip()
            if error:return error
            else:return out
        except Exception,e:
            pass

if __name__=="__main__":
    reactor.listenTCP(1234,pb.PBServerFactory(PBDirLister()))
    reactor.run()
