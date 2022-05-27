import argparse
import sys
from parser import Parser


def main():
    # Validate that the incoming file is the correct file type
    if not valid_file(sys.argv[1]):
        print("USAGE: python assembler.py input.asm")
        exit()

    # Instantiate a Parser class object
    parser = Parser(sys.argv[1])


def valid_file(input):
    filename = input.split(".")
    if not filename[1].lower() == "asm":
        print("Incorrect FileType.")
        return False
    else:
        return True


if __name__ == '__main__':
    main()