
"""
    Watch all the bot traffic for the supervisor
"""

import threading, time
import logging as log

from DNABot import config, mcast

from . import supervisor

# Number of heartbeat intervals between activity checks
INTERVALS = 2

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
        # Tracking activity on channel
        self.nMsgs = 0

    def handleMessage(self, msg, sender):
        """Print or store incoming messages"""
        self.nMsgs += 1
        if self.paused:
            self.store.append(msg)
        else:
            self.output.write(msg + "\n")

    def reportActive(self):
        """Check how many bots have joined or left"""
        if self.nMsgs == 0:
            self.output.write("Channel is quiet...\n")
        self.nMsgs = 0

    def run(self):
        """Listen to bot activity"""
        log.debug("Start bot traffic watcher")
        nextReport = supervisor.clock() + config.heartbeat * INTERVALS
        while self.running:
            # Resume after pause?
            while len(self.store) > 0 and not self.paused:
                msg = self.store.pop(0);
                self.output.write(msg + "\n")
            # New messages?
            msg, sender = self.channel.recv()
            now = supervisor.clock()
            if msg is not None:
                self.handleMessage(msg, sender)
            # Regular check?
            if now > nextReport and not self.paused:
                self.reportActive()
                nextReport += config.heartbeat * INTERVALS
        log.info("End bot traffic watcher")
