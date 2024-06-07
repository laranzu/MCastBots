#!/usr/bin/env python

# Program to run lots of DNABots, each in own temp dir.
# You probably want to change the arguments and PYTHONPATH

# Usage: ./spawnBots.py N

import math, os, shutil, subprocess, sys, tempfile, time
from os import path

N = 8

UNDO = 5

# How many?
if len(sys.argv) > 1:
    N = int(sys.argv[1])
if N > 16:
    print("{} is a lot of bots".format(N))
    print("You have {} seconds to Ctrl-C".format(UNDO))
    time.sleep(UNDO)
print("Starting {} bots...".format(N))

# Dir setup is /tmp/botNNN/, zero padded so all same length
TMP = tempfile.gettempdir()

# How many digits per bot name?
d = int(math.ceil(math.log10(N + 1)))
# Format for name
fmt = "Bot{{:0{:d}d}}".format(d)

# Go!
for i in range(1, N + 1):
    fullPath = path.join(TMP, fmt.format(i))
    # Delete existing dir, create new
    if path.exists(fullPath):
        shutil.rmtree(fullPath)
    shutil.copytree("./Proto", fullPath)
    # Run
    subprocess.Popen(
        ["/usr/bin/python", "-m", "DNABot", "-debug",],
        cwd=fullPath,
        env={ "PYTHONPATH": "/home/hugh/Progs/ASD/ASD0231324_247950" },
        )
    print("Bot #{} in {}".format(i, fullPath))

print("OK.")
