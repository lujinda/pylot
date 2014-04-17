import socket

host="127.0.0.1"
port=1234
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))

s.listen(10)
conn,addr=s.accept()
conn.sendall("ok\n")
print conn.recv(1024),
s.close()

