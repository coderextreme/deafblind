from twisted.internet import protocol, reactor

class MyProtocol(protocol.Protocol):
    def connectionMade(self):
        #self.transport.write(b"Welcome to the server!\n")
        pass

    def dataReceived(self, data):
        # Process the received data here
        print("Received data:", data.decode())

class MyFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return MyProtocol()

reactor.listenTCP(3000, MyFactory())
reactor.run()
