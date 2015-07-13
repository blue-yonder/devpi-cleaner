# coding=utf-8

import unittest

from mock import Mock

from devpi_plumber.client import DevpiCommandWrapper

from devpi_cleaner.client import list_packages


class ClientTests(unittest.TestCase):
    def test_list_packages(self):
        expected_packages = [
            'http://dummy-server/nutzer/eins/paket-1.0',
            'http://dummy-server/nutzer/zwei/paket-2.0',
        ]

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'nutzer'
        devpi_client.list_indices.return_value = ['eins', 'zwei']
        devpi_client.list.side_effect = [[package] for package in expected_packages]
        devpi_client.url = 'http://dummy-server/nutzer'

        actual_packages = list_packages(devpi_client, 'paket')
        self.assertEqual(expected_packages, actual_packages)

    def test_list_packages_filters(self):
        """
        The package list must be stripped from inherited packages and [*redirected] messages
        """
        devpi_listing = [
            '*redirected: http://localhost:2414/user/index2/delete_me',
            'http://localhost:2414/user/index2/+f/70e/3bc67b3194143/delete_me-0.2-py2.py3-none-any.whl',
            'http://localhost:2414/user/index2/+f/313/8642d2b43a764/delete_me-0.2.tar.gz',
            'http://localhost:2414/other_user/index1/+f/70e/3bc67b3194143/delete_me-0.2-py2.py3-none-any.whl',
            'http://localhost:2414/other_user/index1/+f/313/8642d2b43a764/delete_me-0.2.tar.gz'
        ]
        expected_packages = [
            'http://localhost:2414/user/index2/+f/70e/3bc67b3194143/delete_me-0.2-py2.py3-none-any.whl',
            'http://localhost:2414/user/index2/+f/313/8642d2b43a764/delete_me-0.2.tar.gz',
        ]

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.url = 'http://localhost:2414/user/index2'
        devpi_client.list_indices.return_value = ['index2']
        devpi_client.list.return_value = devpi_listing

        actual_packages = list_packages(devpi_client, 'delete_me')
        self.assertEqual(expected_packages, actual_packages)
