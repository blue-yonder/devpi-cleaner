# coding=utf-8

from argparse import ArgumentParser

from devpi_plumber.client import DevpiClient


def main(args=None):
    parser = ArgumentParser(description='A utility to clean packages from the Devpi server used at Blue Yonder.')
    args = parser.parse_args(args=args)

    with DevpiClient(args.server, args.user, args.password) as client:
        pass
