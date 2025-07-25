"""
    Handle file uploads from bots for the supervisor
"""

import socket, threading, time
import logging as log

from DNABot import config, mcast

from . import supervisor

class UploadHandler(threading.Thread):
    """Handle incoming TCP uploads from bots"""

    def __init__(self, channel, output):
        """Channel so we know IPv4 or IPv6. Output stream is where uploads are printed"""
        super().__init__()
        self.output = output
        self.sock = None
        if channel.address.version == 6:
            self.addrFamily = socket.AF_INET6
            self.servAddr   = "::"
        else:
            self.addrFamily = socket.AF_INET
            self.servAddr   = "0.0.0.0"
        # Use to end thread
        self.running = True

    def receiveFile(self, client):
        """Handle single file upload"""
        # Read binary from socket
        inData = b''
        while True:
            try:
                chunk = client.recv(config.PKT_SIZE)
                if len(chunk) == 0:
                    break
                inData += chunk
            except (socket.timeout, TimeoutError):
                break
            except OSError as e:
                log.warning(tr("Upload error {} {}").format(type(e).__name__, e.args))
                break
        log.debug("Bot upload socket close")
        client.close()
        self.content(inData)

    def content(self, data):
        """Just print the file to stdout"""
        if len(data) <= 0:
            log.warning(tr("Empty file upload"))
            return
        # Assume it is text
        txt = data.decode('utf-8', 'backslashreplace')
        lines = txt.splitlines(keepends=True)
        # Log the first line, expected to be HTTP style status response
        log.info(tr("UPLOAD {}").format(lines[0]))
        # Print content
        for s in lines:
            self.output.write(s)
        if len(lines) == 1:
            self.output.write("EOF\n")

    def run(self):
        """TCP server"""
        log.debug("Start upload handler")
        self.sock = socket.socket(self.addrFamily, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.servAddr, config.filePort))
        self.sock.listen(5)
        # Put timeout on socket so can check self.running
        self.sock.settimeout(2.0)
        log.info(tr("File uploads to {} : {}").format(self.sock.getsockname()[0],
                                        self.sock.getsockname()[1]))
        while self.running:
            try:
                client, clientAddr = self.sock.accept()
            except (socket.timeout, TimeoutError):
                continue
            except OSError as e:
                log.warning(tr("Upload accept error {} {}").format(type(e).__name__, e.args))
                continue
            log.debug("Accept from {}".format(clientAddr))
            self.receiveFile(client)
        log.info(tr("End upload handler"))
        self.sock.close()
