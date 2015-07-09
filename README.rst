=============
Devpi Cleaner
=============

A utility to clean packages from a devpi server. Given a package and version specification it will remove the package
from all indices of a given user.

Use Cases
=========

* Removing outdated development packages
* Removing packages uploaded by accident
* Removing packages available from other indices

Example Usage
=============

The following command will delete all development packages preceding version 4.0 of ``some_package`` in indices of
the user::

    devpi-cleaner --dev-only http://localhost:3141/ User Password 'some_package<4.0'

Packages will be listed and confirmation required before they are actually deleted from the server.
