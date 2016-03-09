# coding=utf-8

import argparse
import getpass
import sys

from devpi_plumber.client import DevpiClient, DevpiClientError
from six import print_
from six.moves import input
from progressbar import ProgressBar

from .client import list_packages, remove_packages, volatile_index


def main(args=None):
    parser = argparse.ArgumentParser(description='A utility to clean packages from the Devpi server used at Blue Yonder.')
    parser.add_argument('server', help='The devpi server to operate on.')
    parser.add_argument('user', help='The devpi server of which to clean the indices.')
    parser.add_argument('package_specification', help='The specification of the package version(s) to remove.')
    parser.add_argument('--batch', help='Assume yes on confirmation questions.', action='store_true')
    parser.add_argument('--dev-only', help='Remove only development versions as specified by PEP 440.', action='store_true')
    parser.add_argument('--force', help='Temporarily make indices volatile to enable package removal.', action='store_true')
    parser.add_argument('--password', help='The password with which to authenticate.')
    parser.add_argument('--login', help='The user name to user for authentication. Defaults to the user of the indices to operate on.')
    args = parser.parse_args(args=args)

    login_user = args.login if args.login else args.user
    password = args.password
    if password is None:
        password = getpass.getpass()

    try:
        with DevpiClient(args.server, login_user, password) as client:
            packages = list_packages(client, args.user, args.package_specification, args.dev_only)

            print('Packages to be deleted: ')
            for package in packages:
                print(' * {package_url}'.format(package_url=package))

            if not args.batch:
                confirmation = input('Enter "yes" to confirm: ')
                if confirmation != 'yes':
                    print('Aborting...')
                    return

            if len(packages) > 1:
                # Make iteration over the packages display a progress bar
                packages = ProgressBar()(packages)

            remove_packages(client, packages, args.force)

    except DevpiClientError as client_error:
        print_(client_error, file=sys.stderr)
        sys.exit(1)
