"""
    Upload files or whatever from bot to supervisor
"""

import socket
import logging as log

from . import config


def handleRequest(msg):
    """Respond to UPLD message"""
    log.debug("Respond to UPLD...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Don't risk hanging around too long
    sock.settimeout(1.0)
    try:
        destAddr = msg.addrSender[0]
        sock.connect((destAddr, config.filePort))
        log.debug("Bot upload connection to {} {}".format(sock.getpeername()[0], sock.getpeername()[1]))
        sock.close()
    except (socket.timeout, TimeoutError):
        log.warning("Upload socket timed out")
    except OSError as e:
        log.warning("Upload socket exception: {} {}".format(type(e).__name__, e.args))
    log.debug("...end UPLD")
