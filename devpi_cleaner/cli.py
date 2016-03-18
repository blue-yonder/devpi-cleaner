# coding=utf-8

import argparse
import getpass
import sys

from devpi_plumber.client import DevpiClient, DevpiClientError
from six import print_
from six.moves import input
from progressbar import ProgressBar

from .client import list_packages_by_index, remove_packages


def main(args=None):
    parser = argparse.ArgumentParser(
        description='A utility to batch-remove packages from a Devpi server.',
        epilog='The arguments --dev-only and --version-filter can be combined. In this case only packages passing both filters will be removed.',
    )
    parser.add_argument('server', help='The devpi server to operate on.')
    parser.add_argument('index_spec', metavar='user[/index]', help='The index from which to remove the packages. If only the user part is specified, all indices of that user will be cleaned.')
    parser.add_argument('package_specification', help='The specification of the package version(s) to remove.')
    parser.add_argument('--batch', help='Assume yes on confirmation questions.', action='store_true')
    parser.add_argument('--dev-only', help='Remove only development versions as specified by PEP 440.', action='store_true')
    parser.add_argument('--version-filter', metavar='REGEX', help='Remove only versions in which the given regular expression can be found.')
    parser.add_argument('--force', help='Temporarily make indices volatile to enable package removal.', action='store_true')
    parser.add_argument('--password', help='The password with which to authenticate.')
    parser.add_argument('--login', help='The user name to user for authentication. Defaults to the user of the indices to operate on.')
    args = parser.parse_args(args=args)

    login_user = args.login if args.login else args.index_spec.split('/')[0]
    password = args.password
    if password is None:
        password = getpass.getpass()

    try:
        with DevpiClient(args.server, login_user, password) as client:
            packages_by_index = list_packages_by_index(
                client, args.index_spec, args.package_specification, args.dev_only, args.version_filter
            )

            for index, packages in packages_by_index.items():
                print('Packages to be deleted from {}: '.format(index))
                for package in packages:
                    print(' * {}'.format(package))

            if not args.batch:
                confirmation = input('Enter "yes" to confirm: ')
                if confirmation != 'yes':
                    print('Aborting...')
                    return

            for index, packages in packages_by_index.items():
                print('Cleaning {}…'.format(index))
                if len(packages) > 1:
                    # Make iteration over the packages display a progress bar
                    packages = ProgressBar()(packages)
                remove_packages(client, index, packages, args.force)

    except DevpiClientError as client_error:
        print_(client_error, file=sys.stderr)
        sys.exit(1)
