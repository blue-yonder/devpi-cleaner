=============
Devpi Cleaner
=============

Léon, the devpi cleaner, helps to batch remove files from a devpi server. Given a package and version specification it
will remove the specified versions of a package from all indices of a given user.

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

License
=======

`New BSD`_


.. _New BSD: https://github.com/blue-yonder/devpi-cleaner/blob/master/COPYING
