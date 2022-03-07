import socket
import threading

import messaging
from settings import ADDR, DISCONNECT_MSG, SERVER


class Server:
    def __init__(self):
        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_conn.bind(ADDR)
        self.num_clients = 0
        self.clients = {}
        self.messages = []

    def start(self):
        print("[STARTING] server is starting...")
        self.server_conn.listen()  # listen for new connections
        print(f"[LISTENING] server is listening on {SERVER}")
        while True:
            conn, addr = self.server_conn.accept()  # wait for connection
            self.num_clients += 1

            client_thread = threading.Thread(target=self.client, args=(conn, addr))
            client_thread.start()

    def client(self, conn : socket.socket, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        client_name = messaging.recv(conn)
        if client_name == DISCONNECT_MSG:
            self.num_clients -= 1
            conn.close()
            return
        self.clients[client_name] = conn
        # notify everyone about new client
        self.send_all(client_name + " has joined the chat room!")
        while True:
            msg = messaging.recv(conn)
            if msg != "":
                if msg == DISCONNECT_MSG:
                    self.send_all(client_name + " has left the chat room!")
                    break
                # must have a new message
                # tell all other clients
                self.send_all(client_name + ": " + msg)

        print(f"[DISCONNECTED] {addr} lost connection")
        conn.close()
        self.clients.pop(client_name)
        self.num_clients -= 1

    def send_all(self, message):
        # print(message)
        self.messages.append(message)
        for client_name, conn in self.clients.items():
            messaging.send(message, conn)

def main():
    server = Server()
    server.start()

if __name__ == "__main__":
    main()
