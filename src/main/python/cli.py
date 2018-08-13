
import argparse

import gitpage_flask


def cli():
    # create cli options parser and configure it
    cli_parser = argparse.ArgumentParser()

    cli_parser.add_argument('command', choices=['start', 'stop', 'status'],
                            help='start, stop, or view the status of the gitpage server')

    # parse the arguments provided
    options = cli_parser.parse_args()

    # pass the command to the command handler
    execute_command(options.command)


def execute_command(command):
    if command == 'start':
        gitpage_flask.start_flask()
    elif command == 'stop':
        pass


if __name__ == '__main__':
    cli()
