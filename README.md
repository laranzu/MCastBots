
## Multicast Peer to Peer Demo in Python

Written by Hugh/Hugo Fisher <br/>
AKA laranzu <br/>
Canberra, Australia <br/>
hugo.fisher@gmail.com

Released under MIT License

Version 1.0

This was an Australian Signals Directorate technical assessment. I applied for
a job there, was instructed to write the code for a peer to peer system and
push it to a GitHub repo. I did so and never heard from ASD again. So if you
are here because you are also applying to ASD, I wouldn't copy the code.

This is a peer to peer system, meaning that there is no server that every
other program connects to like a web site or Gmail. All the peers are
identical programs that communicate over an IP multicast group address.
This is very Ship of Theseus, any peer can join or leave at any time, but
the group persists while at least one is active on the multicast address.

My system is inspired by the Paranoia tabletop roleplaying game, so the
peers represent bots (robots) using recombinant genetic engineering to research
new DNA therapies, pollution eating algae, and fast food flavours. Every so
often a bot makes a discovery and announces this on the multicast group, and
all the bots send heartbeat packets at regular intervals.

Supervisors are a second type of program, representing the humans who keep an
eye on progress and upload data from the bots. (Better than being the humans
who have to _test_ the new products.) Supervisor programs also use the
multicast group address to discover bots by listening to announcements or
active pings, requesting bots to send their data to the supervisor, and even
shutting down bots. Since they are also "peers", supervisors can come and go,
and there can be more than one supervisor running at the same time.


IMPORTANT: the Fedora/RedHat/CentOS `firewalld` or local equivalent may block
incoming multicast, if so the bots and supervisor can send but never receive
anything :-( I changed to the "Workstation" profile which is for developers
and thus allows most traffic, or you could just shut down the firewall for
testing. (Not on your production system, right?)

For testing, you can run everything on a single host with address 127.0.0.1.
Everybody can send, but only the last program started will receive.



#### Running bot

Written as a Python package, so run with `python -m DNABot` from parent
directory. Bots are not interactive, but I recommend `-fg` for testing.

To run from somewhere else, `export PYTHONPATH="/full/path/to/MCastBots`
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


#### Translation

`I18N` has commands and data for translating into other languages.

Both the bot and supervisor will **run** with just the standard Python library.
To make a new translation or update existing you will need the `babel` Python
package.

Information, warning, error strings are all marked for translation. Debug
messages are not because all the code and comments are in English.


#### Plans

Handle lost messages. Since multicast on my own PC is very reliable, will
add a network setting to simulate packet loss.

Java version? Good interoperability test
