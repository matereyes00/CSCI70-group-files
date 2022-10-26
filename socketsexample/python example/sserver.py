import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = socket.gethostbyname('www.google.com')
print (ip)

HOST = "192.168.55.105"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print (data)
            if not data:
                break
            conn.sendall(data)