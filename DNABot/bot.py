
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

import hashlib, time
import random as RNG
import logging as log

from . import config


# To avoid timezones, leap seconds, daylight saving, ... all bots
# use a relative clock. Messages will have intervals, not absolute
# times, so bots don't have to be synchronised.

def clock():
    """Whatever the system relative clock is"""
    return time.monotonic()


# Bots need some kind of unique identifier on messages, and I want
# them to be self configuring. Can't be based on IP address because
# I'm testing on a single computer.

def newName():
    """Create random 8 hex digit identifier for bot"""
    n = RNG.randint(1, 65535)
    digest = hashlib.new("md5")
    data32 = bytes([
            (n >> 24) & 0x0FF,
            (n >> 16) & 0x0FF,
            (n >> 8) & 0x0FF,
            (n & 0x0FF)])
    digest.update(data32)
    # Finish calculation (pad, etc)
    name = digest.hexdigest()
    # Did you know the top 32 bits of the MD5 hashes for 16 bit
    # integers don't collide? Now you do.
    name = name[0:8]
    # And uppercase to be more robotic
    name = name.upper()
    return name


##

def mainLoop():
    """Run bot for lifespan seconds"""
    # Need unique identifier for network messages.
    botName = newName()
    log.info("Bot {} activated".format(botName))
    # Don't want all bots starting at once
    wait = RNG.random() * 5
    log.debug("Delay start by {:4.2f}".format(wait))
    time.sleep(wait)
    #
    finish = clock() + config.lifespan
    while True:
        time.sleep(1)
        print("{} Beep".format(botName))
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

def initBot(args):
    """One time startup"""
    # Don't need cryptographic quality truly random numbers,
    # but bots must not be in lockstep eg for name generation
    RNG.seed(time.perf_counter())

def boot(args):
    """Run DNABot"""
    initLogging(args)
    initBot(args)
    config.init(args)
    mainLoop()
