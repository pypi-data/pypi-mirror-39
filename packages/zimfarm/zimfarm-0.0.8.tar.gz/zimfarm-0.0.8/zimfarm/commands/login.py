from argparse import ArgumentParser, Namespace

from zimfarm.client import Client


def register(parser: ArgumentParser):
    parser.add_argument('username', type=str, help='a valid Zimfarm username')
    parser.add_argument('password', type=str, help='a valid Zimfarm password')


def process(args: Namespace):
    username, password = args.username, args.password

    print('Logging in...', end='', flush=True)

    print('success')