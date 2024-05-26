"""
    Handle file uploads from bots for the supervisor
"""

import socket, threading, time
import logging as log

from DNABot import config, mcast

from . import supervisor

class UploadHandler(threading.Thread):
    """Handle incoming TCP uploads from bots"""

    def __init__(self):
        """Listen for TCP upload connections, print to output stream"""
        super().__init__()
        # Use to end thread
        self.running = True
        self.sock = None


    def run(self):
        """TCP server"""
        log.debug("Start upload handler")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", config.filePort))
        self.sock.listen(5)
        self.sock.settimeout(2.0)
        log.info("File uploads to {} : {}".format(self.sock.getsockname()[0],
                                        self.sock.getsockname()[1]))
        while self.running:
            try:
                client, clientAddr = self.sock.accept()
            except (socket.timeout, TimeoutError):
                continue
            except OSError as e:
                log.warning("Upload accept error {} {}".format(type(e).__name__, e.args))
            log.debug("Accepted upload from {}".format(clientAddr))
            client.close()
        log.info("End upload handler")
        self.sock.close()
