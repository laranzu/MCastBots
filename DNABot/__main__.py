
"""
    Main program for DNABot, ASD technical challenge program.

    Hugh/Hugo Fisher AKA laranzu
    Canberra, Australia
    hugo.fisher@gmail.com

    CLI args
        -debug          Logging level
        -info           Logging level
"""

import sys
import logging as log

from . import config

def initLogging(args):
    """My preferred logging setup"""
    logLevel = log.WARNING
    if "-debug" in args:
        logLevel = log.DEBUG
    elif "-info" in args:
        logLevel = log.INFO;
    params = {
        'format':   "%(levelname)s %(message)s",
        'datefmt':  "%H:%M:%S",
        'level':    logLevel,
    }
    if "-fg" not in args:
        params["filename"] = "./dnabot.log"
    log.basicConfig(**params)


def main(args):
    """Main control for DNABot"""
    initLogging(args)
    config.load()
    log.debug("debug?")
    log.info("info?")
    log.warning("warn?")
    print("Hello world")

if __name__ == "__main__":
    main(sys.argv)
