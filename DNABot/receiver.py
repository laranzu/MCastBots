"""
    Incoming message thread for bot.
    Does not process messages, just queues for main loop
"""

import socket, threading, time
import logging as log

from . import config, mcast

class BotReceiver(threading.Thread):
    """Queue up incoming messages for bot"""

    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        # Use to end thread
        self.running = True

    def run(self):
        log.debug("Start bot receive")
        while self.running:
            # New messages?
            try:
                msg, sender = self.channel.recv()
                if msg is not None:
                    log.debug("Received {}".format(msg))
            except OSError:
                break
        log.info("End bot receiver")
