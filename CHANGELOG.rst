=========
Changelog
=========

This is the version history of `devpi_cleaner`.


UNRELEASED
==========

Added
-----

* Python 3.10 is now officially supported.

Removed
-------

* Python 3.6 is no longer supported.


Version 0.3.0 - 2021-02-05
==========================

Added
-----

* Throttle deletion if Devpi seems under heavy load.
* Python 3.6 to 3.9 are now officially supported.

Changed
-------

* Tests are now executed via pytest to avoid compatibility problems with Python 3.10.

Removed
-------

* Python 2.7, and 3.3 to 3.5 are no longer supported.


Version 0.2.0 - 2016-04-08
==========================

Added
-----

* Allow cleaning of single indices instead of all indices of a user. See ``--help`` for the invocation syntax.
* Allow to limit the versions to delete via a regular expression.
* Display a progress bar while performing the removal if multiple packages or package versions are selected.
* Python 3.5 is now officially supported
* PyPy is now officially supported

Changed
-------

* Prompt the user for a list of package versions and the indices from which to delete them. Previously the user was
  shown a list of package URLs. However, `devpi_cleaner` will actually delete by package version, not by uploaded file.
* Improved performance when deleting multiple package versions from non-volatile indices
* Changelog is now maintained in the format suggested by http://keepachangelog.com/.

Removed
-------

* Python 3.2 is no longer supported


Version 0.1.1 - 2015-11-23
==========================

Added
-----

* Add support for HTTPS.


Version 0.1.0 - 2015-07-17
==========================

Added
-----

* Batch removal of packages from all indices of a Devpi user
* Allow restricting removal to development versions
* Enable removal of packages from non-volatile indices
* Batch mode for non-interactive operation
