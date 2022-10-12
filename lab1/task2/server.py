#!usr/bin/env python3
# coding: UTF-8

import socket
import threading

last_messages = []


def login(conn, clients):
    nickname = f"User_{len(clients)+1}"
    
    clients[nickname] = conn
    conn.send('\nSucceed!\n'.encode('utf-8'))
    
    threading.Thread(target=updates_handler, args=(nickname, conn, clients), daemon=True).start()

    return
                

def updates_handler(name, client, clients):
    
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                messg = f"{name}: {message}"

                last_messages.append(messg)
                print(messg)
                if message:
                    for nickname, conn in clients.items():
                        try:
                            if conn != client:

                                conn.send((messg+'\n').encode('utf-8'))
                        except OSError:
                            conn.close()
                            clients.pop(nickname)
            except ConnectionResetError:
                client.close()
            except OSError:
                break
            except RuntimeError:
                continue


def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 8080

    sock.bind((host, port))

    sock.listen(5)

    print('The server is waiting for connection')

    clients = dict()

    while True:
        try:
            conn, addr = sock.accept()

            if conn not in clients:
                login(conn, clients)
                print(f'Got a connection from {addr}')
        except KeyboardInterrupt:
            break
        except:           
            continue
        

    conn.close()

start_server()