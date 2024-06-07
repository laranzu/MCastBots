"""
    Upload files or whatever from bot to supervisor
"""

import ipaddress, os, socket, time
from os import path
import random as RNG
import logging as log

from . import config


def sendLine(sock, txt):
    """Write encoded string with linefeed"""
    txt += "\n"
    sock.send(txt.encode('UTF-8'))


def handleRequest(msg, myName):
    """Respond to UPLD message"""
    if msg.args is None:
        log.warning("UPLD request without resource name, ignored")
        return
    # Don't all hit the server at once
    if msg.dest == "*":
        time.sleep(RNG.random() * config.backoff)
    log.debug("Respond to {}".format(msg))
    destAddr = ipaddress.ip_address(msg.addrSender[0])
    if destAddr.version == 6:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Don't risk hanging around too long
    sock.settimeout(1.0)
    try:
        sock.connect((destAddr.compressed, config.filePort))
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
        sendLine(sock, "404 No resource {}:{}".format(myName, resource))
        return
    if path.isfile(resource):
        # Get all the data now. Future version may upload files in parallel with
        # main thread, so this minimises chance of write to file while uploading
        try:
            f = open(resource, "rt")
        except OSError as e:
            log.warning("Error opening file: {} {}".format(type(e).__name__, e.args))
            sendLine(sock, "500 Cannot upload {}:{}".format(myName, resource))
            return
        data = f.readlines()
        f.close()
        # send
        log.debug("Sending file content")
        sendLine(sock, "200 {}:{}".format(myName, resource))
        for line in data:
            sendLine(sock, line.rstrip())
    elif path.isdir(resource):
        try:
            data = os.listdir(resource)
        except OSError as e:
            log.warning("Error listing directory: {} {}".format(type(e).__name__, e.args))
            sendLine(sock, "500 Cannot upload {}:{}".format(myName, resource))
            return
        data = sorted(data)
        log.debug("Sending dir list")
        sendLine(sock, "200 {}:{}".format(myName, resource))
        for line in data:
            sendLine(sock, line)
    else:
        sendLine(sock, "505 Cannot upload {}:{}".format(myName, resource))
