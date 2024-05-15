
"""
    Configuration loading and reloading for DNABot
"""

import logging as log


# Time to run, in seconds
lifespan = 30

def _setGlobal(name, value):
    """If a global exists for name, assign and preserve type"""
    modVars = globals()
    if name in modVars:
        log.debug("CLI config {} = {}".format(name, value))
    else:
        log.debug("Ignore CLI {} = {}".format(name, value))

def load(cliArgs):
    # TODO load .ini file
    # CLI args override config file
    # Must be format -key=value
    for arg in cliArgs:
        print(arg)
        if arg.startswith("-"):
            try:
                arg = arg.split("=")
                key = arg[0][1:]
                val = arg[1]
                _setGlobal(key, val)
            except IndexError:
                pass
    #

