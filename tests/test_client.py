# coding=utf-8

import unittest

from mock import Mock

from devpi_plumber.client import DevpiCommandWrapper

from devpi_cleaner.client import list_packages, remove_packages, Package


class ListTests(unittest.TestCase):
    def test_list_packages(self):
        devpi_listing = [
            'http://dummy-server/user/eins/+f/70e/3bc67b3194143/dummy-1.0.tar.gz',
            'http://dummy-server/user/zwei/+f/70e/3bc67b3194144/dummy-2.0.tar.gz',
        ]
        expected_packages = {
            'dummy 1.0 on user/eins',
            'dummy 2.0 on user/zwei',
        }

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.list_indices.return_value = ['user/eins', 'user/zwei']
        devpi_client.list.side_effect = [[package] for package in devpi_listing]
        devpi_client.url = 'http://dummy-server/user'

        actual_packages = list_packages(devpi_client, 'user', 'dummy', only_dev=False)
        self.assertSetEqual(expected_packages, {str(package) for package in actual_packages})

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
        expected_packages = {
            'delete_me 0.2 on user/index2',
        }

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.url = 'http://localhost:2414/user/index2'
        devpi_client.list_indices.return_value = ['user/index2']
        devpi_client.list.return_value = devpi_listing

        actual_packages = list_packages(devpi_client, 'user', 'delete_me', only_dev=False)
        self.assertSetEqual(expected_packages, {str(package) for package in actual_packages})

        devpi_client.list.assert_called_once_with('--all', 'delete_me')  # `--all` is important as otherwise not all packages will be returned

    def test_list_only_dev_packages(self):
        devpi_listing = [
            'http://localhost:2414/user/index1/+f/70e/3bc67b3194143/delete_me-0.2-py2.py3-none-any.whl',
            'http://localhost:2414/user/index1/+f/313/8642d2b43a764/delete_me-0.2.tar.gz',
            'http://localhost:2414/user/index1/+f/bab/f9b37c9d0d192/delete_me-0.2a1.tar.gz',
            'http://localhost:2414/user/index1/+f/e8e/d9cfe14d2ef65/delete_me-0.2a1-py2.py3-none-any.whl',
            'http://localhost:2414/user/index1/+f/842/84d1283874110/delete_me-0.2.dev2.tar.gz',
            'http://localhost:2414/user/index1/+f/636/95eef6ac86c76/delete_me-0.2.dev2-py2.py3-none-any.whl',
            'http://localhost:2414/user/index1/+f/c22/cdec16d5ddc3a/delete_me-0.1-py2.py3-none-any.whl',
            'http://localhost:2414/user/index1/+f/45b/301745c6d8bbf/delete_me-0.1.tar.gz',
        ]
        expected_packages = {
            'delete_me 0.2.dev2 on user/index1',
        }

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.url = 'http://localhost:2414/user/index1'
        devpi_client.list_indices.return_value = ['user/index1']
        devpi_client.list.return_value = devpi_listing

        actual_packages = list_packages(devpi_client, 'user', 'delete_me', only_dev=True)
        self.assertSetEqual(expected_packages, {str(package) for package in actual_packages})

    def test_list_packages_on_https(self):
        devpi_listing = [
            'https://dummy-server/user/eins/+f/70e/3bc67b3194143/dummy-1.0.tar.gz',
            'https://dummy-server/user/zwei/+f/70e/3bc67b3194144/dummy-2.0.tar.gz',
        ]
        expected_packages = {
            'dummy 1.0 on user/eins',
            'dummy 2.0 on user/zwei',
        }

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.list_indices.return_value = ['user/eins', 'user/zwei']
        devpi_client.list.side_effect = [[package] for package in devpi_listing]
        devpi_client.url = 'https://dummy-server/user'

        actual_packages = list_packages(devpi_client, 'user', 'dummy', only_dev=False)
        self.assertSetEqual(expected_packages, {str(package) for package in actual_packages})


