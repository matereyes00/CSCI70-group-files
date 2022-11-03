import socket
import sys
from getpass import getpass
from colorama import init
from colorama import Fore, Back, Style
from art import *
init()

wins = []
loses = []

def display_title():
    game_title=text2art("RPS",font='block',chr_ignore=True)
    print(game_title)

def make_a_move():
    print(f"Please choose 'Rock', 'Paper', or 'Scissors'")
    player_move = getpass(">>> ")
    return player_move

def scoreboard():
    p1_score = wins.count(p1_name)
    p2_score = wins.count(p2_name)

    print(f"{p1_name}'s score: {p1_score}")
    print(f"{p2_name}'s score: {p2_score}")

def start_rps(p1Move, p2Move):
    moves = ["scissors", "paper", "rock"]

    while True:
        p1Move = p1Move.lower()
        p2Move = p2Move.lower()
        if p1Move == p2Move: # TIE
            print("Tie!")

        elif p1Move != p2Move: 
            # USER 1 == SCISSORS
            if p1Move == moves[0]: # scissors beat paper, scissors lose rock
                if p2Move == moves[1]:
                    print(f"{p1_name} wins. Scissors beats paper")
                    wins.append(p1_name)
                    loses.append(p2_name)

                elif p2Move == moves[2]:
                    print(f"{p2_name} wins. Rock beats scissors")
                    wins.append(p2_name)
                    loses.append(p1_name)
            
            # USER 1 == PAPER
            elif p1Move == moves[1]: # paper beats rock, paper lose scissors
                if p2Move == moves[0]:
                    print(f"{p2_name} wins. Scissors beats paper")
                    wins.append(p2_name)
                    loses.append(p1_name)
                
                elif p2Move == moves[2]:
                    print(f"{p1_name} wins. Paper beats rock")
                    wins.append(p1_name)
                    loses.append(p2_name)
            
            # p1_name == ROCK
            elif p1Move == moves[2]: # rock beats scissors, rock lose paper
                if p2Move == moves[0]:
                    print(f"{p1_name} wins. Rock beats Scissors")
                    wins.append(p1_name)
                    loses.append(p2_name)
                
                elif p2Move == moves[1]:
                    print(f"{p2_name} wins. Paper beats rock")
                    wins.append(p2_name)
                    loses.append(p1_name)

            # player 2 (client) waits for player 1 to input valid answer
            while p1Move not in moves:
                print(f"Waiting for a valid answer from {p1_name}")
                p1Move = client_socket.recv(HEADER).decode(FORMAT)
                start_rps(p1Move, p2Move)

            # player 2 inputs invalid answer
            while p2Move not in moves:
                print("Sorry, not a valid move. Try again:")
                p2Move = make_a_move()
                p2Move = p2Move.lower()
                client_socket.send(p2Move.encode()) # send revised answer
                start_rps(p1Move, p2Move)

            while p1Move not in moves:
                print(f"Waiting for a valid answer from {p1_name}")
                # start_rps(p1Move, p2Move)

        scoreboard()
        
        play_again = input("Play again? (y/n): ")
        client_socket.send(play_again.encode(FORMAT))
        play_again_resp = client_socket.recv(HEADER).decode(FORMAT)
        if play_again.lower() != "y":
            sys.exit()
        
        elif play_again.lower() == "y":
            p2Move = make_a_move()
            client_socket.send(p2Move.encode(FORMAT))  # send data to the client
            p1Move = client_socket.recv(HEADER).decode(FORMAT) # receiving p1's move
            start_rps(p1Move, p2Move)

def client_program():

    global host, port, HEADER, FORMAT, client_socket
    # host = socket.gethostname()  # as both code is running on same pc
    # port = 6006  # socket server port number
    HEADER = 64 
    FORMAT = 'utf-8'

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate

    # ⚠️ you have to specify the host ip address you want to connect to
    print("Please input the Ip address of the server")
    host = input("")
    print("Please input the port of the server")
    port = int(input(""))
    # client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # client_socket.bind((host, port)) 
    client_socket.connect((host, port))  # connect to the server

    global p2_name, p1_name, p2_move, p1_move
    display_title()

    p2_name = input("Please input your name: ")
    client_socket.send(p2_name.encode(FORMAT))
    p1_name = client_socket.recv(HEADER).decode(FORMAT)
    print(f"You are player 2. You are now playing with {p1_name}")
    
    connected = True
    while connected:
        p2_move = make_a_move()  # take input of p2Move
        client_socket.send(p2_move.encode(FORMAT))  # send message
        p1_move = client_socket.recv(HEADER).decode(FORMAT)  # receive response

        print(Fore.YELLOW + f'[{p2_name} - {socket.gethostbyname(host)}]')
        # print(Fore.CYAN, f"You did {p2_move}. {p1_name} did {p1_move}")  # show in terminal

        start_rps(p1_move, p2_move)

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()