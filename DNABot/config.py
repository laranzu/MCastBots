
"""
    Configuration loading and reloading for DNABot.

    Standard dnabot.ini file with one section
    [DNABot]
"""

import logging as log
from configparser import ConfigParser

SECTION = "DNABot"

##  All these can be set by config file or command line.
##  Need to add each at two places in code below

# Time to run, in seconds
lifespan = 120
# Backoff range for random delay on startup, group pings, etc.
backoff = 5
# Bot needs to send at least one message over this many seconds
heartbeat = 10

# Bot output file (not log)
results = "results.data"
# Probability that bot will discover something per second
discovery = 0.01


# Probability that bot will go Frankenstein, per second
frankenstein = 0.001
# Increase probability whenever human supervisor kills a bot
killBoost = 0.01


# Multicast channel for group communication
chanAddr = "239.1.2.4"
#chanAddr = "ff05::ef:1:2:4"
# receive port
chanPort = 8421
# Optional interface identified by IP address
chanIface = ""
# Maximum expected packet size
PKT_SIZE = 1024

# Limit on stored but not processed incoming messages
QUEUE_SIZE = 512

# File uploads are TCP to this port on supervisor
filePort = 8000


##

def init(cliArgs):
    """Initial load from file and CLI args"""
    #
    config = ConfigParser()
    # Config file can be changed by CLI
    fileName = "./dnabot.ini"
    try:
        idx = cliArgs.index("-config")
        if idx >= 0 and idx < len(cliArgs) - 1:
            fileName = cliArgs[idx + 1]
    except ValueError:
        pass
    # Default values
    hardWired = {
        "lifespan":     str(lifespan),
        "backoff":      str(backoff),
        "heartbeat":    str(heartbeat),
        "results":      results,
        "discovery":    str(discovery),
        "frankenstein": str(frankenstein),
        "killBoost":    str(killBoost),
        "chanAddr":     chanAddr,
        "chanPort":     str(chanPort),
        "chanIface":    chanIface,
        "PKT_SIZE":     str(PKT_SIZE),
        "QUEUE_SIZE":   str(QUEUE_SIZE),
        "filePort":     str(filePort),
    }
    config['DNABot'] = hardWired
    # Read from file, if exists
    log.debug("Try reading config file {}".format(fileName))
    config.read(fileName)
    # We only care about one section
    config = config['DNABot']
    # CLI args override config file. Must be format -key=value
    for arg in cliArgs:
        if arg.startswith("-"):
            try:
                arg = arg.split("=")
                key = arg[0][1:]
                val = arg[1]
                if key in config:
                    config[key] = val
                    log.debug("CLI config override {}={}".format(key, val))
            except IndexError:
                pass
    # OK, set global values
    # Need to convert from config string to appropriate types
    for name in ("lifespan", "backoff", "heartbeat", "chanPort", "PKT_SIZE", "QUEUE_SIZE", "filePort"):
        globals()[name] = config.getint(name)
        log.debug("{} {}".format(name, globals()[name]))
    for name in ("results", "chanAddr", "chanIface"):
        # Remove quotes, since I keep making this mistake
        s  = config.get(name).strip("\"\'")
        # Special case empty string
        if s:
            globals()[name] = s
        else:
            globals()[name] = None
        log.debug("{} {}".format(name, globals()[name]))
    for name in ("discovery", "frankenstein", "killBoost",):
        globals()[name] = config.getfloat(name)
        log.debug("{} {}".format(name, globals()[name]))

