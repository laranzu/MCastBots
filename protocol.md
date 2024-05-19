
## DNABot protocol

All bots and supervisors are members of a multicast group. All commands
and reports are sent to the group address and received by all, but most
have a single destination in the message.

Current programs use an IPv4 239.0.0.0/8 address, administrative scope
that should never be transmitted over the global Internet.

Future version: register bots with multicast DNS as well? Discover port
through SRV records?


#### Message header

Each message is one line of text, space separate fields.
Standard prefix is

`sender sequenceNumber opcode destination`

The `sender` is the identifier assigned by the program. Bots have an 8
digit hex identifier, randomly chosen.

The `sequence number` is a sender-specific, not global, integer.
I was going to implement an OSPF 32 bit lollipop wrapping sequence,
but then I remembered this is Python and we have infinite precision
integers. (Plus I doubt these bots are going to run for long enough
to overflow anything.) So they just keep incrementing from 1.

`Opcode` is a four character verb or command. See description below.

`Destination` is usually another program identifier. Some opcodes
accept * meaning that this message should be acted on by all; or
that this is an informational message, no action required.


#### Opcodes

`NEWS * text...`
Bot has discovered a new genetic sequence or something. Just notice,
actual data stored by bot in a file.

`BEAT * text...`
Heartbeat message to indicate that the bot is still running.

`UPLD dest portnum filename`
Request bot to open TCP connection to specified port on sender and
upload the named file. Most often used to upload bot scientific data,
but could be config file, source code, etc.

TCP probably will be HTTP response with status code and content type
descriptor before data.

`PING dest`
Request bot send an immediate BEAT message.

`RSET dest`
Request bot to reset itself from configuration file, keeping any
created scientific data.

`KILL dest`
Activate bot self-destruct, removing both bot and any research results.
Supervisors are advised to use only when absolutely necessary as it makes
the other bots nervous. If the dest is * everything shuts down.


#### Reliable multicast opcodes

`NACK sender sequenceNumber`
Missing packet detected by gaps in received sequence numbers. Since this
is multicast will be random backoff, and don't NACK if someone else has
already done so.

`RSND sender sequenceNumber message...`
Resend in response to NACK. Usually expected to be the original sender,
but any bot with a copy of the packet can do so.

`SKIP sender sequenceNumber`
Indicate that missing packet was a BEAT, NACK, or RSND that does not
need retransmission, or that original message wasn't saved or something.
