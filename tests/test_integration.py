# coding=utf-8

import collections
import unittest

import mock
import six

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


def _filter_redirect_entry(packages):
    return [package for package in packages if '*redirected' not in package]


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

            with mock.patch('sys.stdin', six.StringIO('{password}\nyes\n'.format(password=TEST_PASSWORD))):
                main([client.server_url, TEST_USER, 'delete_me==0.2'])

            indices = client.list_indices(user=TEST_USER)
            for index in indices:
                client.use(index)
                self.assertListEqual([], _filter_redirect_entry(client.list('delete_me==0.2')))
                self.assertNotEqual(0, len(_filter_redirect_entry(client.list('delete_me==0.2.dev2'))))

    def test_abort_unless_yes(self):
        with TestServer(users=TEST_USERS, indices=TEST_INDICES) as client:
            _bootstrap_test_user(client)

            with mock.patch('sys.stdin', six.StringIO('\n')):  # press enter on verification prompt
                main([client.server_url, TEST_USER, 'delete_me==0.2', '--password', TEST_PASSWORD])

            indices = client.list_indices(user=TEST_USER)
            for index in indices:
                client.use(index)
                self.assertNotEqual(0, len(_filter_redirect_entry(client.list('delete_me==0.2'))))

    def test_remove_only_dev_packages(self):
        with TestServer(users=TEST_USERS, indices=TEST_INDICES) as client:
            _bootstrap_test_user(client)

            main([client.server_url, TEST_USER, 'delete_me<=0.2', '--dev-only', '--batch', '--password', TEST_PASSWORD])

            indices = client.list_indices(user=TEST_USER)
            for index in indices:
                client.use(index)
                self.assertListEqual([], _filter_redirect_entry(client.list('delete_me==0.2.dev2')))
                self.assertNotEqual(0, len(_filter_redirect_entry(client.list('delete_me==0.1'))))
                self.assertNotEqual(0, len(_filter_redirect_entry(client.list('delete_me==0.2a1'))))
                self.assertNotEqual(0, len(_filter_redirect_entry(client.list('delete_me==0.2'))))

    def test_fails_on_non_volatile_by_default(self):
        with TestServer(users=TEST_USERS, indices=TEST_INDICES) as client:
            _bootstrap_test_user(client)

            indices = client.list_indices(user=TEST_USER)

            for index in indices:
                client.modify_index(index, 'volatile=False')

            with mock.patch('sys.stderr', new_callable=six.StringIO) as error_output:
                with self.assertRaises(SystemExit) as exit_code_catcher:
                    main([client.server_url, TEST_USER, 'delete_me', '--batch', '--password', TEST_PASSWORD])
                self.assertEquals(1, exit_code_catcher.exception.code)

            self.assertIn('not volatile', error_output.getvalue())

            for index in indices:
                client.use(index)
                self.assertNotEqual(0, len(_filter_redirect_entry(client.list('delete_me==0.1'))))
                self.assertNotEqual(0, len(_filter_redirect_entry(client.list('delete_me==0.2.dev2'))))
                self.assertNotEqual(0, len(_filter_redirect_entry(client.list('delete_me==0.2a1'))))
                self.assertNotEqual(0, len(_filter_redirect_entry(client.list('delete_me==0.2'))))

    def test_force_removal_on_non_volatile(self):
        with TestServer(users=TEST_USERS, indices=TEST_INDICES) as client:
            _bootstrap_test_user(client)

            indices = client.list_indices(user=TEST_USER)

            client.modify_index('user/index1', 'volatile=False')

            main([client.server_url, TEST_USER, 'delete_me', '--force', '--batch', '--password', TEST_PASSWORD])

            for index in indices:
                client.use(index)
                self.assertListEqual([], _filter_redirect_entry(client.list('delete_me==0.1')))
                self.assertListEqual([], _filter_redirect_entry(client.list('delete_me==0.2.dev2')))
                self.assertListEqual([], _filter_redirect_entry(client.list('delete_me==0.2a1')))
                self.assertListEqual([], _filter_redirect_entry(client.list('delete_me==0.2')))

            self.assertIn('volatile=False', client.modify_index('user/index1'))
            self.assertIn('volatile=True', client.modify_index('user/index2'))

