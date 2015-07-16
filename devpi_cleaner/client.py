# coding=utf-8

from contextlib import contextmanager

from devpi_plumber.client import DevpiClientError

_TAR_GZ_END = '.tar.gz'
_ZIP_END = '.zip'


def _remove_distribution_type_from_version(version):
    if version.endswith(_TAR_GZ_END):
        return version[:-len(_TAR_GZ_END)]
    elif version.endswith(_ZIP_END):
        return version[:-len(_ZIP_END)]
    elif version.endswith('.whl'):
        return version.split('-')[0]
    else:
        raise NotImplementedError('Unknown package type. Cannot extract version from {}.'.format(version))


class Package(object):
    def __init__(self, package_url):
        self.url = package_url
        parts = self.url.rsplit('/', 6)  # example URL http://localhost:2414/user/index1/+f/45b/301745c6d8bbf/delete_me-0.1.tar.gz
        self.index = parts[1] + '/' + parts[2]
        self.name, version_plus_distribution_type = parts[6].split('-', 1)
        self.version = _remove_distribution_type_from_version(version_plus_distribution_type)
        self.is_dev_package = '.dev' in self.version

    def __str__(self):
        return self.url


def _list_packages_on_current_index(client, package_spec, only_dev):
    def selector(package):
        return package.url.startswith(client.url) and (not only_dev or package.is_dev_package)

    all_packages = [
        Package(package_url) for package_url in client.list('--all', package_spec) if package_url.startswith('http://')
    ]
    return filter(selector, all_packages)


def list_packages(client, package_spec, only_dev):
    result = []
    for index in client.list_indices(user=client.user):
        client.use(index)
        result.extend(_list_packages_on_current_index(client, package_spec, only_dev))
    return result


def _filter_duplicates(packages):
    return {
        (package.index, package.name, package.version): package for package in packages
    }.values()


def remove_packages(client, packages, force):
    for package in _filter_duplicates(packages):
        client.use(package.index)
        with volatile_index(client, package.index, force):
            client.remove('{name}=={version}'.format(name=package.name, version=package.version))


@contextmanager
def volatile_index(client, index, force=False):
    """
    Ensure that the given index is volatile.

    Unless the keyword argument `force` is used an exception will be raised if the index is not volatile.

    :param client: A devpi_plumber.DevpiClient connected to the server to operate on.
    :param index: The index to ensure the volatility on.
    :param force: If True, the indices will be set volatile and reset at the end.
    """
    is_non_volatile = 'volatile=False' in client.modify_index(index)

    if is_non_volatile:
        if force:
            client.modify_index(index, 'volatile=True')
        else:
            raise DevpiClientError('Index {} is not volatile.'.format(index))
    try:

        yield

    finally:
        if is_non_volatile:
            client.modify_index(index, 'volatile=False')
