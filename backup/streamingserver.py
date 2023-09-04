import socket

# from Shell-GPT

def start_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 3000)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print('Server listening on {}:{}'.format(*server_address))

    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Connected to client:', client_address)

    # Receive and process messages from the client
    message_count = 0
    while message_count < 1000000:
        message = client_socket.recv(1024).decode()
        print('Received message:', message_count, message)
        message_count += 1

    # Close the connection
    client_socket.close()
    server_socket.close()

# Start the server
start_server()
