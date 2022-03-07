import threading
import pygame
import socket

from settings import ADDR, DISCONNECT_MSG, FORMAT, FPS, HEADER, HEIGHT, WIDTH, COLORS
from ui.text_box import TextBox
from ui.font import Font
import messaging

class Client:
    def __init__(self):
        self.name = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(ADDR)

    def send(self, msg : str):
        messaging.send(msg, self.socket)

    def close(self):
        self.socket.close()

class ChatApp:
    def __init__(self):
        self.client = Client()
        # initialize pygame, screen, and clock
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Chat - Client")
        self.clock = pygame.time.Clock()
        self.running = True
        self.messages = []

    def get_name(self):
        text_box = TextBox(10, 10, WIDTH - 10 * 2, 50, "./res/Lato-Medium.ttf")
        pygame.time.set_timer(pygame.USEREVENT, round(0.20 * 1000))
        while self.running:
            can_backspace = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.client.name = text_box.get_text().strip()
                    else:
                        text_box.user_input(event)
                elif event.type == pygame.USEREVENT:
                    can_backspace = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE] and can_backspace:
                text_box.backspace()

            # update
            text_box.update(pygame.mouse.get_pos())
            # check if the name has been set
            if self.client.name != "":
                break

            # render
            self.screen.fill(COLORS["white"])
            text_box.draw(self.screen, COLORS["white"], COLORS["black"])
            pygame.display.update()
            self.clock.tick(FPS)

        if self.running:
            pygame.display.set_caption("Chat - " + self.client.name)
            self.client.send(self.client.name)
        else:
            self.client.send(DISCONNECT_MSG)
            self.client.close()

    def msg_from_server(self):
        def recv():
            while True:
                # retreive any new messages
                msg = messaging.recv(self.client.socket)
                if msg != "":
                    self.messages.append(msg)
                    # print(msg)
                if not self.running:
                    return
        recv_message_thread = threading.Thread(target=recv, args=())
        recv_message_thread.start()

    def run(self):
        self.get_name()
        if not self.running:
            return
        text_box = TextBox(10, HEIGHT - 60, WIDTH - 10 * 2, 50, "./res/Lato-Medium.ttf")
        pygame.time.set_timer(pygame.USEREVENT, round(0.20 * 1000))
        self.msg_from_server()  # separate thread to receive the messages
        font = Font("./res/Lato-Medium.ttf", round(HEIGHT / 20))
        while self.running:
            can_backspace = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # send new message to server
                        self.client.send(text_box.get_text())
                        # clear message
                        text_box.clear_text()
                    else:
                        text_box.user_input(event)
                elif event.type == pygame.USEREVENT:
                    can_backspace = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE] and can_backspace:
                text_box.backspace()

            # update
            text_box.update(pygame.mouse.get_pos())
            # render
            self.screen.fill(COLORS["white"])

            offset_y = round(HEIGHT * 0.05)
            spacing = round(font.font.get_height() * 1.5)
            all_msg_height = offset_y + (len(self.messages)) * spacing
            if all_msg_height > text_box.rect.top:
                offset_y -= all_msg_height - text_box.rect.top + offset_y
            # render messages
            for i, message in enumerate(self.messages):
                font.render(self.screen, message, COLORS["black"], round(WIDTH * 0.04), round(offset_y + i * spacing))

            # render text box
            text_box.draw(self.screen, COLORS["white"], COLORS["black"])
            # flip double buffer and control fps
            pygame.display.update()
            self.clock.tick(FPS)
        
        self.client.send(DISCONNECT_MSG)
        self.client.close()

def main():
    chat = ChatApp()
    chat.run()

if __name__ == "__main__":
    main()