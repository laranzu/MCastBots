
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
lifespan = 60
# Max delay at start
startup = 5
# Bot needs to send at least one message over this many seconds
heartbeat = 10

# Bot output file (not log)
results = "results.data"
# Probability that bot will discover something per attempt
discovery = 0.01

# Multicast channel for group communication
# Expected to be multicast, but 127.0.0.1 works for testing
#chanAddr = "239.1.2.4"
chanAddr = "127.0.0.1"
# receive port
chanPort = 8421
# Maximum expected packet size
MAX_PACKET = 1024

# File uploads are TCP to this port
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
        "startup":      str(startup),
        "heartbeat":    str(heartbeat),
        "results":      results,
        "discovery":    str(discovery),
        "chanAddr":     chanAddr,
        "chanPort":     str(chanPort),
        "MAX_PACKET":   str(MAX_PACKET),
        "filePort":     str(filePort),
    }
    config['DNABot'] = hardWired
    # Read from file, if exists
    log.info("Try reading config file {}".format(fileName))
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
    for name in ("lifespan", "startup", "heartbeat", "chanPort", "MAX_PACKET", "filePort"):
        globals()[name] = config.getint(name)
        log.debug("{} {}".format(name, globals()[name]))
    for name in ("results", "chanAddr",):
        globals()[name] = config.get(name)
        log.debug("{} {}".format(name, globals()[name]))
    for name in ("discovery", ):
        globals()[name] = config.getfloat(name)
        log.debug("{} {}".format(name, globals()[name]))

