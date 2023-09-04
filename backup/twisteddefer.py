from twisted.internet import reactor, threads
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
from twisted.python import log
from queue import Queue
class MessageSenderProtocol(Protocol):
   def __init__(self, message_queue):
       self.message_queue = message_queue

   def connectionMade(self):
       self.sendNextMessage()

   def sendNextMessage(self):
       while not self.message_queue.empty():
           message = self.message_queue.get()
           self.transport.write(message.encode())

   def connectionLost(self, reason):
       reactor.stop()

class MessageSenderFactory(ClientFactory):
   def __init__(self, message_queue):
       self.message_queue = message_queue

   def buildProtocol(self, addr):
       return MessageSenderProtocol(self.message_queue)

   def clientConnectionFailed(self, connector, reason):
       log.err(reason)
       reactor.stop()

def produceMessages(message_queue):
   # Your message production logic goes here
   # Example:
   for i in range(1000000):
       message = f"Message {i}\n"
       message_queue.put(message)

def startSending():
   message_queue = Queue()

   # Start the message producer thread
   producer_thread = threads.deferToThread(produceMessages, message_queue)

   # Start the message sender thread
   sender_factory = MessageSenderFactory(message_queue)
   reactor.connectTCP('127.0.0.1', 3000, sender_factory)

   # Start the reactor event loop
   reactor.run()
startSending()
