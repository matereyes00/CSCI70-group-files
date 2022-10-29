import socket
from colorama import init
from colorama import Fore, Back, Style
from art import *
init()

def display_title():
    game_title=text2art("RPS",font='block',chr_ignore=True)
    print(game_title)

def make_a_move():
    print(f"Please choose 'Rock', 'Paper', or 'Scissors'")
    player_move = input(">>> ")
    return player_move

def start_rps(p1Move, p2Move):
    moves = ["scissors", "paper", "rock"]
    wins = []
    loses = []
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
                    wins.append(p2_name)
                    loses.append(p1_name)
            
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

        print("================================")
        play_again = input("Play again? (y/n): ")
        client_socket.send(play_again.encode(FORMAT))
        play_again_resp = client_socket.recv(HEADER).decode(FORMAT)
        if play_again.lower() != "y":
            # sending server that client doesnt want to play again
            if play_again_resp == "n":
                break
        
        elif play_again.lower() == "y":
            p2Move = make_a_move()
            client_socket.send(p2Move.encode(FORMAT))  # send data to the client
            p1Move = client_socket.recv(HEADER).decode(FORMAT) # receiving p1's move
            start_rps(p1Move, p2Move)


def client_program():

    global host, port, HEADER, FORMAT, client_socket
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    HEADER = 64 
    FORMAT = 'utf-8'

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
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
        print(Fore.CYAN, f"You did {p2_move}. {p1_name} did {p1_move}")  # show in terminal

        start_rps(p1_move, p2_move)

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()