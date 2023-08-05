This package defines the (console) script ``ztest``, a small wrapper
around the Zope (3) testrunner to run tests of Zope (2) application components
(often so called Zope (2) products).

Until Zope 2.11, its functionality was available as ``bin/zopectl test``.
For Zope 2.12,
Zope developers switched to ``buildout`` for Zope development itself
and (to save some work) dropped support for ``bin/zopectl test``.
Thus, developers of Zope application components (like me) were forced
either to switch to ``buildout``, to renounce testing or to build something
like ``ztest``.

My experience with ``buildout`` has not been good: compared with
a more traditional (and more manual) ``virtualenv``,
``buildout`` gave me much more surprises (surprising upgrades),
much more waiting time due to unnecessary rebuildings and was
far less reliable (due to problems of internet servers scanned for
sources). Therefore, I do not want to switch to ``buildout``.
Of course, I do not want to renounce testing.
Thus, I stiched the Zope 2.11 code together to build ``ztest``.

``ztest`` can also be used together with ``buildout``.
A ``buildout`` part definition for ``ztest`` could look like::

  [ztest]
  recipe = zc.recipe.egg:scripts
  eggs =
    dm.zopepatches.ztest
    ${buildout:eggs}
  extra-paths =
    ${zope2:location}/lib/python

It creates a script ``bin/ztest`` that can test packages either in
Zope or in the available eggs.


Basic usage
===========

ztest -h
  list the available options

ztest [--config-file *config_file*] -s *package*
  run tests for *package*. If given, use *config_file* as the Zope
  configuration file

ztest [--config-file *config_file*] --package-path *file_path_to_package* *package* -s *package*
  occationally, the testrunner is too stupid to find the tests in a package.
  Then it is necessary to specify its file path with the ``--package-path``
  option.


History
=======

2.0
  Python 3/Zope4+ compatibility

  Requiring modern ``zope.testrunner`` (>= 4.9). This makes
  this release Python 3 (>= 3.3) and Python 2.7 only.

  New command line option ``--logging`` to activate basic logging.

1.1.3
  Bugfix: a module filter was usually not effective

1.1.2
  support for Zope 2.10

1.1
  try to determine 'package-path' automatically by a trial import. May not always work.
