# coding=utf-8

from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description='A utility to clean packages from the Devpi server used at Blue Yonder.')
    args = parser.parse_args()
