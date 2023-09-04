import socket

# from Shell-GPT

def send_message(message):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    server_address = ('localhost', 3000)  # Replace with your server address
    sock.connect(server_address)
    try:
        # Send the message
        sock.sendall(message.encode())
        # Wait for the server to acknowledge the message
        # wee don't need a response, thanks
        #response = sock.recv(1024)
        #print(f"Received: {response.decode()}")
    finally:
        # Close the socket
        sock.close()
# Send 1000000 messages
for i in range(1000000):
    message = f"Message {i+1}"
    print(message)
    send_message(message)
