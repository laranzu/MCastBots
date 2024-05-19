"""
    Multicast group protocol for bots and supervisors

    Basic unreliable multicast for now - since I'm running my tests
    on localhost, not a problem.
    The Plan is to add NACK based reliability in a future version.
"""

import socket, struct

class Channel(object):
    """Multicast group communication channel"""

    pass
