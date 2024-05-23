
"""
    Watch all the bot traffic for the supervisor
"""

import threading, time
import logging as log

from DNABot import config, mcast

from . import supervisor

class Listener(threading.Thread):
    """Listen to all the bot traffic and print to output stream"""

    def __init__(self, channel, output):
        """Create listener for multicast channel, print to output stream"""
        super().__init__()
        self.channel = channel
        self.output  = output
        # Use to end thread
        self.running = True

    def run(self):
        """Listen to bot activity"""
        nextReport = supervisor.clock() + config.heartbeat
        while self.running:
            msg = self.channel.read()
            now = supervisor.clock()
            if msg is not None:
                self.output.write(msg + "\n")
                nextReport = now + config.heartbeat
            elif now > nextReport:
                self.output.write("Channel is quiet...\n")
                nextReport = now + config.heartbeat
        log.info("End listener")
