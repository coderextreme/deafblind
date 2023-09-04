from twisted.internet import reactor, protocol

class MessageSender(protocol.Protocol):
    def connectionMade(self):
        for i in range(1000000):
            self.sendMessage(f"Message {i+1}\n".encode())

        # self.transport.loseConnection()

    def sendMessage(self, message):
        self.transport.write(message)

class MessageSenderFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return MessageSender()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

def sendMessages():
    reactor.connectTCP('127.0.0.1', 3000, MessageSenderFactory())
    reactor.run()

sendMessages()
