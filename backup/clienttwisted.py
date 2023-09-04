from twisted.internet import reactor, protocol

class MyClient(protocol.Protocol):
    def connectionMade(self):
        self.send_message("Hello, server!")

    def send_message(self, message):
        self.transport.write(message.encode())

    def dataReceived(self, data):
        print("Received:", data.decode())

class MyClientFactory(protocol.ClientFactory):
    protocol = MyClient

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()

def send_message_to_server(message):
    factory = MyClientFactory()
    reactor.connectTCP('127.0.0.1', 3000, factory)
    factory.protocol.send_message(message)

# Example usage
while True:
    send_message_to_server("Hello, server!")
    send_message_to_server("How are you?")
    send_message_to_server("Goodbye!")

reactor.run()
