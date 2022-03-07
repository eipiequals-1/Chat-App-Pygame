import socket

# networking settings
PORT = 8080
HEADER = 64 # 64 byte message that tells next message size
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT"

# client settings
WIDTH = 800
HEIGHT = 450
FPS = 60

# pygame settings
COLORS = {
    "white" : (255, 255, 255), 
    "black" : (0, 0, 0),
    "grey" : (128, 128, 128),
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue" : (0, 0, 255),
    "yellow" : (255, 255, 0),
    "purple" : (0, 0, 255)
}