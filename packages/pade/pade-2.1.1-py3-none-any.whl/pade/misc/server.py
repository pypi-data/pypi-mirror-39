import sys
from twisted.internet import protocol, reactor, endpoints

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        print('Server data received: {}'.format(data.decode()))
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

endpoints.serverFromString(reactor, 'tcp:{}'.format(sys.argv[1])).listen(EchoFactory())
reactor.run()
