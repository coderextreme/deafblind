#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver


class EchoClient(LineReceiver):
    end = b"Bye-bye!"
    count = 0

    def connectionMade(self):
        self.sendLine(b"1000000")
        # self.sendLine(self.end)

    def lineReceived(self, line):
        self.count += 1
        print(f"receive: {self.count}, {line}")
        if line == self.end:
            self.transport.loseConnection()


class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print("connection failed:", reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print("connection lost:", reason.getErrorMessage())
        self.done.callback(None)


def main(reactor):
    factory = EchoClientFactory()
    reactor.connectTCP("localhost", 1234, factory)
    return factory.done


if __name__ == "__main__":
    task.react(main)
