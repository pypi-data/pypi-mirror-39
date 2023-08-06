.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============
pdfreactor-api
==============

Python API for PDFreactor (https://www.pdfreactor.com), a HTML-to-PDF processor.

This distribution package is based on the original API module by RealObjects.
To make use of it, you need

- a license key (from RealObjects; see https://www.pdfreactor.com/buy/)
- a running PDFreactor server.


Features
--------

- The module ``pdfreactor.api`` contains the Python API version 6
  (based on ``wrappers/python/lib/PDFreactor.py`` from the PDFreactor tarball),
  suitable for PDFreactor server versions 8 to 10.


Examples
--------

This add-on can be seen in action at the following sites:

- Is there a page on the internet where everybody can see the features?
- https://www.unitracc.de
- https://www.unitracc.com


Documentation
-------------

Full documentation for end users can be found in the "docs" folder.


Installation
------------

Install pdfreactor-api by adding it to your buildout::

    [buildout]

    ...

    eggs =
        pdfreactor-api


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/visaplan/pdfreactor-api/issues
- Source Code: https://github.com/visaplan/pdfreactor-api
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know;
please use the issue tracker mentioned above.


License
-------

The project is licensed under the GPLv2.

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
