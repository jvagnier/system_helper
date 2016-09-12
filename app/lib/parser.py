import sys
import argparse
from app.settings import PARSER_COMMANDS



def main(argv=sys.argv[1:]):
    base = argparse.ArgumentParser()
    subparsers = base.add_subparsers(dest="command")

    for name, command in PARSER_COMMANDS.items():
        parser = command.make_command()
        subparsers.add_parser(name, parents=[parser], add_help=False)

    args = base.parse_args(argv)
    args = dict(vars(args))

    command_name = args.pop('command')
    command = PARSER_COMMANDS[command_name]
    command.run(**args)
