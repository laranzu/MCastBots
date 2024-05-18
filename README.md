
## ASD Technical Assessment

Written by Hugh/Hugo Fisher \
AKA laranzu \
Canberra, Australia \
hugo.fisher@gmail.com

Inspired by the Paranoia tabletop roleplaying game. (Which is also my excuse
for rushed coding and complete lack of security.) The clients are R&D robots,
using recombinant genetic engineering to create new DNA therapies, pollution
eating algae, and fast food flavours. The bots are supervised by humans who
keep an eye on progress and upload data from the bots to the server. (Better
than being the one who has to _test_ the new products.)

#### Running program

Written as a Python package, so run with `python -m DNABot` from parent
directory.

To run from somewhere else, `export PYTHONPATH="/full/path/to/ASD0231324_247950`
first. Since this is a Python module rather than a program, don't forget to clear
`__pycache__` first if you've changed any of the imports.

Various options and parameters can be set from a config file `dnabot.ini` in the
current directory, ie where you run the program from NOT the DNABot dir. These
can in turn be overridden by command line args.


`-info`     Log level \
`-debug`    Log level

`-fg`       Send output (log) to stdout, not to a file

`-config <filename>`  Use a different config file   \
`-name=value`         Override config file


#### Running lots of bots

`spawnBots.py` is my utility program to run a whole lot of bots on my Linux
PC for testing. Creates a whole bunch of dirs in /tmp, copies `Proto/` into
each, starts a new DNABot.
