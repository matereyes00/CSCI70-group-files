import socket
from colorama import init
from colorama import Fore, Back, Style
from art import *
init()


def start_rps(p1Move, p2Move):
    moves = ["scissors", "paper", "rock"]
    p1_name_answers = []
    p2_name_answers = []
    wins = []
    loses = []
    while True:
        p1_name_answers.append(p1Move)
        p2_name_answers.append(p2Move)

        if p1_name_answers[-1] == p2_name_answers[-1]: # TIE
            print("Tie!")

        elif p1_name_answers[-1] != p2_name_answers[-1]: 
            # USER 1 == SCISSORS
            if p1_name_answers[-1] == moves[0]: # scissors beat paper, scissors lose rock
                if p2_name_answers[-1] == moves[1]:
                    print(f"{p1_name} wins. Scissors beats paper")
                    wins.append(p1_name)
                    loses.append(p2_name)

                elif p2_name_answers[-1] == moves[2]:
                    print(f"{p2_name} wins. Rock beats scissors")
                    wins.append(p2_name)
                    loses.append(p1_name)
                else:
                    print("invalid move")
            
            # USER 1 == PAPER
            elif p1_name_answers[-1] == moves[1]: # paper beats rock, paper lose scissors
                if p2_name_answers[-1] == moves[0]:
                    print(f"{p2_name} wins. Scissors beats paper")
                    wins.append(p2_name)
                    loses.append(p1_name)
                
                elif p2_name_answers[-1] == moves[2]:
                    print(f"{p1_name} wins. Paper beats rock")
                    wins.append(p2_name)
                    loses.append(p1_name)

                else:
                    print("invalid move")
            
            # p1_name == ROCK
            elif p1_name_answers[-1] == moves[2]: # rock beats scissors, rock lose paper
                if p2_name_answers[-1] == moves[0]:
                    print(f"{p1_name} wins. Rock beats Scissors")
                    wins.append(p1_name)
                    loses.append(p2_name)
                
                elif p2_name_answers[-1] == moves[1]:
                    print(f"{p2_name} wins. Paper beats rock")
                    wins.append(p2_name)
                    loses.append(p1_name)

                else:
                    print("invalid move")
            
            # not valid option
            elif p1_name_answers[-1] not in moves:
                print("Sorry, not a valid move.")
                p1Move = input("Try again: ")

            # not valid option
            elif p2_name_answers[-1] not in moves:
                print("Sorry, not a valid move.")
                p2Move = input("Try again: ")


        play_again = input("Play again? (y/n): ")
        if play_again.lower() != "y":
            break


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

    print(f"Please choose 'Rock', 'Paper', or 'Scissors'")
    p1_move = input(' >>> ')

    connected = True
    while connected:
        conn.send(p1_move.encode())  # send data to the client
        p2_move = conn.recv(HEADER).decode(FORMAT) # receiving p2's move
        if not p2_move:
            # if data is not received break
            break
        
        print(Fore.YELLOW + f"[{p1_name} - {socket.gethostbyname(host)}]")
        print(Fore.CYAN, f"{p2_name} did {p2_move}")
        
        start_rps(p1_move, p2_move)

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()