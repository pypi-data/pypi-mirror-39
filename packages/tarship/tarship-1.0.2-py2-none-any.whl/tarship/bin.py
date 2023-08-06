import os
import getpass
import argparse
from tarship.utils import run_deploy

parser = argparse.ArgumentParser()
parser.add_argument('--host', help='remote hostname')
parser.add_argument('--user', help='remote user')
args = parser.parse_args()


def run():
    run_deploy(
        os.getcwd(),
        raw_input('host: ') if not args.host else args.host,
        raw_input('user: ') if not args.user else args.user,
        getpass.getpass('password: ')
    )
