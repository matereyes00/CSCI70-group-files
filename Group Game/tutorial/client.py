import socket

HEADER = 64 # first msg to the server from the client is gonna be this, tells us the length of the message of the client
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname()) #get SERVER automatically for u
ADDR = (SERVER, PORT)

# set up socket for client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
client.connect(ADDR) 


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # pad it to make it 64
    send_length += b' ' * (HEADER - len(send_length))# addking byte space
    client.send(send_length)
    client.send(message)

send("Hello World!")
player_name = input("Type Player Name: ")
players=[]
players.append(player_name)
print(players)
send(DISCONNECT_MESSAGE)