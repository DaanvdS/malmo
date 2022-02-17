import socket
from vlc import Instance
import time
import platform
import os
import sys

ClientSocket = socket.socket()
host = '11.0.0.54'
port = 25001

def decodeResponse(s):
    if s=="play":
        player.play()
    elif s=="stop":
            player.stop()
    elif s=="pause":
            player.pause()


print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    sys.exit("Didn't work")


i = int(ClientSocket.recv(1024).decode('utf-8'))
print("Connected, we are number "+str(i))

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
        i=0
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

while True:
    Response = ClientSocket.recv(1024)
    if Response.decode('utf-8') == "Exiting":
        print("Server exited")
        break
    
    s = Response.decode('utf-8')
    decodeResponse(s)
    print(s)

ClientSocket.close()