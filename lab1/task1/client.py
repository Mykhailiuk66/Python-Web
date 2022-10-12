#!usr/bin/env python3
# coding: UTF-8

import socket
import threading

def main():
    start_client()


def get_new_messages(sock):
    while True:
        print(sock.recv(1024).decode('utf-8'), end='')


def start_client():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 8080

    sock.connect((host, port))


    get_new_messages_thread = threading.Thread(target=get_new_messages, args=(sock,), daemon=True)
    get_new_messages_thread.start()


    while True:
        my_message = input()

        if my_message == 'exit': break

        sock.send(my_message.encode('utf-8'))
        print('\033[1A' + "Me: " + my_message + '\033[K')


if __name__ == "__main__":
    main()