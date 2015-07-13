# coding=utf-8

import collections
import unittest
import StringIO

import mock

from devpi_plumber.server import TestServer

from devpi_cleaner.cli import main

TEST_USER = 'user'
TEST_PASSWORD = 'password'
TEST_USERS = {TEST_USER: {'password': TEST_PASSWORD}}

TEST_INDICES = collections.OrderedDict()
TEST_INDICES[TEST_USER + '/index1'] = {'bases': ''}
TEST_INDICES[TEST_USER + '/index2'] = {'bases': TEST_USER + '/index1'}


def _bootstrap_test_user(client):
    indices = client.list_indices(user=TEST_USER)
    for index in indices:
        client.login(TEST_USER, TEST_PASSWORD)
        client.use(index)
        client.upload('tests/artefacts/delete_me_package/dist', directory=True)


class IntegrationTests(unittest.TestCase):

    def test_dummy_setup(self):
        with TestServer(users=TEST_USERS, indices=TEST_INDICES) as client:
            _bootstrap_test_user(client)

            indices = client.list_indices(user=TEST_USER)
            for index in indices:
                client.use(index)
                for version in ['0.1', '0.2.dev2', '0.2a1', '0.2']:
                    actual_packages = client.list('delete_me=={}'.format(version))
                    for dist in ['.tar.gz', '-py2.py3-none-any.whl']:
                        expected = 'delete_me-{version}{dist}'.format(version=version, dist=dist)
                        self.assertTrue(any(entry.endswith(expected) for entry in actual_packages))

    def test_removes_specified_packages(self):
        with TestServer(users=TEST_USERS, indices=TEST_INDICES) as client:
            _bootstrap_test_user(client)

            with mock.patch('sys.stdin', StringIO.StringIO('yes\n')):
                main([client.server_url, TEST_USER, TEST_PASSWORD, 'delete_me==0.2'])

            indices = client.list_indices(user=TEST_USER)
            for index in indices:
                client.use(index)
                actual_package_list = [package for package in client.list('delete_me==0.2') if '*redirected' not in package]
                self.assertListEqual([], actual_package_list)
                self.assertNotEqual(0, len(client.list('delete_me==0.2.dev2')))
