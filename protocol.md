
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

The `sequence number` is a sender-specific, not global, integer. I was
going to implement an OSPF 32 bit lollipop wrapping sequence,
but then I remembered this is Python and we have infinite precision
integers. (Plus I doubt these bots are going to run for long enough
to overflow anything.) So they just keep incrementing from 1.

`Opcode` is a four character verb or command. See description below.

`Destination` is usually another program identifier. Some opcodes
accept * meaning that this message should be acted on by all; or
that this is an informational message, no action required.


#### Opcodes

`NEWS text...`
Bot has discovered a new genetic sequence. Rest of the message is a
short text description.

`BEAT text...`
This is a heartbeat message to indicate that the bot is still running.
