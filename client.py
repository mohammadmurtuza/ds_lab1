import socket

ip_port = ('127.0.0.1', 9999)

s = socket.socket()
s.connect(ip_port)

while True:
    inp = input('input command or message: ').strip()
    if not inp:
        continue
    s.sendall(inp.encode())

    if inp == "exit":
        print("Goodbye")
        break

    server_reply = s.recv(1024).decode()
    print(server_reply)

s.close()
