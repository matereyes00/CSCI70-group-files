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


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    HEADER = 64 
    FORMAT = 'utf-8'

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    global p2_name, p1_name, p2_move, p1_move
    game_title=text2art("RPS",font='block',chr_ignore=True)
    print(game_title)

    p2_name = input("Please input your name: ")
    client_socket.send(p2_name.encode(FORMAT))
    p1_name = client_socket.recv(HEADER).decode(FORMAT)
    print(f"You are player 2. You are now playing with {p1_name}")
    p2_move = input(" >>> ")  # take input of p2move

    while p2_move.lower().strip() != 'exit()':
        client_socket.send(p2_move.encode(FORMAT))  # send message
        p1_move = client_socket.recv(HEADER).decode(FORMAT)  # receive response

        print(Fore.YELLOW + f'[{p2_name} - {socket.gethostbyname(host)}]')
        print(Fore.CYAN, f"{p1_name} did {p1_move}")  # show in terminal

        start_rps(p1_move, p2_move)

        # p2_move = input( " >>> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()