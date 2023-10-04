import socket
import threading

# Initialize a socket object and specify the server host and port.
host = '127.0.0.1'  # Server host (localhost in this example)
port = 9998        # Port to connect to

# Create a socket connection to the server.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# Function to send messages to the server.
def send_messages():
    while True:
        inp = input('Input msg: ').strip()
        if not inp:
            continue

        s.sendall(inp.encode())

        if inp == "exit":
            print("Goodbye")
            break

# Function to receive messages from the server.
def receive_messages():
    while True:
        try:
            server_reply = s.recv(1024).decode()
            print(server_reply)
        except ConnectionResetError:
            print("Connection to the server was lost.")
            break

# Create two separate threads for sending and receiving messages.
send_thread = threading.Thread(target=send_messages)
receive_thread = threading.Thread(target=receive_messages)

# Start the threads.
send_thread.start()
receive_thread.start()

# Wait for both threads to complete.
send_thread.join()
receive_thread.join()

# Close the socket.
s.close()
