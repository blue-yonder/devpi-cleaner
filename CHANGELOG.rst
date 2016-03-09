=========
Changelog
=========

This is the version history of `devpi_cleaner`.

Version 0.2.0
=============

* Allow cleaning of single indices instead of all indices of a user. See ``--help`` for the invocation syntax.
* Allow to limit the versions to delete via a regular expression.
* Prompt the user for a list of package versions and the indices from which to delete them. Previously the user was
  shown a list of package URLs. However, `devpi_cleaner` will actually delete by package version, not by uploaded file.
* Display a progress bar while performing the removal if multiple packages or package versions are selected.
* Python 3.2 is no longer supported
* Python 3.5 is now officially supported
* PyPy is now officially supported

Version 0.1.1
=============

* Add support for HTTPS.

Version 0.1.0
=============

* Initial release
