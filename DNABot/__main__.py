
import sys

from . import config

def main(args):
    """Main control for DNABot"""
    print("Hello world")
    config.load()

if __name__ == "__main__":
    main(sys.argv)
