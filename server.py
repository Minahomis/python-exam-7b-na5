from datetime import datetime
from _thread import *
import socket


host = socket.gethostbyname(socket.gethostname())
port = 12345

server = socket.socket()
server.bind((host, port))
server.listen(5)

clients = []
history_file_name = 'historymessage.txt'
history_file = open(history_file_name, 'w')
history_file.close()


def get_time():
    return datetime.now().strftime('%H:%M:%S')


def remove_client(client):
    if client in clients:
        clients.remove(client)
        print(f'{get_time()} Пользователь {client[2]} отключён')


def handle_client(conn, addr, name):
    while True:
        try:
            message = conn.recv(1024).decode()
            if message:
                message_to_print = f'{get_time()}: {addr[0]}: {name}: {message}'
                print(message_to_print)
                send_message(message_to_print, conn)

                message = f'{addr[0]}: {name}: {message}: {get_time()}'
                with open(history_file_name, 'a') as file:
                    file.write(message_to_print + '\n')
            else:
                remove_client((conn, addr, name))
                break
        except:
            remove_client((conn, addr, name))
            continue


def send_message(message, conn):
    for client in clients:
        if client[0] != conn:
            try:
                client[0].send(message.encode())
            except:
                continue

 
print(get_time(), 'Сервер включён')
print('IP:', host)

while True:
    try:
        conn, addr = server.accept()
        name = conn.recv(1024).decode()

        clients.append((conn, addr, name))
        print(get_time(), 'Пользователь', name, 'подлкючился')
        start_new_thread(handle_client, (conn, addr, name))
    except:
        break

server.close()
