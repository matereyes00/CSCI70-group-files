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
            # ORIGINAL
            # player 1 (server) waits for player 2 to input valid answer
            while p2Move not in moves:
                    print(f"Waiting for a valid answer from {p2_name}")
                    p2Move = conn.recv(HEADER).decode(FORMAT)
                    start_rps(p1Move, p2Move)
                
            # player 1 inputs invalid answer
            if p1Move not in moves:
                print("Sorry, not a valid move. Try again:")
                p1Move = make_a_move()
                p1Move = p1Move.lower()
                conn.send(p1Move.encode()) # send revised answer
                start_rps(p1Move, p2Move)

        print("================================")
        play_again = input("Play again? (y/n): ")
        conn.send(play_again.encode(FORMAT))
        play_again_resp = conn.recv(HEADER).decode(FORMAT)
        if play_again.lower() != "y":
            # sending to client that the server doesn't want to play again
            if play_again_resp == "n":
                break
        
        elif play_again.lower() == "y":
            p1Move = make_a_move()
            conn.send(p1Move.encode(FORMAT))  # send data to the client
            p2Move = conn.recv(HEADER).decode(FORMAT) # receiving p2's move
            start_rps(p1Move, p2Move)


def server_program():
    global host, port, HEADER, FORMAT, SERVER, conn
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024
    HEADER = 64 
    FORMAT = 'utf-8'
    SERVER = socket.gethostbyname(socket.gethostname()) #get SERVER automatically for u
    global p2_name, p1_name, p2_move, p1_move


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    print("[STARTING] server is starting...")
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, address = server_socket.accept()  # accept new connection

    display_title()

    p1_name = input("Please input your name: ")
    conn.send(p1_name.encode(FORMAT))
    p2_name = conn.recv(HEADER).decode(FORMAT)
    print(f"You are player 1. You are now playing with {p2_name}")
    
    connected = True
    while connected:
        p1_move = make_a_move()
        conn.send(p1_move.encode(FORMAT))  # send data to the client
        p2_move = conn.recv(HEADER).decode(FORMAT) # receiving p2's move
        
        print(Fore.YELLOW + f"[{p1_name} - {socket.gethostbyname(host)}]")
        print(Fore.CYAN, f"You did {p1_move}. {p2_name} did {p2_move}")

        start_rps(p1_move, p2_move)

        if p1_move == "exit()":
            connected = False

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()