import socket
import os
import sys
from queue import Queue
from _thread import *

connections = []
ssw = 0
prevssw=-1
message = ""
running = True

class Connection:
    def __init__(self, i):
        self.i = i
        self.ip = ""
        self.q = Queue(maxsize = 2)
        self.client = ""
        self.connected = False

    def accept(self, ServerSocket):
        print(str(self.i)+" is accepting")
        client, address = ServerSocket.accept()
        self.connect(client,address)
    def connect(self, client, address):
        self.client = client
        self.connected = True
        self.ip = address[0]
        print('Connected to: ' + self.ip)
        start_new_thread(self.sendThread, ())

    def sendMessage(self, s):
        print(str(self.i)+" is sending")
        if self.connected:
            self.q.put(s)

    def sendThread(self):
        self.client.send(str.encode(str(self.i)))
        while self.connected:
            self.client.sendall(str.encode(self.q.get()))
        self.client.close()


def acceptConnection(ServerSocket, x):
    global connection
    if(len(connections)<x+1):
        connections.append(Connection(x))
    else:
        connections[x] = Connection(x)
    client, address = ServerSocket.accept()
    connections[x].connect(client, address)

def stepper():
    global ssw
    global prevssw
    global ServerSocket
    global connections
    global message
    global running
    if(not ssw==prevssw):
        print(ssw)
        prevssw=ssw
    
    if(ssw == 0):
        #Reset
        connections = []
        ssw=10
    elif(ssw == 10):
        #Start accepting connections
        ServerSocket = socket.socket()
        host = '0.0.0.0'
        port = 25001
        try:
            ServerSocket.bind((host, port))
            print('Waiting for a connection..')
            ServerSocket.listen(5)
            ssw=20
        except socket.error as e:
            print(str(e))
            ssw=10000 #error 1
            
        maxI = int(sys.argv[1])
        for x in range(0,maxI):
            connections.append(Connection(x))
    elif(ssw == 20):
        #Now listening
        for c in connections:
            start_new_thread(c.accept,(ServerSocket, ))
        ssw = 30
    elif(ssw == 30):
        #check if all connections are live
        maxI = int(sys.argv[1])
        done = True
        for c in connections:
            #print(str(c.i)+" is "+str(c.connected))
            done = done and c.connected
        
        if(done):
            ssw=100
        else:
            ssw=30
    elif(ssw == 100):
        #Init done, now listening to keyboard commands
        command = input().split()
        if(command[0] == "q"):
            message = "Exiting"
            ssw = 1000
        if(command[0] == "s"):        
            message = command[1]
            ssw = 200
    elif(ssw == 200):
        #Send message
        for c in connections:
            c.sendMessage(message)
        message = ""
        ssw=500
    elif(ssw == 500):
        #Wait for everyone to send message
        done = True
        for c in connections:
            done = done and c.q.empty()
        
        if(done):
            ssw=100
        else:
            ssw=500
        
    elif(ssw == 1000):
        #Send quitting message
        for c in connections:
            c.sendMessage(message)
        message = ""
        ssw=1100
    elif(ssw == 1100):
        #break down connections?
        ServerSocket.close()
        ssw=2000
    elif(ssw==2000):
        running=False
    else:
        ssw=0
        
while running:
    stepper()