=============
Devpi Cleaner
=============

.. image:: https://coveralls.io/repos/blue-yonder/devpi-cleaner/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/r/blue-yonder/devpi-cleaner?branch=master
.. image:: https://badge.fury.io/py/devpi-cleaner.svg
    :alt: Latest Version
    :target: https://pypi.python.org/pypi/devpi-cleaner


Léon, the devpi cleaner, enables batch removal of artefacts from a `devpi server`_. Given a package and version
specification, it will remove the specified versions of a package from either a single index or all indices of a given
user.

Rationale
=========
Devpi cleaner wraps the original `devpi remove` command. It provides the following extensions:

* Conditionally limit removal to development packages.
* Conditionally limit removal to versions matching a given regular expression.
* Temporarily switch non-volatile indices to volatile.
* Apply a remove operation to all indices of a user.
* Throttle removal activities if the Devpi server is having difficulties keeping up.

Léon by Example
===============

The following command will delete all development packages preceding version 0.2 of ``delete_me`` on index `index1` of
the user::

    > devpi-cleaner http://localhost:2414/ user/index1 'delete_me<=0.2' --dev-only
    Password:
    Packages to be deleted from user/index1:
     * delete_me 0.2.dev1 on user/index1
     * delete_me 0.2.dev2 on user/index1
    Cleaning user/index1…
    100% (2 of 2) |###########################| Elapsed Time: 0:00:00 Time: 0:00:00
    >

As shown, packages will be listed and confirmation required before they are actually deleted from the server.

Commandline Usage
=================
::

    usage: devpi-cleaner [-h] [--batch] [--dev-only] [--version-filter REGEX]
                         [--force] [--password PASSWORD] [--login LOGIN]
                         server user[/index] package_specification

    A utility to batch-remove packages from a Devpi server.

    positional arguments:
      server                The devpi server to operate on.
      user[/index]          The index from which to remove the packages. If only
                            the user part is specified, all indices of that user
                            will be cleaned.
      package_specification
                            The specification of the package version(s) to remove.

    optional arguments:
      -h, --help            show this help message and exit
      --batch               Assume yes on confirmation questions.
      --dev-only            Remove only development versions as specified by PEP
                            440.
      --version-filter REGEX
                            Remove only versions in which the given regular
                            expression can be found.
      --force               Temporarily make indices volatile to enable package
                            removal.
      --password PASSWORD   The password with which to authenticate.
      --login LOGIN         The user name to user for authentication. Defaults to
                            the user of the indices to operate on.

    The arguments --dev-only and --version-filter can be combined. In this case
    only packages passing both filters will be removed.

License
=======

`New BSD`_


.. _devpi server: http://doc.devpi.net/latest/
.. _New BSD: https://github.com/blue-yonder/devpi-cleaner/blob/master/COPYING
