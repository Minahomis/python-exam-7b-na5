import socket
from _thread import *


client = socket.socket()
port = 12345

hostname = input('Введите IP сервера: ')
name = input('Введите своё имя: ')


def handle_server_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print(message)
            else:
                print('Проблемы с соединением с сервером')
                break
        except:
            print('Проблемы с соединением с сервером')
            break


try:
    client.connect((hostname, port))
except:
    print('Ошибка подключения (проверьте IP)')
    exit()
print('Подключён с серверу\n')
client.send(name.encode())

start_new_thread(handle_server_messages, ())

user_input = ' '
while user_input != '/exit':
    try:
        if not user_input.isspace():
            client.send(user_input.encode())
        user_input = input()
    except:
        break

client.close()
print('Вы отключились от чата')
