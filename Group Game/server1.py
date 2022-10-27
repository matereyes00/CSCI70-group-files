import socket
from colorama import init
from colorama import Fore, Back, Style
from art import *
init()

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024
    HEADER = 64 
    FORMAT = 'utf-8'
    SERVER = socket.gethostbyname(socket.gethostname()) #get SERVER automatically for u

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    print("[STARTING] server is starting...")
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, address = server_socket.accept()  # accept new connection

    global p2_name, p1_name, p2_move, p1_move
    game_title=text2art("RPS",font='block',chr_ignore=True)
    print(game_title)

    p1_name = input("Please input your name: ")
    conn.send(p1_name.encode(FORMAT))

    p2_name = conn.recv(HEADER).decode(FORMAT)
    print(f"You are player 1. You are now playing with {p2_name}")

    connected = True
    while connected:
        p2_move = conn.recv(HEADER).decode(FORMAT)
        if not p2_move:
            # if data is not received break
            break
        
        print(Fore.YELLOW + f"[{p1_name} - {socket.gethostbyname(host)}]")
        print(Fore.CYAN, f"{p2_name} did {p2_move}")
        p2_move = input(' >>> ')
        
        conn.send(p2_move.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()