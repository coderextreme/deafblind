import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    #def handle(self):
    #    self.messages = self.request.recv(1024).decode();
    #    if self.messages:
    #        print("{} wrote:".format(self.client_address[0]))
    #        print(self.messages)
    def handle(self):
        MSGLEN = 1024
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.request.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            print(b''.join(chunks))
            #print("{} wrote:".format(self.request.client_address[0]))
        return b''.join(chunks)

if __name__ == "__main__":
    HOST, PORT = "localhost", 3000
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
