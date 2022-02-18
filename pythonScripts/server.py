import socket
import os
import sys
import time
from queue import Queue
from _thread import *

class Connection:
    def __init__(self):
        self.ip = ""
        self.q = Queue(maxsize = 2)
        self.client = ""
        self.connected = False
        
    def connect(self, client, address):
        self.client = client
        self.connected = True
        self.ip = address[0]
        print('Connected to: ' + self.ip)
        start_new_thread(self.sendThread, ())

    def sendMessage(self, s):
        if self.connected:
            self.q.put(s)
            
    def sendAlive(self):
        if self.connected:
            self.q.put("alive")

    def sendThread(self):
        while self.connected:
            try:
                self.client.sendall(str.encode(self.q.get()))
            except socket.error as e:
                self.connected=False
                print("Lost: "+str(self.ip))
        self.client.close()

class Server:
    def __init__(self):
        self.connections = []
        self.ssw = 0
        self.maxI = int(sys.argv[1])
        self.x=0
        self.prevssw=-1
        self.message = "play"
        self.running = True
        self.doneAccepting = False
        self.lastCheckTime = 0
        self.lastAlive = 0
        self.ServerSocket=""
        
    def findConnctionWithIP(self,ip):
        for i in range(0,len(self.connections)):
            if(self.connections[i].ip == ip and self.connections[i].connected==False):
                return i
        
        return -1

    def acceptConnection(self,x):
        client, address = self.ServerSocket.accept()
        self.connections[x].connect(client, address)
        self.doneAccepting=True
        
    def acceptConnectionIP(self,ip):
        client, address = self.ServerSocket.accept()
        if(address[0]==ip):
            i=self.findConnctionWithIP(ip)
            if(i>=0):
                print("Recovered "+str(ip))
                self.connections[i].connect(client, address)
                self.doneAccepting=True
            else:
                print("IP not found in connections, this shouldnt be possible")
        else: 
            print(address)
            print(ip)

    def stepper(self):
        if(not self.ssw==self.prevssw):
            print(self.ssw)
            self.prevssw=self.ssw
        
        if(self.ssw == 0):
            #Reset
            self.connections = []
            self.ssw=10
        elif(self.ssw == 10):
            #Start accepting connections
            self.ServerSocket = socket.socket()
            host = '0.0.0.0'
            port = 25001
            try:
                self.ServerSocket.bind((host, port))
                print('Waiting for a connection..')
                self.ServerSocket.listen(5)
                self.ssw=20
            except socket.error as e:
                print(str(e))
                self.ssw=10000 #error 1
                
            
            for i in range(0,self.maxI):
                self.connections.append(Connection())
            
            self.x=0
            self.doneAccepting=False
        elif(self.ssw == 20):
            #Now listening
            start_new_thread(self.acceptConnection,(self.x, ))
            self.ssw = 30
        elif(self.ssw == 30):
            #Check if accepting is done (1 conn)
            if(self.doneAccepting):
                self.x=self.x+1
                if(self.x<self.maxI):
                    self.doneAccepting=False
                    self.ssw=20
                else:
                    self.ssw=40
            else:
                self.ssw=30
        elif(self.ssw == 40):
            #check untill all connections are live
            done = True
            for c in self.connections:
                done = done and c.connected
            
            if(done):
                self.lastCheckTime=time.time()
                self.ssw=100
            else:
                self.ssw=40
        elif(self.ssw == 50):
            #check if all connections are still live if not checked in the last 30 seconds
            for c in self.connections:
                if(not c.connected):
                    start_new_thread(self.acceptConnectionIP,(c.ip, ))
                
            self.ssw=100
        elif(self.ssw == 100):
            if(self.lastAlive+1<time.time()):
                for c in self.connections:
                    c.sendAlive()
                self.lastAlive=time.time()
            if(self.lastCheckTime+1<time.time()):
                self.lastCheckTime=time.time()
                self.ssw=50
            
            if(not self.message==""):
                if(self.message=="Exiting"):
                    self.ssw=1000
                else: self.ssw=200
                
        elif(self.ssw == 200):
            #Send message
            for c in self.connections:
                c.sendMessage(self.message)
            self.message = ""
            self.ssw=500
        elif(self.ssw == 500):
            #Wait for everyone to send message
            done = True
            for c in self.connections:
                done = done and c.q.empty()
            
            if(done):
                self.ssw=100
            else:
                self.ssw=500
            
        elif(self.ssw == 1000):
            #Send quitting message
            for c in self.connections:
                c.sendMessage(self.message)
            self.message = ""
            self.ssw=1100
        elif(self.ssw == 1100):
            #break down connections
            for c in self.connections:
                c.connected = False
            self.ServerSocket.close()
            self.ssw=2000
        elif(self.ssw==2000):
            self.running=False
        else:
            self.ssw=0

serverInst = Server()

def stepperRun():
    while serverInst.running:
        serverInst.stepper()

start_new_thread(stepperRun, ())

while(serverInst.running):
    command = input().split()
    if(command[0] == "q"):
        serverInst.message = "Exiting"
        break
    if(command[0] == "s"):        
        serverInst.message = command[1]
    if(command[0] == "break"):
        serverInst.ssw=1000
        break

while(serverInst.running):
    time.sleep(1)    