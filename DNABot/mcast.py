"""
    Multicast group protocol for bots and supervisors

    Basic unreliable multicast for now - since I'm running my tests
    on localhost, not a problem.
    The Plan is to add NACK based reliability in a future version.

    See protocol.md for description of packets
"""

import socket, struct
import logging as log

from . import config


class BasicChannel(object):
    """Multicast group communication channel"""

    def __init__(self, IPaddress, portNumber, senderID):
        """Create and connect new socket for group address"""
        self.address = IPaddress
        self.receivePort = portNumber
        self.sender = senderID
        self.seqNo = 1
        self.createSockets()
        log.info("Connected to group channel {}:{} as {}".format(self.address, self.receivePort, self.sender))

    def createSockets(self):
        """Need one socket for send, one for receive"""
        # For listening
        self.input = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.input.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.input.bind(("0.0.0.0", self.receivePort))
        self.input.bind((self.address, self.receivePort))
        binAddr = socket.inet_aton(self.address)
        mreqn = struct.pack('!4BIH', *binAddr, socket.INADDR_ANY, 0)
        self.input.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreqn)
        log.debug("BasicChannel input socket created")
        # For sending
        self.output = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.output.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.output.connect((self.address, self.receivePort))
        log.debug("BasicChannel output socket created")

    def close(self):
        """Close channel"""
        binAddr = socket.inet_aton(self.address)
        mreqn = struct.pack('!4BIH', *binAddr, socket.INADDR_ANY, 0)
        self.input.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreqn)
        self.input.close()
        self.output.close()
        log.debug("Closed group channel")

    ##

    def write(self, message):
        """Prefix with sender and sequence number, send"""
        msg = "{} {} ".format(self.sender, self.seqNo) + message
        #self.output.sendto(msg.encode('UTF-8'), (self.address, self.receivePort))
        self.output.send(msg.encode('UTF-8'))
        self.seqNo += 1

    def read(self):
        """Return next message including header"""
        try:
            msg = self.input.recv(config.MAX_PACKET)
            if msg is not None:
                msg = msg.decode('utf-8', 'backslashreplace')
        except socket.timeout:
            msg = None
        return msg

    ##

    def rename(self, newSender):
        """Bot can change sender ID"""
        log.debug("Change sender ID from {} to {}".format(self.sender, newSender))
        self.sender = newSender
