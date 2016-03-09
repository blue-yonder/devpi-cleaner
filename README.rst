=============
Devpi Cleaner
=============

.. image:: https://travis-ci.org/blue-yonder/devpi-cleaner.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/blue-yonder/devpi-cleaner
.. image:: https://coveralls.io/repos/blue-yonder/devpi-cleaner/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/r/blue-yonder/devpi-cleaner?branch=master
.. image:: https://badge.fury.io/py/devpi-cleaner.svg
    :alt: Latest Version
    :target: https://pypi.python.org/pypi/devpi-cleaner
.. image:: https://requires.io/github/blue-yonder/devpi-cleaner/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/blue-yonder/devpi-cleaner/requirements/?branch=master


Léon, the devpi cleaner, helps to batch removal of files from a `devpi server`_. Given a package and version specification
it will remove the specified versions of a package from all indices of a given user.

Rationale
=========
Devpi cleaner wraps the original `devpi remove` command. It provides the following extensions:

* Conditionally limit removal to development packages.
* Conditionally limit removal to versions matching a given regular expression.
* Temporarily switch non-volatile indices to volatile.
* Apply a remove operation to all indices of a user.

Léon by Example
===============

The following command will delete all development packages preceding version 0.2 of ``delete_me`` in indices of
the user::

    > devpi-cleaner http://localhost:2414/ user 'delete_me<=0.2' --dev-only
    Password:
    Packages to be deleted:
     * delete_me 0.2.dev2 on user/index1
     * delete_me 0.2.dev2 on user/index2
    Enter "yes" to confirm: yes
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

License
=======

`New BSD`_


.. _devpi server: http://doc.devpi.net/latest/
.. _New BSD: https://github.com/blue-yonder/devpi-cleaner/blob/master/COPYING
