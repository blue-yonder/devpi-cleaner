# coding=utf-8
import re
import time

from devpi_plumber.client import volatile_index, DevpiClientError

_TAR_GZ_END = '.tar.gz'
_TAR_BZ2_END = '.tar.bz2'
_ZIP_END = '.zip'


def _extract_name_and_version(filename):
    if filename.endswith('.whl') or filename.endswith('.egg'):
        return filename.split('-')[:2]
    else:
        name, version_and_ext = filename.rsplit('-', 1)
        if not version_and_ext[0].isdigit():  # setuptools-scm on old setuptools separates local part via dash.
            parts = filename.split('-')
            name = '-'.join(parts[:-2])
            version_and_ext = '-'.join(parts[-2:])
        for extension in (_TAR_GZ_END, _TAR_BZ2_END, _ZIP_END):
            if version_and_ext.endswith(extension):
                return name, version_and_ext[:-len(extension)]
        raise NotImplementedError('Unknown package type. Cannot extract version from {}.'.format(filename))


class Package(object):
    def __init__(self, package_url):
        parts = package_url.rsplit('/', 6)  # example URL http://localhost:2414/user/index1/+f/45b/301745c6d8bbf/delete_me-0.1.tar.gz
        self.index = parts[1] + '/' + parts[2]
        self.name, self.version = _extract_name_and_version(parts[-1])

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


def _list_packages_on_index(client, index, package_spec, only_dev, version_filter):
    if version_filter is not None:
        version_filter = re.compile(version_filter)

    def selector(package):
        return (
            package.index == index and
            (not only_dev or package.is_dev_package) and
            (version_filter is None or version_filter.search(package.version))
        )

    client.use(index)

    all_packages = {
        Package(package_url) for package_url in client.list('--index', index, '--all', package_spec)
        if package_url.startswith('http://') or package_url.startswith('https://')
    }

    return set(filter(selector, all_packages))


def _get_indices(client, index_spec):
    spec_parts = index_spec.split('/')
    if len(spec_parts) > 1:
        return [index_spec, ]
    else:
        return client.list_indices(user=index_spec)


def list_packages_by_index(client, index_spec, package_spec, only_dev, version_filter):
    return {
        index: _list_packages_on_index(client, index, package_spec, only_dev, version_filter)
        for index in _get_indices(client, index_spec)
    }


def get_index_queue_size(metrics):
    for metric_name, _, value in metrics:
        if metric_name == "devpi_web_whoosh_index_queue_size":
            return value
    return 0


def wait_for_sync(client):
    """Deletion can cause significant load on the replicas, thus we need a way to wait for them to be in sync"""
    now = start = time.time()
    while now < start + 1800:  # up to 30 minutes
        status = client.get_json('/+status')['result']
        last_in_sync = float(status.get('replica-in-sync-at', now))
        indexer_queue_size = get_index_queue_size(status.get('metrics', []))
        if last_in_sync > now - 60 and indexer_queue_size < 100:
            # We are neither talking to a lagging replica nor is the instance
            # swamped with items to index. Should be fine to add some load.
            return
        # Wait for Devpi to catch up
        time.sleep(10)
        now = time.time()
    # At some point we just have to continue, maybe we are lucky and this goes through
    return


def remove_package(client, package):
    client.remove('--index', package.index, '{name}=={version}'.format(name=package.name, version=package.version))


def remove_packages(client, index, packages, force):
    with volatile_index(client, index, force):
        for package in packages:
            assert package.index == index
            wait_for_sync(client)
            remove_package(client, package)
