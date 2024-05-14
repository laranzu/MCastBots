
"""
    Main program for DNABot, ASD technical challenge program.

    Hugh/Hugo Fisher AKA laranzu
    Canberra, Australia
    hugo.fisher@gmail.com
"""

import sys

from . import config

def main(args):
    """Main control for DNABot"""
    print("Hello world")
    config.load()

if __name__ == "__main__":
    main(sys.argv)
