#!usr/bin/env python3
# coding: UTF-8

import socket
import threading


def get_new_messages(sock):
    while True:
        print(sock.recv(1024).decode('utf-8'), end='')


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 8080

sock.connect((host, port))

server_message = sock.recv(1024).decode('utf-8')
print(server_message)

get_new_messages_thread = threading.Thread(target=get_new_messages, args=(sock,), daemon=True)
get_new_messages_thread.start()

while True:
    my_message = input()
    sock.send(my_message.encode('utf-8'))
    print('\033[1A' + "Me: " + my_message + '\033[K')
