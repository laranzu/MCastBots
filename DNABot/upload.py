"""
    Upload files or whatever from bot to supervisor
"""

import os, socket
from os import path
import logging as log

from . import config


def handleRequest(msg, myName):
    """Respond to UPLD message"""
    if msg.args is None:
        log.warning("UPLD request without resource name, ignored")
        return
    log.debug("Respond to UPLD")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Don't risk hanging around too long
    sock.settimeout(1.0)
    try:
        destAddr = msg.addrSender[0]
        sock.connect((destAddr, config.filePort))
        log.debug("Bot upload connection to {} {}".format(sock.getpeername()[0], sock.getpeername()[1]))
        sendContent(sock, msg.args[0], myName)
        sock.close()
    except (socket.timeout, TimeoutError):
        log.warning("Upload socket timed out")
    except OSError as e:
        log.warning("Upload socket exception: {} {}".format(type(e).__name__, e.args))
    log.debug("End UPLD")


def sendContent(sock, resource, myName):
    """Upload content of named resource through socket"""
    if not path.exists(resource):
        sock.send("404 No resource {}://{}\r\n".format(myName, resource).encode('UTF-8'))
        return
    if path.isfile(resource):
        # Get all the data now. Future version may upload files in parallel with
        # main thread, so this minimises chance of write to file while uploading
        try:
            f = open(resource, "rt")
        except OSError as e:
            log.warning("Error opening file: {} {}".format(type(e).__name__, e.args))
            sock.send("500 Cannot upload {}://{}\r\n".format(myName, resource).encode('UTF-8'))
            return
        data = f.readlines()
        f.close()
        # send
        sock.send("200 {}://{}\r\n".format(myName, resource).encode('UTF-8'))
        for line in data:
            line += "\n"
            sock.send(line.encode('UTF-8'))
        sock.close()
    elif path.isdir(resource):
        pass
    else:
        sock.send("505 Cannot upload {}://{}\r\n".format(myName, resource).encode('UTF-8'))
