import socket
from settings import FORMAT, HEADER

def send(msg : str, conn : socket.socket):
    message = msg.encode(FORMAT)
    msg_len = len(message)

    # send = message to let server know what size of next message
    send_length = str(msg_len).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def recv(conn : socket.socket):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length != "":
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg
    return ""