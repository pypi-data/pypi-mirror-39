from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
import sys

class Echo(Protocol):
    def dataReceived(self, data):
        print('Client data received: {}'.format(data.decode()))
        reactor.callLater(1.0, self.send_message)

    def send_message(self):
        self.transport.write('Hello server, I am the client'.encode())

    def connectionMade(self):
        self.transport.write('Hello server, I am the client'.encode())
        # self.transport.loseConnection()

class EchoClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        return Echo()

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)


reactor.connectTCP('localhost', int(sys.argv[1]), EchoClientFactory())
reactor.run()
