
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
import builtins, gettext, pathlib

from DNABot import config, mcast

from . import capture, upload


# Global state: multicast group and a couple of threads

channel  = None
watcher  = None
receiver = None

##

def clock():
    """Whatever the system relative clock is"""
    return time.monotonic()


##

def execCommand(cmd):
    """Do some checks and send the command over network"""
    fields = cmd.split()
    if len(fields) < 2:
        log.warning(tr("Command does not have opcode and dest"))
    # Uppercase opcode
    fields[0] = fields[0].upper()
    # Fill in upload filename if not present
    if fields[0] == "UPLD" and len(fields) < 3:
        fields.append(config.results)
    # and send
    cmd = " ".join(fields)
    channel.send(cmd)
    log.debug("Supervisor command {}".format(cmd))

def commandLoop():
    """Read and execute commands from console"""
    log.debug("Start command loop")
    try:
        while True:
            command = input()
            # Enter by itself pauses / resumes output from capture thread
            if len(command) == 0:
                watcher.paused = not watcher.paused
                log.debug("Watcher paused: {}".format(watcher.paused))
                if watcher.paused:
                    print(tr("Command: OPCODE bot ..."))
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
    # Set up language translations, shared in parent
    progDir = pathlib.Path(__file__).parents[1]
    translator = gettext.translation("messages", localedir=pathlib.Path(progDir, "I18N"), fallback=True)
    builtins.__dict__["tr"] = translator.gettext
    # Connect to channel
    channel = mcast.BasicChannel(config.chanAddr, config.chanPort, "HUMAN")


def main(args):
    """Run supervisor"""
    global channel, watcher, receiver
    #
    initLogging(args)
    config.init(args)
    initSupervisor(args)
    # Threads
    watcher = capture.Listener(channel, sys.stdout)
    watcher.start()
    receiver = upload.UploadHandler(channel, sys.stdout)
    receiver.start()
    commandLoop()
    #
    watcher.running = False
    receiver.running = False
    watcher.join()
    receiver.join()
    log.info("Supervisor shutdown")
