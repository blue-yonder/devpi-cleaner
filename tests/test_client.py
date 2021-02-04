# coding=utf-8

import unittest

from mock import Mock

from devpi_plumber.client import DevpiCommandWrapper

from devpi_cleaner.client import list_packages_by_index, remove_packages, Package


class ListTests(unittest.TestCase):
    def test_list_packages(self):
        devpi_listing = [
            'http://dummy-server/user/eins/+f/70e/3bc67b3194143/dummy-1.0.tar.gz',
            'http://dummy-server/user/zwei/+f/70e/3bc67b3194144/dummy-2.0.tar.gz',
        ]
        expected_packages = {
            'user/eins': {Package(devpi_listing[0])},
            'user/zwei': {Package(devpi_listing[1])},
        }

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.list_indices.return_value = ['user/eins', 'user/zwei']
        devpi_client.list.side_effect = [[package] for package in devpi_listing]
        devpi_client.url = 'http://dummy-server/user'

        actual_packages = list_packages_by_index(devpi_client, 'user', 'dummy', only_dev=False, version_filter=None)
        self.assertDictEqual(expected_packages, actual_packages)

    def test_list_packages_on_specified_index(self):
        devpi_listing = [
            'http://dummy-server/user/eins/+f/70e/3bc67b3194143/dummy-1.0.tar.gz',
            'http://dummy-server/user/zwei/+f/70e/3bc67b3194144/dummy-2.0.tar.gz',
        ]
        expected_packages = {
            'user/eins': {Package(devpi_listing[0])},
        }

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.list_indices.return_value = ['user/eins', 'user/zwei']
        devpi_client.list.side_effect = [[package] for package in devpi_listing]
        devpi_client.url = 'http://dummy-server/user'

        actual_packages = list_packages_by_index(devpi_client, 'user/eins', 'dummy', only_dev=False, version_filter=None)
        self.assertDictEqual(expected_packages, actual_packages)

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
            'user/index2': {Package(devpi_listing[1])}
        }

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.url = 'http://localhost:2414/user/index2'
        devpi_client.list_indices.return_value = ['user/index2']
        devpi_client.list.return_value = devpi_listing

        actual_packages = list_packages_by_index(devpi_client, 'user', 'delete_me', only_dev=False, version_filter=None)
        self.assertDictEqual(expected_packages, actual_packages)

        devpi_client.list.assert_called_once_with('--index', 'user/index2', '--all', 'delete_me')  # `--all` is important as otherwise not all packages will be returned

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
            'user/index1': {Package(devpi_listing[5])},
        }

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.url = 'http://localhost:2414/user/index1'
        devpi_client.list_indices.return_value = ['user/index1']
        devpi_client.list.return_value = devpi_listing

        actual_packages = list_packages_by_index(devpi_client, 'user', 'delete_me', only_dev=True, version_filter=None)
        self.assertDictEqual(expected_packages, actual_packages)

    def test_list_only_packages_matching_version_filter(self):
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
            'user/index1': {Package(devpi_listing[2])},
        }

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.url = 'http://localhost:2414/user/index1'
        devpi_client.list_indices.return_value = ['user/index1']
        devpi_client.list.return_value = devpi_listing

        actual_packages = list_packages_by_index(devpi_client, 'user', 'delete_me', only_dev=False, version_filter=r'a\d+')
        self.assertDictEqual(expected_packages, actual_packages)

    def test_list_packages_on_https(self):
        devpi_listing = [
            'https://dummy-server/user/eins/+f/70e/3bc67b3194143/dummy-1.0.tar.gz',
            'https://dummy-server/user/zwei/+f/70e/3bc67b3194144/dummy-2.0.tar.gz',
        ]
        expected_packages = {
            'user/eins': {Package(devpi_listing[0])},
            'user/zwei': {Package(devpi_listing[1])},
        }

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.user = 'user'
        devpi_client.list_indices.return_value = ['user/eins', 'user/zwei']
        devpi_client.list.side_effect = [[package] for package in devpi_listing]
        devpi_client.url = 'https://dummy-server/user'

        actual_packages = list_packages_by_index(devpi_client, 'user', 'dummy', only_dev=False, version_filter=None)
        self.assertDictEqual(expected_packages, actual_packages)


