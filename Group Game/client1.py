import socket
from inspect import isclass
from colorama import init
from colorama import Fore, Back, Style
init()


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    HEADER = 64 
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    P2_name = input("Please input your name: ")
    message = input(" >>> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode(FORMAT))  # send message
        data = client_socket.recv(HEADER).decode(FORMAT)  # receive response

        print(Fore.CYAN, f'[{P2_name} - {socket.gethostbyname(host)}]')
        print(Fore.CYAN, f"Received a message from server {data}")  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()