class RemovalTests(unittest.TestCase):
    def test_same_package_on_separate_indices(self):
        packages = [
            Package('http://localhost:2414/user/index1/+f/313/8642d2b43a764/delete_me-0.2.tar.gz'),
            Package('http://localhost:2414/user/index2/+f/313/8642d2b43a764/delete_me-0.2.tar.gz'),
        ]

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.modify_index.return_value = 'volatile=True'
        remove_packages(devpi_client, packages, False)

        devpi_client.remove.assert_called_with('delete_me==0.2')
        self.assertEquals(2, devpi_client.remove.call_count)


class PackageTests(unittest.TestCase):
    def test_sdist(self):
        package = Package('http://localhost:2414/user/index1/+f/45b/301745c6d8bbf/delete_me-0.1.tar.gz')
        self.assertEquals('user/index1', package.index)
        self.assertEquals('delete_me', package.name)
        self.assertEquals('0.1', package.version)
        self.assertFalse(package.is_dev_package)

        zip_package = Package('http://localhost:2414/user/index1/+f/45b/301745c6d8bbe/delete_me-0.1.zip')
        self.assertEquals('0.1', zip_package.version)

    def test_wheel(self):
        package = Package('http://localhost:2414/user/index1/+f/636/95eef6ac86c76/delete_me-0.2.dev2-py2.py3-none-any.whl')
        self.assertEquals('user/index1', package.index)
        self.assertEquals('delete_me', package.name)
        self.assertEquals('0.2.dev2', package.version)
        self.assertTrue(package.is_dev_package)

    def test_unknown_format(self):
        with self.assertRaises(NotImplementedError):
            Package('http://localhost:2414/user/index1/+f/45b/301745c6d8bbf/delete_me-0.1.unkown')

    def test_string(self):
        http_url = 'http://localhost:2414/user/index1/+f/45b/301745c6d8bbf/delete_me-0.1.tar.gz'
        package = Package(http_url)
        self.assertEquals('delete_me 0.1 on user/index1', str(package))

    def test_from_https_url(self):
        package = Package('https://localhost:2414/user/index1/+f/636/95eef6ac86c76/delete_me-0.2.dev2-py2.py3-none-any.whl')
        self.assertEquals('user/index1', package.index)
        self.assertEquals('delete_me', package.name)
        self.assertEquals('0.2.dev2', package.version)
        self.assertTrue(package.is_dev_package)

    def test_comparison(self):
        package_v1_sdist = Package('http://localhost:2414/user/index1/+f/45b/301745c6d8bbf/delete_me-0.1.tar.gz')
        package_v1_wheel = Package('https://localhost:2414/user/index1/+f/636/95eef6ac86c76/delete_me-0.1-py2.py3-none-any.whl')
        package_v2_wheel = Package('https://localhost:2414/user/index1/+f/636/95eef6ac86c76/delete_me-0.2-py2.py3-none-any.whl')
        other_package_v1_sdist = Package('https://dummy-server/user/eins/+f/70e/3bc67b3194143/dummy-0.1.tar.gz')

        self.assertEquals(package_v1_sdist, package_v1_sdist)
        self.assertEquals(package_v1_sdist, package_v1_wheel)
        self.assertNotEquals(package_v1_wheel, package_v2_wheel)
        self.assertNotEquals(package_v1_sdist, other_package_v1_sdist)

    def test_hash(self):
        package_v1_sdist = Package('http://localhost:2414/user/index1/+f/45b/301745c6d8bbf/delete_me-0.1.tar.gz')
        package_v1_wheel = Package(
            'https://localhost:2414/user/index1/+f/636/95eef6ac86c76/delete_me-0.1-py2.py3-none-any.whl')
        package_v2_wheel = Package(
            'https://localhost:2414/user/index1/+f/636/95eef6ac86c76/delete_me-0.2-py2.py3-none-any.whl')
        other_package_v1_sdist = Package('https://dummy-server/user/eins/+f/70e/3bc67b3194143/dummy-0.1.tar.gz')

        self.assertEquals(hash(package_v1_sdist), hash(package_v1_sdist))
        self.assertEquals(hash(package_v1_sdist), hash(package_v1_wheel))
        self.assertNotEquals(hash(package_v1_wheel), hash(package_v2_wheel))
        self.assertNotEquals(hash(package_v1_sdist), hash(other_package_v1_sdist))
