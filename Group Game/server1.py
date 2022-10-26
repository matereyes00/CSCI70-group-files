import socket
from colorama import init
from colorama import Fore, Back, Style
import inspect
init()


def RPS_game(user1, user2):
    user1 = input("Enter P1 name: ")
    user2 = input("Enter P2 name: ")

    moves = ["scissors", "paper", "rock"]
    user1_answers = []
    user2_answers = []

    wins = []
    loses = []

    while True:
        user1_move = input("Enter P1 move:")
        user2_move = input("Enter P2 move:")
        user1_answers.append(user1_move)
        user2_answers.append(user2_move)

        if user1_answers[-1] == user2_answers[-1]: # TIE
            print("Tie!")

        elif user1 != user2: 
            # USER 1 == SCISSORS
            if user1_answers[-1] == moves[0]: # scissors beat paper, scissors lose rock
                if user2_answers[-1] == moves[1]:
                    print(f"{user1} wins. Scissors beats paper")
                    wins.append(user1)
                    loses.append(user2)

                elif user2_answers[-1] == moves[2]:
                    print(f"{user2} wins. Rock beats scissors")
                    wins.append(user2)
                    loses.append(user1)
                else:
                    print("invalid move")
            
            # USER 1 == PAPER
            elif user1_answers[-1] == moves[1]: # paper beats rock, paper lose scissors
                if user2_answers[-1] == moves[0]:
                    print(f"{user2} wins. Scissors beats paper")
                    wins.append(user2)
                    loses.append(user1)
                
                elif user2_answers[-1] == moves[2]:
                    print(f"{user1} wins. Paper beats rock")
                    wins.append(user2)
                    loses.append(user1)

                else:
                    print("invalid move")
            
            # USER1 == ROCK
            elif user1_answers[-1] == moves[2]: # rock beats scissors, rock lose paper
                if user2_answers[-1] == moves[0]:
                    print(f"{user1} wins. Rock beats Scissors")
                    wins.append(user1)
                    loses.append(user2)
                
                elif user2_answers[-1] == moves[1]:
                    print(f"{user2} wins. Paper beats rock")
                    wins.append(user2)
                    loses.append(user1)

                else:
                    print("invalid move")
            
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

    p2_name = conn.recv(HEADER).decode(FORMAT)
    print(f"You are now chatting with {p2_name}")

    P1_name = input("Please input your name: ")
    conn.send(P1_name.encode(FORMAT))
    
    connected = True
    while connected:
        data = conn.recv(HEADER).decode(FORMAT)
        if not data:
            # if data is not received break
            break
        
        print(Fore.YELLOW + f"[{P1_name} - {socket.gethostbyname(host)}]")
        print(Fore.CYAN, f"Received a message from {p2_name}: {data}")
        data = input(' >>> ')
        
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()