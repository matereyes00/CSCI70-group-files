import socket
from colorama import init
from colorama import Fore, Back, Style
init()


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    HEADER = 64 
    FORMAT = 'utf-8'

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    P2_name = input("Please input your name: ")
    client_socket.send(P2_name.encode(FORMAT))
    p1_name = client_socket.recv(HEADER).decode(FORMAT)
    print(f"You are now chatting with {p1_name}")
    message = input(" >>> ")  # take input

    while message.lower().strip() != 'exit()':
        client_socket.send(message.encode(FORMAT))  # send message
        data = client_socket.recv(HEADER).decode(FORMAT)  # receive response

        print(Fore.YELLOW + f'[{P2_name} - {socket.gethostbyname(host)}]')
        print(Fore.CYAN, f"Received a message from {p1_name}: {data}")  # show in terminal

        message = input( " >>> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()