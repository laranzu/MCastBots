
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


# Global state: multicast group and a couple of threads

channel = None
listener = None


##

def clock():
    """Whatever the system relative clock is"""
    return time.monotonic()


##

def execCommand(cmd):
    """Do some checks and send the command over network"""
    log.debug("Supervisor command {}".format(cmd))
    print("EXEC", cmd)

def commandLoop():
    """Read and execute commands from console"""
    log.debug("Start command loop")
    try:
        while True:
            command = input()
            # Enter by itself pauses / resumes output from capture thread
            if len(command) == 0:
                listener.paused = not listener.paused
                log.debug("Listener paused: {}".format(listener.paused))
            else:
                execCommand(command)
    except (KeyboardInterrupt, EOFError):
        pass
    log.debug("Command loop end")

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
    global channel, listener
    #
    initLogging(args)
    config.init(args)
    initSupervisor(args)
    #
    listener = capture.Listener(channel, sys.stdout)
    listener.start()
    commandLoop()
    #
    listener.running = False
    listener.join()
    log.info("Supervisor shutdown")
