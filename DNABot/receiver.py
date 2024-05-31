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
                log.debug("Received {}".format(msg))
                try:
                    self.buffer.put((msg, sender), block=False)
                except queue.Full:
                    log.warning("Receiver queue full, drop message")
            except OSError:
                break
        log.info("End bot receiver")
