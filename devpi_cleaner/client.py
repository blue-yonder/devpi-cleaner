# coding=utf-8


def _list_packages_on_current_index(client, package_spec):
    return [
        package_url
        for package_url in client.list(package_spec)
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
