
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
lifespan = 30
# Max delay at start
startup = 5
# Bot needs to send at least one message over this many seconds
heartbeat = 10

# Multicast group address
groupAddress = "239.1.2.4"
# receive port
groupPort = 8421


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
        "groupAddress": groupAddress,
        "groupPort":    str(groupPort)
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
    for name in ("lifespan", "startup", "heartbeat", "groupPort"):
        globals()[name] = config.getint(name)
        log.debug("{} {}".format(name, globals()[name]))
    for name in ("groupAddress",):
        globals()[name] = config.get(name)
        log.debug("{} {}".format(name, globals()[name]))

