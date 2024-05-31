
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

import hashlib, queue, time
import random as RNG
import logging as log

from . import config, mcast, receiver


# Global state which isn't in config
botName     = None
channel     = None
msgBuffer   = None

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
    """Create random hex digit identifier for bot"""
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


# Heartbeat has two timers. Control timer is fixed interval from
# program start time, next timer is control - small random value
# so we always send something a bit ahead of schedule

def nextHeartBeat(t):
    """Return updated control, next times from t"""
    beatControl = t + config.heartbeat
    nextBeat = beatControl - RNG.random() * 2
    return beatControl, nextBeat


def handleMessage(msg, sender):
    """Respond (if needed) to incoming channel messages"""
    log.debug("Message {} from {}".format(msg, sender))

def doResearch():
    """If bot discovers something, update file and return true"""
    if RNG.random() > config.discovery:
        return False
    products = (
        "Bouncy Bubbly Beverage additive",
        "Cherenkov cellular damage lotion",
        "Plastic eating algae",
        "Soup decontaminant",
        "Synthetic probiotic supplement",
        )
    result = RNG.choice(products)
    # Append to file
    f = open(config.results, "at")
    f.write(result + "\n")
    f.close()
    # Main program sends packet
    return True


def mainLoop():
    """Run bot for lifespan seconds"""
    log.info("Bot {} activated".format(botName))
    # Don't want all bots starting at once
    wait = RNG.random() * config.startup
    log.debug("Delay start by {:4.2f}".format(wait))
    time.sleep(wait)
    #
    try:
        now = clock()
        finish = now + config.lifespan
        beatControl = now
        nextBeat = now
        while True:
            time.sleep(1)
            # Incoming messages?
            n = msgBuffer.qsize() # Don't handle messages that arrive while we're handling
            for i in range(0, n):
                msg, sender = msgBuffer.get()
                handleMessage(msg, sender)
            # Research?
            if doResearch():
                # Notify everybody
                msg = "NEWS * Discovery"
                channel.send(msg)
                log.info("{} {}".format(botName, msg))
                # And no need for heartbeat
                beatControl, nextBeat = nextHeartBeat(beatControl)
            # Timers gone off?
            now = clock()
            if now > finish:
                break
            if now > nextBeat:
                beatControl, nextBeat = nextHeartBeat(beatControl)
                msg = "BEAT * Beep"
                channel.send(msg)
                log.debug("{} {}".format(botName, msg))
        log.info("Lifespan reached")
    except (KeyboardInterrupt, ) as e:
        log.warning("Bot end on exception {}".format(type(e).__name__))
    channel.close()

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
    global botName, channel, msgBuffer
    log.debug("initBot")
    # Don't need cryptographic quality truly random numbers,
    # but bots must not be in lockstep eg for name generation
    RNG.seed(time.perf_counter())
    # Need unique identifier for network messages.
    botName = newName()
    # Now connect to channel
    channel = mcast.BasicChannel(config.chanAddr, config.chanPort, botName)
    # Init results file
    f = open(config.results, "wt")
    f.close()
    # Init message queue
    msgBuffer = queue.Queue(config.QUEUE_SIZE)


def boot(args):
    """Run DNABot"""
    initLogging(args)
    config.init(args)
    initBot(args)
    # Thread for incoming
    chat = receiver.BotReceiver(channel, msgBuffer)
    chat.start()
    # and run until stopped by something
    mainLoop()
    chat.running = False
    chat.join()
    log.info("Bot end program")
