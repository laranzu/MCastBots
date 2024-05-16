
"""
    Main program for DNABot, ASD technical challenge program.

    Hugh/Hugo Fisher AKA laranzu
    Canberra, Australia
    hugo.fisher@gmail.com

    This module is a singleton, not a class.

    CLI args
        -debug          Logging level
        -info           Logging level
        -fg             Output to console, not file
"""

import random, time
import logging as log

from . import config


# To avoid timezones, leap seconds, daylight saving, ... all bots
# use a relative clock. Messages will have intervals, not absolute
# times, so bots don't have to be synchronised.

def clock():
    """Whatever the system relative clock is"""
    return time.monotonic()


##

def mainLoop():
    """Run bot for lifespan seconds"""
    # Don't want all bots starting at once
    wait = random.random() * 5
    log.debug("Delay start by {:4.2f}".format(wait))
    time.sleep(wait)
    #
    finish = clock() + config.lifespan
    while True:
        time.sleep(1)
        print("Beep")
        if clock() > finish:
            break
    log.info("Lifespan reached")

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
    # Normally run as daemon and log to file, but
    # for testing can send log to console instead.
    if "-fg" not in args:
        params["filename"] = "./dnabot.log"
    log.basicConfig(**params)


def boot(args):
    """Run DNABot"""
    initLogging(args)
    config.init(args)
    mainLoop()
