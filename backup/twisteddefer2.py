from twisted.internet import reactor, threads
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.defer import DeferredQueue

class MessageSender(Protocol):
    def __init__(self, queue):
        self.queue = queue

    def connectionMade(self):
        self.sendNextMessage()

    def sendNextMessage(self):
        while not self.queue.isEmpty():
            message = self.queue.get()
            self.transport.write(message)
            self.sendNextMessage()
        self.transport.loseConnection()
    def doStart(self):
        # Code to be executed when the service starts
        print("Service started")

    def startedConnecting(self, foob):
        print("started connecting")

class MessageProducer:
    def __init__(self, queue):
        self.queue = queue

    def produceMessages(self):
        # Generate or fetch messages to be sent
        messages = ["Message 1", "Message 2", "Message 3"]

        for message in messages:
            self.queue.put(message)

def startClient():
    queue = DeferredQueue()
    producer = MessageProducer(queue)
    sender = MessageSender(queue)

    # Start the message producer in a separate thread
    threads.deferToThread(producer.produceMessages)

    # Connect the message sender to the server
    reactor.connectTCP("127.0.0.1", 3000, sender)

    # Start the Twisted reactor
    reactor.run()

startClient()
