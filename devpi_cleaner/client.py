# coding=utf-8


_TAR_GZ_END = '.tar.gz'


class Package(object):
    def __init__(self, package_url):
        self.url = package_url
        parts = self.url.rsplit('/', 6)
        self.index = parts[1] + '/' + parts[2]
        self.name, self.version = parts[6].split('-', 1)
        self._remove_distribution_type_from_version()

    def _remove_distribution_type_from_version(self):
        if _TAR_GZ_END in self.version:
            self.version = self.version[:-len(_TAR_GZ_END)]
        elif self.version.endswith('.whl'):
            self.version = self.version.split('-')[0]
        else:
            raise NotImplemented('Unkown package type {}. Cannot extract version.'.format(self.url))

    def __str__(self):
        return self.url


def _list_packages_on_current_index(client, package_spec):
    return [
        package_url
        for package_url in client.list('--all', package_spec)
        if package_url.startswith(client.url)
    ]


def list_packages(client, package_spec):
    result = []
    for index in client.list_indices(user=client.user):
        client.use(index)
        result.extend(_list_packages_on_current_index(client, package_spec))
    return result


def remove_packages(client, package_spec):
    for index in client.list_indices(user=client.user):
        client.use(index)
        client.remove(package_spec)
