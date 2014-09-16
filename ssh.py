#!/usr/bin/python
import paramiko
import sys

class ssh:
    def __init__(self,username,password,host):
        try:
            self.ssh=paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(host,22,username,password,timeout=5)
        except:
            print "Error"
            sys.exit(1)

    def execComm(self,cmd):
        stdin,stdout,stderr=self.ssh.exec_command(cmd)
        for out in stdout.readlines():
            print out,

    def lsFile(self,total,_):
        for file_attr in self.sftp.listdir_attr('.'):
            print file_attr.longname

    def getFile(self):
        self.sftp=self.ssh.open_sftp()
        self.sftp.get('t.txt','tt.txt',self.lsFile)

if __name__=="__main__":
    username="ljd"
    password="zxc123"
    host="localhost"
    connect=ssh(username,password,host)
    connect.execComm("who")
    connect.getFile()
