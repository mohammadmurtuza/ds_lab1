import socket
import threading

# Initialize a socket object and bind it to a specific host and port.
host = '127.0.0.1'  # Server host (localhost in this example)
port = 9996       # Port to listen on
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))

# Store a dictionary to keep track of client connections and their IDs.
clients = {}
client_id_counter = 1


# Function to send the list of active client IDs to a requesting client.
def send_active_client_ids(client_socket):
    global clients
    active_client_ids = list(clients.keys())
    client_socket.send(f"Active Clients: {active_client_ids}".encode())

# Function to forward a message to a target client.
def forward_message(client_socket, target_id, message):
    global clients
    if target_id in clients:
        target_socket = clients[target_id]
        message_to_send = f"{client_id}: {message}"
        target_socket.send(message_to_send.encode())
        client_socket.send("Message sent.".encode())  # Acknowledgment to the sender
    else:
        client_socket.send("Target client not found.".encode())
# Store a dictionary to keep track of chat history.
chat_history = {}

# Function to retrieve chat history between two clients.
def retrieve_chat_history(client_socket, target_id):
    global chat_history
    if target_id in chat_history:
        history = chat_history[target_id]
        for msg in history:
            client_socket.send(msg.encode())
    else:
        client_socket.send("No chat history found.".encode())

# Function to handle each client's connection.
def handle_client(client_socket, client_id):
    try:
        # Send the client their unique ID.
        client_socket.send(f"Welcome! Your ID is {client_id}".encode())

        while True:
            # Receive data from the client.
            data = client_socket.recv(1024).decode()
            if not data:
                print(f"Client {client_id} disconnected.")
                break

            # Split the data into command and parameters.
            parts = data.split(' ', 1)
            command = parts[0].lower()
            
            if command == 'list':
                send_active_client_ids(client_socket)
            elif command.startswith('forward'):
                print(len(parts))
                if len(parts)<2:
                    print("Incorrect syntax")
                    client_socket.send(f"incorrect syntax".encode())
                    continue
                parts = parts[1].split(' ', 1)
                target_id = int(parts[0])
                message = parts[1]
                forward_message(client_socket, target_id, message)
            elif command.startswith('history'):
                if len(parts)<1:
                    print("Incorrect syntax")
                    client_socket.send(f"incorrect syntax".encode())
                    continue
                parts = parts[1].split(' ', 1)
                target_id = int(parts[0])
                retrieve_chat_history(client_socket, target_id)
            elif command == 'exit':
                client_socket.send("Goodbye".encode())
                break
            else:
                client_socket.send("Invalid command.".encode())

    except Exception as e:
        print(f"Error handling client {client_id}: {str(e)}")
    finally:
        # Remove the client from the list and close the socket.
        del clients[client_id]
        client_socket.close()

# Start listening for incoming connections.
server_socket.listen(5)
print(f"Server is listening on {host}:{port}")

while True:
    # Accept a new client connection.
    client_sock, client_addr = server_socket.accept()
    print(f"Accepted connection from {client_addr}")

    # Assign a unique ID to the client.
    client_id = client_id_counter
    clients[client_id] = client_sock

    # Start a new thread to handle the client.
    client_thread = threading.Thread(target=handle_client, args=(client_sock, client_id))
    client_thread.start()

    # Increment the client ID counter for the next client.
    client_id_counter += 1
