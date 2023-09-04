from twisted.internet import reactor, protocol

class Server(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class ServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Server()

class Client(protocol.Protocol):
    def connectionMade(self):
        for i in range(1000000):
            self.sendMessage(f"Message {i+1}\n".encode())

        # self.transport.loseConnection()

    def sendMessage(self, message):
        self.transport.write(message)

class ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Client()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

reactor.connectTCP('127.0.0.1', 3000, ClientFactory())

reactor.listenTCP(3002, ServerFactory())
reactor.run()

# sendMessages()
