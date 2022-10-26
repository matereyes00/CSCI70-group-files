import socket
import threading 
# allows us to separate code so its not waiting for other code to finish 

HEADER = 64 # first msg to the server from the client is gonna be this, tells us the length of the message of the client
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #get SERVER automatically for u
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# BIND
ADDR = (SERVER, PORT)

# make a socket that opens device to other connections
# 1. pick server
# 2. pick socket
# 3. bind socket to that address

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) # anything that connects to this address will hit this socket

# handle communication between server and client
def handle_client(conn, addr):
    # run concurrently with each 
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # wait to receive info from the client
        # make sure we are receiving a valid message (receiving nothing for the first time)
        msg_length = conn.recv(HEADER).decode(FORMAT) # blocking. We wont pass this UNTIL we receive message from client. Receive from the socket.
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            conn.send("Msg received".encode(FORMAT))
    
    conn.close()


# allow our server to listen for connections
# handling connections, pass to handle_client()
# ADDR: What port, what ip address connected to server
# CONN: socket object. Communicate back to the thing connected (info about connection). 
# handle new connections, dist where they need to go
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True: # will continue to listen until off
        conn, addr = server.accept() # blocks, line will wait for a new connection to the server. Address will be stored and what port it came from. 
        # Conn = store object to send info back to that connection

        # whena new connection occurs, we will pass to hand_client, arguments are what we are passing to the function
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        # amt of threads active in this process. Represents num of clients connected. Since there's 1 thread running always, itll tell us there's 1 active connection when theres 2 threads running
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()