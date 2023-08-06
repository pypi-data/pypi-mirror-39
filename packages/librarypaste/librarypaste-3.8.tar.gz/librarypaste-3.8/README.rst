.. image:: https://img.shields.io/pypi/v/librarypaste.svg
   :target: https://pypi.org/project/librarypaste

.. image:: https://img.shields.io/pypi/pyversions/librarypaste.svg

.. image:: https://img.shields.io/travis/yougov/librarypaste/master.svg
   :target: https://travis-ci.org/yougov/librarypaste

.. .. image:: https://img.shields.io/appveyor/ci/jaraco/skeleton/master.svg
..    :target: https://ci.appveyor.com/project/jaraco/skeleton/branch/master

.. .. image:: https://readthedocs.org/projects/skeleton/badge/?version=latest
..    :target: https://skeleton.readthedocs.io/en/latest/?badge=latest

Usage
=====

Launch with the ``librarypaste``
command or with ``python -m librarypaste``. The library will host the service
on ``[::0]:8080`` by default. Pass cherrypy config files on the command line
to customize behaivor.

By default, the server saves pastes to the file system  in ``./repo`` using the
JSON store, but there is support for a MongoDB backend as well.

See also `lpaste <https://pypi.org/project/lpaste>`_ for a Python-based
client (including a clipboard helper) and Mac OS X App.
