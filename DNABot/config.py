
"""
    Configuration loading and reloading for DNABot.

    Standard dnabot.ini file with one section
    [DNABot]
"""

import logging as log
from configparser import ConfigParser

SECTION = "DNABot"

##  All these can be set by config file

# Time to run, in seconds
lifespan = 30

# Max delay at start
startup = 5


def init(cliArgs):
    """Initial load from file and CLI args"""
    global lifespan, startup
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
    lifespan = config.getint("lifespan")
    startup = config.getint("startup")
    #
    log.debug("lifespan {}".format(lifespan))
    log.debug("startup {}".format(startup))

