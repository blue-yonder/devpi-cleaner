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

Use Cases
=========

* Removing outdated development packages
* Removing packages uploaded by accident
* Removing packages available from other indices

Léon by Example
===============

The following command will delete all development packages preceding version 0.2 of ``delete_me`` in indices of
the user::

    > devpi-cleaner http://localhost:2414/ user 'delete_me<=0.2' --dev-only
    Password:
    Packages to be deleted:
     * http://localhost:2414/user/index2/+f/842/84d1283874110/delete_me-0.2.dev2.tar.gz
     * http://localhost:2414/user/index2/+f/636/95eef6ac86c76/delete_me-0.2.dev2-py2.py3-none-any.whl
     * http://localhost:2414/user/index1/+f/842/84d1283874110/delete_me-0.2.dev2.tar.gz
     * http://localhost:2414/user/index1/+f/636/95eef6ac86c76/delete_me-0.2.dev2-py2.py3-none-any.whl
    Enter "yes" to confirm: yes
    >

As shown, packages will be listed and confirmation required before they are actually deleted from the server.

Commandline Usage
=================
::

    usage: devpi-cleaner [-h] [--batch] [--dev-only] [--force]
                         [--password PASSWORD]
                         server user package_specification

    A utility to clean packages from the Devpi server used at Blue Yonder.

    positional arguments:
      server                The devpi server to operate on.
      user                  The devpi server of which to clean the indices.
      package_specification
                            The specification of the package version(s) to remove.

    optional arguments:
      -h, --help            show this help message and exit
      --batch               Assume yes on confirmation questions.
      --dev-only            Remove only development versions as specified by PEP
                            440.
      --force               Temporarily make indices volatile to enable package
                            removal.
      --password PASSWORD   The password with which to authenticate.

License
=======

`New BSD`_


.. _devpi server: http://doc.devpi.net/latest/
.. _New BSD: https://github.com/blue-yonder/devpi-cleaner/blob/master/COPYING
