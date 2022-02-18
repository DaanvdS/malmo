import socket
from vlc import Instance
import time
import platform
import os
import sys
from _thread import *

ClientSocket = ""

def decodeResponse(s):
    if s=="play":
        player.play()
    elif s=="stop":
            player.stop()
    elif s=="pause":
            player.pause()


class VLC:
    def __init__(self):
        self.Player = Instance('--loop')

    def addPlaylist(self):
        self.mediaList = self.Player.media_list_new()
        if platform.system()=="Windows":
            path = r"D:/Projects/Camiel/malmo/Audio/"
        else:
            path = r"/home/pi/Desktop/malmo/Audio/"
        #songs = os.listdir(path)
        #for s in songs:
        #    self.mediaList.add_media(self.Player.media_new(os.path.join(path,s)))
        self.mediaList.add_media(self.Player.media_new(os.path.join(path,str(str(i%2)+".wav"))))
        self.listPlayer = self.Player.media_list_player_new()
        self.listPlayer.set_media_list(self.mediaList)
    def play(self):
        self.listPlayer.play()
    def pause(self):
        self.listPlayer.pause()
    def stop(self):
        self.listPlayer.stop()

player = VLC()
player.addPlaylist()

lastAlive = 0
connected = False
closing = False

def start():
    global ClientSocket
    global running
    global lastAlive
    global connected
    print('Waiting for connection')
    while(not connected):
        try:
            ClientSocket = socket.socket()
            host = '11.0.0.54'
            port = 25001
            ClientSocket.connect((host, port))
            connected=True
        except socket.error as e:
            print("Didn't work")
            time.sleep(5)
            connected=False

    print("Connected")
    running = True
    lastAlive = 0
    startReceiving()

def receive():
    global connected
    global lastAlive
    global closing
    while connected:
        try:
            Response = ClientSocket.recv(1024)
        except socket.error as e:
            print("Lost server")
            connected = False
            break
        if Response.decode('utf-8') == "Exiting":
            print("Server exited")
            connected=False
            closing=True
            break
        
        s = Response.decode('utf-8')
        if(s=="alive"):
            lastAlive=time.time()
        else:
            decodeResponse(s)
            print(s)

def listenToSTDIN():
    global connected
    while(connected):
        command = input().split()
        if(command[0] == "break"):
            sys.exit(0)
            break

def startReceiving():
    global ClientSocket
    global connected
    start_new_thread(receive, ())
    start_new_thread(listenToSTDIN, ())
    
    while(connected):
        time.sleep(1)
    time.sleep(2)
    ClientSocket.close()

def main():
    start()
    while(connected):
        time.sleep(5)
    if(not closing): main()
    
main()