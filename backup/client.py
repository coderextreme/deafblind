import socket
import struct

sock = None

#def msgSend(sock, data):
#    if data:
#        retval = sock.sendall(data.encode())
#        print(retval)

def msgSend(sock, data):
    totalsent = 0
    newmsg = data.encode()
    MSGLEN = len(newmsg)
    while totalsent < MSGLEN:
        sent = sock.send(newmsg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

def socketCreate():
    HOST, PORT = "localhost", 3000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    sock.connect((HOST, PORT))
    return sock


# Create a socket (SOCK_STREAM means a TCP socket)
if __name__ == '__main__':
    sock = socketCreate()
    for i in range(1,2001):
        print(f"Connection {i}:");
        # sock = socketCreate()
        msgSend(sock, "DUCK\n")
        msgSend(sock, "GOOSE\n")
        msgSend(sock, "RAVEN\n")
        msgSend(sock, "EAGLE\n")
        msgSend(sock, "CHICKEN\n")
        msgSend(sock, "CROW\n")
        msgSend(sock, "EOF\n")
data = "EOF\n"
sockendall(struct.pack("L", len(data))+data)
sock.shutdown(socket.SHUT_RDWR)
sock.close()
