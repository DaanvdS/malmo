import socket
from vlc import Instance
import time
import platform
import os
import sys
import random
from _thread import *
import socket

ClientSocket = ""

def decodeResponse(s):
    if s=="play":
        player.play()
    elif s=="stop":
            player.stop()
    elif s=="pause":
            player.pause()

def findAudiofile():
    h=socket.gethostname()
    if(h=="pi-value"):
        return "1.mp3"
    elif(h=="pi-connected"):
        return "2.mp3"
    elif(h=="pi-more"):
        return "3.mp3"
    elif(h=="pi-emergence-left"):
        return "4L.mp3"
    elif(h=="pi-emergence-right"):
        return "4R.mp3"
    elif(h=="pi-perspctive"):
        return "5.mp3"
    elif(h=="pi-binary-left"):
        return "6L.mp3"
    elif(h=="pi-binary-right"):
        return "6R.mp3"
    elif(h=="pi-measure"):
        return "7.mp3"
    else:
        return "0.mp3"

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
        #self.mediaList.add_media(self.Player.media_new(os.path.join(path,str(str(random.randint(0, 1))+".mp3"))))
        self.mediaList.add_media(self.Player.media_new(os.path.join(path,findAudiofile())))
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
            host = '11.0.0.30'
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
            player.stop()
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
            decodeResponse(s.replace('alive', ''))
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
    
h=socket.gethostname()

print(h)
main()