import socket
import os
import sys
from queue import Queue
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0

qs = []
maxI = int(sys.argv[1])

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


def threaded_client(i,q,connection):
    sentLast = ""
    connection.send(str.encode(str(i)))
    while True:
        connection.sendall(str.encode(q.get()))
    connection.close()


for x in range(0,maxI):
    q = Queue(maxsize = 2)
    qs.append(q)
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (x,q, Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

def sendMessage(s):
    for q in qs:
            q.put(s)

while True:
    command = input().split()
    if(command[0] == "q"):
        sendMessage("Exiting")
        break
    if(command[0] == "s"):        
        sendMessage(command[1])

done = False
while done:
    for q in qs:
        done = done and q.empty()
        
ServerSocket.close()