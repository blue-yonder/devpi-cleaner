# coding=utf-8

from contextlib import contextmanager

from devpi_plumber.client import DevpiClientError

_TAR_GZ_END = '.tar.gz'
_ZIP_END = '.zip'


class Package(object):
    def __init__(self, package_url):
        self.url = package_url
        parts = self.url.rsplit('/', 6)
        self.index = parts[1] + '/' + parts[2]
        self.name, self.version = parts[6].split('-', 1)
        self._remove_distribution_type_from_version()
        self.is_dev_package = '.dev' in self.version

    def _remove_distribution_type_from_version(self):
        if _TAR_GZ_END in self.version:
            self.version = self.version[:-len(_TAR_GZ_END)]
        elif _ZIP_END in self.version:
            self.version = self.version[:-len(_ZIP_END)]
        elif self.version.endswith('.whl'):
            self.version = self.version.split('-')[0]
        else:
            raise NotImplementedError('Unknown package type {}. Cannot extract version.'.format(self.url))

    def __str__(self):
        return self.url


def _list_packages_on_current_index(client, package_spec, only_dev):
    return [
        Package(package_url)
        for package_url in client.list('--all', package_spec)
        if package_url.startswith(client.url)
        and (not only_dev or Package(package_url).is_dev_package)
    ]


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


def remove_packages(client, packages):
    for package in _filter_duplicates(packages):
        client.use(package.index)
        client.remove('{name}=={version}'.format(name=package.name, version=package.version))


def _set_index_volatility(client, value, *indices):
    for index in indices:
        client.modify_index(index, 'volatile={}'.format(value))


@contextmanager
def volatile_indices(client, *indices, **kwargs):
    """
    Ensure that the given indices are volatile.

    Unless the keyword argument `force` is used an exception will be raised if the index is not volatile.

    :param client: A devpi_plumber.DevpiClient connected to the server to operate on.
    :param indices: The indices to ensure the volatility on.
    :param force: If True, the indices will be set volatile and reset at the end.
    """
    force = kwargs.get('force', False)

    non_volatile_indices = [index for index in indices if 'volatile=False' in client.modify_index(index)]

    if len(non_volatile_indices) > 0:
        if force:
            _set_index_volatility(client, True, *non_volatile_indices)
        else:
            raise DevpiClientError('\n'.join(['Index {} is not volatile.'.format(index) for index in indices]))

    yield

    _set_index_volatility(client, False, *non_volatile_indices)
