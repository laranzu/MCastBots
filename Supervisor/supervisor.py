
"""
    Main program for bot supervisor, ASD technical challenge program.

    Shares configuration and multicast code with DNABot.

    Hugh/Hugo Fisher AKA laranzu
    Canberra, Australia
    hugo.fisher@gmail.com
"""

import time
import random as RNG
import logging as log

from DNABot import config, mcast


global channel


##

def clock():
    """Whatever the system relative clock is"""
    return time.monotonic()


def listener(channel):
    """Listen to bot activity"""
    #channel.sock.settimeout(1.0)
    while True:
        msg = channel.read()
        if msg is not None:
            print(msg)

##

def initLogging(args):
    """My preferred logging setup"""
    # CLI can override default log level
    logLevel = log.WARNING
    if "-debug" in args:
        logLevel = log.DEBUG
    elif "-info" in args:
        logLevel = log.INFO;
    #
    params = {
        'format':   "%(levelname)s %(message)s",
        'datefmt':  "%H:%M:%S",
        'level':    logLevel,
    }
    # This is foreground app, log to console
    # params["filename"] = "./supervisor.log"
    log.basicConfig(**params)

def initSupervisor(args):
    """One time startup"""
    global channel
    # 
    RNG.seed(time.perf_counter())
    # Connect to channel
    channel = mcast.BasicChannel(config.groupAddress, config.groupPort, "HUMAN")


def main(args):
    """Run supervisor"""
    initLogging(args)
    config.init(args)
    initSupervisor(args)
    #
    # TODO start threads
    listener(channel)
