
"""
    Main program for bot supervisor, ASD technical challenge program.

    Shares configuration and multicast code with DNABot.

    Hugh/Hugo Fisher AKA laranzu
    Canberra, Australia
    hugo.fisher@gmail.com
"""

import sys, threading, time
import random as RNG
import logging as log

from DNABot import config, mcast

from . import capture

global channel


##

def clock():
    """Whatever the system relative clock is"""
    return time.monotonic()


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
    channel = mcast.BasicChannel(config.chanAddr, config.chanPort, "HUMAN")


def main(args):
    """Run supervisor"""
    try:
        initLogging(args)
        config.init(args)
        initSupervisor(args)
        #
        listener = capture.Listener(channel, sys.stdout)
        listener.start()
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("Stopping")
        listener.running = False
    listener.join()
