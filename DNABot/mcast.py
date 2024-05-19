"""
    Multicast group protocol for bots and supervisors

    Basic unreliable multicast for now - since I'm running my tests
    on localhost, not a problem.
    The Plan is to add NACK based reliability in a future version.

    17 May: Something is Wrong. Bots can send to the group address without
    problem, but they/the supervisor can't read anything. Not sure what
    I'm doing wrong :-(

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
        self.createSocket()
        log.info("Connected to group channel {}:{} as {}".format(self.address, self.receivePort, self.sender))

    def createSocket(self):
        """Multicast socket for sending and receiving"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # For listening
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.address, self.receivePort))
        addr = socket.inet_aton(self.address)
        optVal = struct.pack('4sL', addr, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, optVal)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        # For sending
        #self.sock.connect((self.address, self.receivePort))

    def close(self):
        """Close channel"""
        addr = socket.inet_aton(self.address)
        optVal = struct.pack('4sL', addr, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, optVal)
        self.sock.close()
        log.debug("Closed group channel")

    ##

    def write(self, message):
        """Prefix with sender and sequence number, send"""
        msg = "{} {} ".format(self.sender, self.seqNo) + message
        self.sock.sendto(msg.encode('UTF-8'), (self.address, self.receivePort))
        self.seqNo += 1

    def read(self):
        """Return next message including header"""
        try:
            msg = self.sock.recv(config.MAX_PACKET)
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
