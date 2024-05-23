
"""
    Watch all the bot traffic for the supervisor
"""

import logging as log

from DNABot import config, mcast

from . import supervisor

def listener(channel):
    """Listen to bot activity"""
    nextReport = supervisor.clock() + config.heartbeat
    while True:
        msg = channel.read()
        now = supervisor.clock()
        if msg is not None:
            print(msg)
            nextReport = now + config.heartbeat
        elif now > nextReport:
            print("Waiting...")
            nextReport = now + config.heartbeat
