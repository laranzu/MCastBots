
## ASD Technical Assessment

Written by Hugh/Hugo Fisher \
AKA laranzu \
Canberra, Australia \
hugo.fisher@gmail.com

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
