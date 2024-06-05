"""
    Multicast group protocol for bots and supervisors.
    Not a channel in the CSP sense, I just watch a lot of science fiction.

    Basic unreliable multicast for now - since I'm running my tests
    on localhost, not a problem.
    The Plan is to add NACK based reliability in a future version.

    Only one thread should send, only one thread should receive.

    See protocol.md for description of packets
"""

import ipaddress, socket, struct
import logging as log

from . import config


class BasicChannel(object):
    """Multicast group communication channel"""

    def __init__(self, IPaddress, portNumber, senderID):
        """Create and connect new socket for group address"""
        self.address = ipaddress.ip_address(IPaddress)
        self.destPort = portNumber
        self.sender = senderID
        self.seqNo = 1
        self.createSockets()
        log.info("Connected to group channel {} : {} as {}".format(self.address, self.destPort, self.sender))

    def createSockets(self):
        """Input and output sockets for group channel"""
        # For listening
        log.debug("Create input socket for {} : {}".format(self.address, self.destPort))
        if self.address.version == 6:
            family = socket.AF_INET6
        else:
            family = socket.AF_INET
        self.input = socket.socket(family, socket.SOCK_DGRAM)
        self.input.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.input.bind((self.address.compressed, self.destPort))
        self.input.settimeout(1.0)
        # Although designed for multicast, can use localhost for testing
        if self.address.is_multicast:
            log.debug("Add membership for {}".format(self.address))
            if self.address.version == 6:
                ipv6_mreq = struct.pack('!16sI', self.address.packed, 0)
                self.input.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, ipv6_mreq)
            else:
                ip_mreqn = struct.pack('!4sIH', self.address.packed, socket.INADDR_ANY, 0)
                self.input.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, ip_mreqn)
        # For sending
        log.debug("Create output socket for {} : {}".format(self.address, self.destPort))
        self.output = socket.socket(family, socket.SOCK_DGRAM)
        self.output.connect((self.address.compressed, self.destPort))
        log.debug("BasicChannel sockets created")

    def close(self):
        """Close channel"""
        if self.address.is_multicast:
            if self.address.version == 6:
                ipv6_mreq = struct.pack('!16sI', self.address.packed, 0)
                self.input.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_LEAVE_GROUP, ipv6_mreq)
            else:
                ip_mreqn = struct.pack('!4sIH', self.address.packed, socket.INADDR_ANY, 0)
                self.input.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, ip_mreqn)
        self.input.close()
        self.output.close()
        log.debug("Closed channel")

    ##

    def send(self, message):
        """Prefix with sender and sequence number, send"""
        msg = "{} {} ".format(self.sender, self.seqNo) + message
        #self.output.sendto(msg.encode('UTF-8'), (self.address, self.destPort))
        self.output.send(msg.encode('UTF-8'))
        self.seqNo += 1

    def recv(self):
        """Return next message including header, sender IP"""
        try:
            msg, src = self.input.recvfrom(config.PKT_SIZE)
            if msg is not None:
                msg = msg.decode('utf-8', 'backslashreplace')
        except (socket.timeout, TimeoutError):
            msg = None
            src = None
        return msg, src

    ##

    def rename(self, newSender):
        """Bot can change sender ID"""
        log.debug("Change sender ID from {} to {}".format(self.sender, newSender))
        self.sender = newSender
