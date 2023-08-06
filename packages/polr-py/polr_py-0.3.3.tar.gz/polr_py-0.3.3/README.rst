====
polr
====


.. image:: https://img.shields.io/pypi/v/polr.svg
        :target: https://pypi.python.org/pypi/polr-py

.. image:: https://img.shields.io/travis/kylie-a/polr.svg
        :target: https://travis-ci.org/kylie-a/polr-py

.. image:: https://readthedocs.org/projects/polr/badge/?version=latest
        :target: https://polr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/kylie-a/polr/shield.svg
     :target: https://pyup.io/repos/github/kylie-a/polr-py/
     :alt: Updates



Python CLI for the Polr link shortener


* Free software: MIT license
* Documentation: https://polr.readthedocs.io.


Features
--------

* TODO

CLI Usage
=========

.. code-block::

   polr [OPTIONS] COMMAND [ARGS]...

Commands for using the Go link shortening service.

Options:

- ``--help``:  Show this message and exit.

Commands:

- ``exists``:   Check to see if a link with the given ending already exists.
- ``shorten``:  Shorten a link with the option to give it a custom ending.


``shorten``
-----------

Usage:

    polr shorten [OPTIONS] URL

Shorten a link with the option to give it a custom ending. Checks to see
if a link with the given ending exists. Can be configured to fail if it
already exists with ``[-f|--fail]``.

.. code-block::

   polr shorten URL [(-e|--ending=)ending] [(-f|--fail)]`

Examples:

.. code-block::

   # Use default ending
   $ polr shorten https://example.com
   http://polr.example.com/ad14gfwe

   # Use custom ending, if ending already exists don't return error, return link with that ending.
   polr shorten https://example.com -e my-custom-ending
   http://polr.example.com/my-custom-ending

   # Use custom ending, return error if it already exists.
   polr shorten https://example.com -e my-custom-ending -f
   ERROR: link with ending my-custom-ending already exists
   echo "$?"
   1

Options:

- ``-e, --ending TEXT``  A custom ending for the shortened link.
- ``-f, --fail``         Return an error if a link with the desired custom ending already exists
- ``--help``             Show this message and exit.

#### `exists`

Usage:

    polr exists [OPTIONS] ENDING

Check to see if a link with the given ending already exists. Exits with status code 1 if it exists

Examples:

.. code-block:: console

   # Doesn't exist
   $ polr exists my-new-ending
   False
   $ echo "$?"
   0

   # Exists
   $ polr exists my-existing-ending
   True
   $ echo "$?"
   1

Options:

- ``--help``:  Show this message and exit.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
