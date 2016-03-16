#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, division

import argparse
import collections
import logging
import os
import os.path as path
import sys


def files_directory(directory):
    return path.join(directory, '+files')


_TAR_GZ_END = '.tar.gz'
_TAR_BZ2_END = '.tar.bz2'
_ZIP_END = '.zip'
_DOC_ZIP_END = '.doc.zip'
_EGG_END = '.egg'

_Ki = 1024
_Mi = 1024 * _Ki
_Gi = 1024 * _Mi


def humanize_binary(value):
    if value // _Gi > 0:
        return '{:.1f} Gi'.format(value / _Gi)
    elif value // _Mi > 0:
        return '{:.1f} Mi'.format(value / _Mi)
    elif value // _Ki > 0:
        return '{:.1f} Ki'.format(value / _Ki)
    else:
        return '{:.1f} '.format(value)


def extract_name_and_version(filename):
    if filename.endswith('.whl') or filename.endswith('.egg'):
        return filename.split('-')[:2]
    else:
        name, version_and_ext = filename.rsplit('-', 1)
        for extension in (_TAR_GZ_END, _TAR_BZ2_END, _DOC_ZIP_END, _ZIP_END):
            if version_and_ext.endswith(extension):
                return name, version_and_ext[:-len(extension)]
        raise NotImplementedError('Unknown package type. Cannot extract version from {}.'.format(filename))


class Artefact(object):
    def __init__(self, dirpath, filename):
        self.dirpath = dirpath
        self.filename = filename
        path_components = self.dirpath.split(os.sep)
        self.user = path_components[-5]
        self.index = path_components[-4]
        (self.name, self.version) = extract_name_and_version(filename)

    @property
    def path(self):
        return path.join(self.dirpath, self.filename)

    @property
    def size(self):
        """ Get the artefact's size in bytes """
        return path.getsize(self.path)


def find_artefacts(directory):
    for (dirpath, _, filenames) in os.walk(directory):
        for filename in filenames:
            try:
                yield Artefact(dirpath, filename)
            except (ValueError, NotImplemented):
                logging.exception('Failed to process %s/%s – ignoring.', dirpath, filename)


def collect_size_information(directory):
    base_dir = files_directory(directory)

    artefacts = find_artefacts(base_dir)

    return artefacts


def generate_report(artefacts):
    size_by_package = collections.defaultdict(int)

    for artefact in artefacts:
        size_by_package[(artefact.user, artefact.name)] += artefact.size

    packages_sorted_by_size = sorted(size_by_package.items(), key=lambda x: x[1], reverse=True)

    for package, size in packages_sorted_by_size:
        print('{package_desc:<60}: {size:>10}B'.format(
            package_desc='{1} on {0}'.format(*package),
            size=humanize_binary(size)
        ))


def assert_devpi_data_dir(directory):
    """ Crude heuristic to check that this is actually a Devpi data directory. """

    if not path.isfile(path.join(directory, '.serverversion')):
        logging.error("Failed to find Devpi's server version in %s.", directory)
        sys.exit(1)

    if not path.isfile(path.join(directory, '.sqlite')):
        logging.error("Failed to find Devpi's database in %s.", directory)
        sys.exit(1)

    if not path.isdir(files_directory(directory)):
        logging.error("Failed to find Devpi's file story in %s", directory)
        sys.exit(1)

    logging.debug('Found Devpi data directory at %s', directory)


def filter_non_dev_versions(artefacts):
    return (
        artefact for artefact in artefacts if '.dev' in artefact.version
    )


def main():
    parser = argparse.ArgumentParser(
        description='Find heavy packages on Devpi'
    )
    parser.add_argument('devpi_directory', help='The data directory of the Devpi server to inspect.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show debug information.')
    parser.add_argument('--only-dev', action='store_true', help='Find only development versions as specified by PEP440.')
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=logging.DEBUG if args.verbose else logging.INFO)

    assert_devpi_data_dir(args.devpi_directory)

    size_info = collect_size_information(args.devpi_directory)

    if args.only_dev:
        size_info = filter_non_dev_versions(size_info)

    generate_report(size_info)


if __name__ == '__main__':
    main()
