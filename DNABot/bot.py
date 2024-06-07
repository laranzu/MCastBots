
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

from . import config, mcast, receiver, upload


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

def handleCollision(msg):
    """Group name collision detected"""
    global botName, channel
    #
    log.debug("Name collision for {} from {}".format(botName, msg.addrSender))
    # Just rename ourself
    botName = newName()
    channel.rename(botName)

##


# Heartbeat has two timers. Control timer is fixed interval from
# program start time, next timer is control - small random value
# so we always send something a bit ahead of schedule

def nextHeartBeat(t):
    """Return updated control, next times from t"""
    beatControl = t + config.heartbeat
    nextBeat = beatControl - RNG.random() * 2
    return beatControl, nextBeat


##


def sendPing(msg):
    """Respond to ping request with heartbeat"""
    # If wildcard, wait random time to avoid congesting channel
    if msg.dest == "*":
        time.sleep(RNG.random() * config.backoff)
    log.debug("Respond to {}".format(msg))
    msg = "BEAT * Beep"
    channel.send(msg)
    # TODO could update beat timers to wait heartbeat from now


def handleMessage(msg):
    """Respond (if needed) to incoming channel messages"""
    if msg.sender == botName:
        handleCollision(msg)
        # And keep going, respond as usual
    # We see everything, only care about messages to us or wildcard
    if msg.dest != botName and msg.dest != "*":
        return
    # What to do?
    if msg.opcode == "PING":
        sendPing(msg)
    elif msg.opcode == "UPLD":
        # Can get complicated so in own module
        upload.handleRequest(msg, botName)
    elif msg.opcode not in ("BEAT",):
        log.debug("No handler for {} : {}".format(msg.opcode, msg))


##


def doResearch(delta):
    """If bot discovers something, update file and return true"""
    if RNG.random() > config.discovery * delta:
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
    wait = RNG.random() * config.backoff
    log.debug("Delay start by {:4.2f}".format(wait))
    time.sleep(wait)
    #
    try:
        now = clock()
        finish = now + config.lifespan
        beatControl = now
        nextBeat = now
        prev = now
        while True:
            time.sleep(1)
            # Incoming messages?
            n = msgBuffer.qsize() # Don't handle messages that arrive while we're handling
            for i in range(0, n):
                msg = msgBuffer.get()
                handleMessage(msg)
            # How much time has passed since last cycle?
            now = clock()
            delta = now - prev
            # Research?
            if doResearch(delta):
                # Notify everybody
                msg = "NEWS * Discovery"
                channel.send(msg)
                log.info("Bot {} has discovered something".format(botName))
                # And no need for heartbeat
                beatControl, nextBeat = nextHeartBeat(beatControl)
            # Timers gone off?
            if now > finish:
                break
            if now > nextBeat:
                beatControl, nextBeat = nextHeartBeat(beatControl)
                msg = "BEAT * Beep"
                channel.send(msg)
                log.debug("{} {}".format(botName, msg))
            # ready for next
            prev = now
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
