
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
        # Listener can be printing, or saving output until later
        self.paused = False
        self.store = [] # Only used within thread, doesn't need to be queue


    def run(self):
        """Listen to bot activity"""
        log.debug("Start bot traffic monitor thread")
        nextReport = supervisor.clock() + config.heartbeat * 2
        while self.running:
            # Resume after pause?
            while len(self.store) > 0 and not self.paused:
                msg = self.store.pop(0);
                self.output.write(msg + "\n")
            # New messages?
            msg = self.channel.read()
            now = supervisor.clock()
            if msg is not None:
                if self.paused:
                    self.store.append(msg)
                else:
                    self.output.write(msg + "\n")
                nextReport = now + config.heartbeat * 2
            # Nothing happening?
            elif now > nextReport and not self.paused:
                self.output.write("Channel is quiet...\n")
                nextReport = now + config.heartbeat
        log.info("End bot traffic monitor")