class RemovalTests(unittest.TestCase):
    def test_remove(self):
        packages = [
            Package('http://localhost:2414/user/index1/+f/313/8642d2b43a764/delete_me-0.2.tar.gz'),
            Package('http://localhost:2414/user/index1/+f/313/8642d2b43a764/delete_me-0.3.tar.gz'),
        ]

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.modify_index.return_value = 'volatile=True'
        devpi_client.get_json.return_value = {'result': {}}
        remove_packages(devpi_client, 'user/index1', packages, False)

        self.assertEquals(2, devpi_client.remove.call_count)

    def test_aborts_if_package_on_wrong_index(self):
        packages = [
            Package('http://localhost:2414/user/index2/+f/313/8642d2b43a764/delete_me-0.2.tar.gz'),
        ]

        devpi_client = Mock(spec=DevpiCommandWrapper)
        devpi_client.modify_index.return_value = 'volatile=True'

        with self.assertRaises(AssertionError):
            remove_packages(devpi_client, 'user/index1', packages, False)

        self.assertLess(devpi_client.remove.call_count, 1)


class PackageTests(unittest.TestCase):
    def test_sdist(self):
        package = Package('http://localhost:2414/user/index1/+f/45b/301745c6d8bbf/delete_me-0.1.tar.gz')
        self.assertEquals('user/index1', package.index)
        self.assertEquals('delete_me', package.name)
        self.assertEquals('0.1', package.version)
        self.assertFalse(package.is_dev_package)

        zip_package = Package('http://localhost:2414/user/index1/+f/45b/301745c6d8bbe/delete_me-0.1.zip')
        self.assertEquals('0.1', zip_package.version)

        with_dashes = Package('http://localhost:2414/user/index1/+f/45b/301745c6d7bbf/with-dashes-0.1.tar.gz')
        self.assertEquals('0.1', with_dashes.version)

        setuptools_scm_and_old_setuptools = Package('http://localhost:2414/user/index1/+f/25d/bb41cc64d762f/old_setuptools_used-2.1.2.dev7-ng8964316.tar.gz')
        self.assertEquals('old_setuptools_used', setuptools_scm_and_old_setuptools.name)
        self.assertEquals('2.1.2.dev7-ng8964316', setuptools_scm_and_old_setuptools.version)

        pyscaffold_and_old_setuptools = Package('http://localhost:2414/user/index1/+f/088/58034d63c6a98/old-setuptools-used-0.1.0.post0.dev4-g5e41942.tar.gz')
        self.assertEquals('old-setuptools-used', pyscaffold_and_old_setuptools.name)
        self.assertEquals('0.1.0.post0.dev4-g5e41942', pyscaffold_and_old_setuptools.version)

    def test_wheel(self):
        package = Package('http://localhost:2414/user/index1/+f/636/95eef6ac86c76/delete_me-0.2.dev2-py2.py3-none-any.whl')
        self.assertEquals('user/index1', package.index)
        self.assertEquals('delete_me', package.name)
        self.assertEquals('0.2.dev2', package.version)
        self.assertTrue(package.is_dev_package)

        old_setuptools = Package('http://localhost:2414/user/index1/+f/475/732413fe3d8f8/old_setuptools_used-0.6b3.post0.dev27_gf3ac2d5-py2-none-any.whl')
        self.assertEquals('old_setuptools_used', old_setuptools.name)
        self.assertEquals('0.6b3.post0.dev27_gf3ac2d5', old_setuptools.version)

    def test_egg(self):
        package = Package('http://localhost:2414/user/index1/+f/636/95eef6acadc76/some_egg-0.1.dev4-py2.7.egg')
        self.assertEquals('user/index1', package.index)
        self.assertEquals('some_egg', package.name)
        self.assertEquals('0.1.dev4', package.version)
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
