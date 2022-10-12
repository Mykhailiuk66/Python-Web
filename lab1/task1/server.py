#!usr/bin/env python3
# coding: UTF-8

from datetime import datetime
import socket
import threading
import time

last_messages = []


def main():
    start_server()


def updates_handler(conn):
        while True:
            try:
                message = conn.recv(1024).decode('utf-8')

                print(message, datetime.now())


                if message == 'exit':
                    conn.close()
                    break
                
                if message:
                    threading.Thread(target=send_message, args=(conn, message, 5), daemon=True).start()

            except ConnectionResetError:
                conn.close()
            except OSError:
                break
            except RuntimeError:
                continue


def send_message(conn, message, timeout=0):
    time.sleep(timeout)
    conn.send((message+'\n').encode('utf-8'))

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 8080

    sock.bind((host, port))

    sock.listen(5)

    print('The server is waiting for connection')


    while True:
        try:
            conn, addr = sock.accept()

            print(f'Got a connection from {addr}')

            threading.Thread(target=updates_handler, args=(conn,), daemon=True).start()

        except KeyboardInterrupt:
            break
        except:           
            continue
        

    conn.close()


if __name__ == "__main__":
    main()