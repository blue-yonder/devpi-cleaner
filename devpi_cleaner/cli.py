# coding=utf-8

from argparse import ArgumentParser

from devpi_plumber.client import DevpiClient
from six.moves import input

from .client import list_packages, remove_packages


def main(args=None):
    parser = ArgumentParser(description='A utility to clean packages from the Devpi server used at Blue Yonder.')
    parser.add_argument('server', help='The devpi server to operate on.')
    parser.add_argument('user', help='The devpi server of which to clean the indices')
    parser.add_argument('password', help='The password with which to authenticate')
    parser.add_argument('package_specification', help='The specification of the package version(s) to remove.')
    parser.add_argument('--dev-only', help='Remove only development versions as specified by PEP 440.', action='store_true')
    args = parser.parse_args(args=args)

    with DevpiClient(args.server, args.user, args.password) as client:
        packages = list_packages(client, args.package_specification)

        print 'Packages to be deleted: '
        for package in packages:
            print ' * {package_url}'.format(package_url=package)

        confirmation = input('Entery "yes" to confirm: ')
        if confirmation != 'yes':
            print 'Aborting...'
            return

        remove_packages(client, packages)
