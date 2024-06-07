
## ASD Technical Assessment

Written by Hugh/Hugo Fisher <br/>
AKA laranzu <br/>
Canberra, Australia <br/>
hugo.fisher@gmail.com

Inspired by the Paranoia tabletop roleplaying game. (Which is also my excuse
for rushed coding and complete lack of security.) The clients are R&D robots,
using recombinant genetic engineering to create new DNA therapies, pollution
eating algae, and fast food flavours. The bots are supervised by humans who
keep an eye on progress and upload data from the bots to the server. (Better
than being the one who has to _test_ the new products.)

The bots all share a common multicast group address, which is also used by
the supervisor program.

IMPORTANT: the Fedora/RedHat/CentOS `firewalld` blocks incoming multicast, so
the bots and supervisor can send but never receive anything :-( I had to shut
down my firewall during testing.

For testing, you can run everything on a single host with address 127.0.0.1.
Everybody can send, but only the last program started will receive.



#### Running bot

Written as a Python package, so run with `python -m DNABot` from parent
directory. Bots are not interactive.

To run from somewhere else, `export PYTHONPATH="/full/path/to/ASD0231324_247950`
first. Since this is a Python module rather than a program, don't forget to clear
`__pycache__` first if you've changed any of the imports.

Various options and parameters can be set from a config file `dnabot.ini` in the
current directory, ie where you run the program from NOT the DNABot dir. These
can in turn be overridden by command line args.


`-info`     Log level <br/>
`-debug`    Log level

`-fg`       Send output (log) to stdout, not to a file

`-config <filename>`  Use a different config file  <br/>
`-name=value`         Override config file


#### Running lots of bots

`spawnBots.py` is my utility program to run a whole lot of bots on my Linux
PC for testing. Creates a whole bunch of dirs in /tmp, copies `Proto/` into
each, starts a new DNABot.

Written for my PC, so you will need to edit the code to set the correct path
and destination for your system.


#### Running the supervisor

This is another Python package, so `python -m Supervisor`

The supervisor borrows some code from DNABot, so if you want to move the code
somewhere else, copy everything.

The supervisor spends most of its time printing out channel traffic. You can
type messages on the command line for sending at any time, slightly easier
if you first enter a blank line to suspend the printout. (Press Enter again
when you want to resume.)

Messages are `CODE dest [args]` where the CODE is an opcode as described in `protocol.md`
(You can enter lowercase codes, the supervisor will capitalize before sending.)
The destination is usually a botname, as shown at the start
of each printed channel message, but can be a wildcard `*` for all bots.

Currently implemented: `PING, UPLD, KILL` </br>
If you don't enter a specific upload file name, the supervisor adds the default
bot results file.

If you want to run more than one supervisor at a time, sure why not?


#### Going Frankenstein

_"Sometimes we go bad."_ Cameron, The Sarah Connor Chronicles.

Bots are supposed to be constrained by "Asimovs", in built Laws of Robotics.
If a bot manages to hack itself and escape control they become dangerous.
Supervisors can activate the remote self destruct with the `KILL` command,
but this makes other bots
nervous and more likely to go Frankenstein themselves. So maybe it is better
to just let the bots do their thing.
