# coding=utf-8

from devpi_plumber.client import volatile_index

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
        parts = package_url.rsplit('/', 6)  # example URL http://localhost:2414/user/index1/+f/45b/301745c6d8bbf/delete_me-0.1.tar.gz
        self.index = parts[1] + '/' + parts[2]
        self.name, version_plus_distribution_type = parts[6].split('-', 1)
        self.version = _remove_distribution_type_from_version(version_plus_distribution_type)

    def __str__(self):
        return '{package} {version} on {index}'.format(
            package=self.name,
            version=self.version,
            index=self.index,
        )

    @property
    def is_dev_package(self):
        return '.dev' in self.version

    def __eq__(self, other):
        return self.index == other.index and self.name == other.name and self.version == other.version

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.index, self.name, self.version))


def _list_packages_on_index(client, index, package_spec, only_dev):
    def selector(package):
        return package.index == index and (not only_dev or package.is_dev_package)

    client.use(index)

    all_packages = {
        Package(package_url) for package_url in client.list('--all', package_spec)
        if package_url.startswith('http://') or package_url.startswith('https://')
    }

    return filter(selector, all_packages)


def list_packages(client, user, package_spec, only_dev):
    packages = set()
    for index in client.list_indices(user=user):
        packages.update(_list_packages_on_index(client, index, package_spec, only_dev))
    return packages


def remove_packages(client, packages, force):
    for package in packages:
        client.use(package.index)
        with volatile_index(client, package.index, force):
            client.remove('{name}=={version}'.format(name=package.name, version=package.version))
