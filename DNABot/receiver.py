"""
    Incoming message thread for bot.
    Does not process messages, just queues for main loop
"""

import queue, socket, threading, time
import logging as log

from . import config, mcast

class BotReceiver(threading.Thread):
    """Queue up incoming messages for bot"""

    def __init__(self, channel, messageQueue):
        super().__init__()
        self.channel = channel
        self.buffer  = messageQueue
        # Use to end thread
        self.running = True

    def run(self):
        log.debug("Start bot receive")
        while self.running:
            # New messages?
            try:
                msg, sender = self.channel.recv()
                if msg is None:
                    continue # Timeout
                #log.debug("Received {}".format(msg))
                try:
                    parsed = ChanMessage(msg, sender)
                    self.buffer.put(parsed, block=False)
                except ValueError:
                    log.debug("Invalid format, drop message")
                except queue.Full:
                    log.warning("Receiver queue full, drop message")
            except OSError:
                break
        log.info("End bot receiver")


class ChanMessage(object):
    """Parsed channel message as record with named fields"""

    def __init__(self, message, ipAddr):
        """Create message, or raise ValueError if message not in right format"""
        self.addrSender = ipAddr
        # Try to parse
        fields = message.split()
        if len(fields) < 4:
            raise ValueError("Channel message must be sender sequenceNumber opcode destination ...")
        self.sender = fields[0]
        self.seqNo = int(fields[1]) # Will raise ValueError if not an int
        if self.seqNo < 0:
            raise ValueError("Channel message has negative sequence number")
        self.opcode = fields[2]
        self.dest = fields[3]
        if len(fields) > 4:
            self.args = fields[4:]
        else:
            self.args = None
        # Keep original string form
        self.text = message

    def __str__(self):
        return self.text
