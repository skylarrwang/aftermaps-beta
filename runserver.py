#!/usr/bin/env python3
"""
Runs Server
"""
import sys
from argparse import ArgumentParser, ArgumentTypeError
from app import app

def main():
    """
    Main function

    Connects to webpage using port
    """
    try:
        args = inputparse()
        port = int(args.port[0])
    except ValueError:
        print('Port must be an integer.', file=sys.stderr)
        sys.exit(1)

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def pos_input(arg_input):
    """Checks for positive port imports

    Args:
        input (int): user's input

    Raises:
        ArgumentTypeError: error based on argument type input

    Returns:
        positive integer: the user input if it's a pos. integer/
    """
    if int(arg_input) < 0:
        raise ArgumentTypeError(f"{arg_input} is not a positive integer")
    return arg_input

def inputparse():
    """parses for command line

    Returns:
        port to connect to
    """
    parser = ArgumentParser(allow_abbrev=False, description='The YUAG search application')
    parser.add_argument('port', type=pos_input, nargs=1,
                        help='the port at which the server is listening')
    return parser.parse_args()

if __name__ == '__main__':
    main()
