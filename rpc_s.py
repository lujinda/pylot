#!/usr/bin/env python
import SimpleXMLRPCServer
import os
import subprocess

allow_cmds=["ls","cat","ifconfig"]

def ls(directory):
    try:
        return os.listdir(directory)
    except OSError:
        return []

def do(cmds):
    cmd=cmds.split(' ',1)[0]
    if cmd.strip() in allow_cmds:
        result=subprocess.Popen(cmds.split(),stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        error=result.stderr.read().strip()
        if error:return error
        result=result.stdout.read().strip()
        return result
    else:
        return None
    
if __name__=="__main__":
    s=SimpleXMLRPCServer.SimpleXMLRPCServer(('127.0.0.1',8765))
    s.register_function(do)
    s.serve_forever()

