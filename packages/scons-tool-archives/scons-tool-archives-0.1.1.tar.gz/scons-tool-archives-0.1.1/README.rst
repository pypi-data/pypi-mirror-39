scons-tool-archives
===================

.. image:: https://badge.fury.io/py/scons-tool-archives.svg
    :target: https://badge.fury.io/py/scons-tool-archives
    :alt: PyPi package version

.. image:: https://travis-ci.org/ptomulik/scons-tool-archives.svg?branch=master
    :target: https://travis-ci.org/ptomulik/scons-tool-archives
    :alt: Travis CI build status

.. image:: https://ci.appveyor.com/api/projects/status/github/ptomulik/scons-tool-archives?svg=true
    :target: https://ci.appveyor.com/project/ptomulik/scons-tool-archives

SCons_ tool to create archives.

Installation
------------

There are few ways to install this tool for your project.

From pypi_
^^^^^^^^^^

This method may be preferable if you build your project under a virtualenv. To
add archives tool from pypi_, type (within your wirtualenv):

.. code-block:: shell

   pip install scons-tool-loader scons-tool-archives

or, if your project uses pipenv_:

.. code-block:: shell

   pipenv install --dev scons-tool-loader scons-tool-archives

Alternatively, you may add this to your ``Pipfile``

.. code-block::

   [dev-packages]
   scons-tool-loader = "*"
   scons-tool-archives = "*"


The tool will be installed as a namespaced package ``sconstool.archives``
in project's virtual environment. You may further use scons-tool-loader_
to load the tool.

As a git submodule
^^^^^^^^^^^^^^^^^^

#. Create new git repository:

   .. code-block:: shell

      mkdir /tmp/prj && cd /tmp/prj
      touch README.rst
      git init

#. Add the `scons-tool-archives`_ as a submodule:

   .. code-block:: shell

      git submodule add git://github.com/ptomulik/scons-tool-archives.git site_scons/site_tools/archives

#. For python 2.x create ``__init__.py`` in ``site_tools`` directory:

   .. code-block:: shell

      touch site_scons/site_tools/__init__.py

   this will allow to directly import ``site_tools.archives`` (this may be required by other tools).

Usage example
-------------

A simple ``SConstruct`` which creates tar archive named ``foo.tar`` containning
two files: ``foo.c`` and ``foo.h``.

.. code-block:: python

    # TODO: uncomment following lines if the tool is installed via pip/pipenv
    # import sconstool.loader
    # sconstool.loader.extend_toolpath(transparent=True)
    env = Environment(tools=['archives'])
    env.TarFile('foo.tar', ['foo.c', 'foo.h'])

Details
-------

Module description
^^^^^^^^^^^^^^^^^^

The scons-tool-archives_ tool provides builders to create archives, such as tar
or zip files. Currently two builders are implemented

- ``TarFile`` - uses `Python tarfile`_ library to create tar archives,
- ``ZipFile`` - uses `Python zipfile`_ library to create zip archives.

Construction variables
^^^^^^^^^^^^^^^^^^^^^^

There are several construction variables used by the builders. Variables
with names starting with ``TARFILE`` are used by the ``TarFile`` builder,
variables starting with ``ZIPFILE`` are used by the ``ZipFile`` builder.

========================= =============================================
Variable                   Default
========================= =============================================
 TARFILESUFFIX             ``.tar``
 TARFILETRANSFORM
 TARFILEMAPPINGS
 TARFILEMODE
 TARFILEBUFSIZE
 TARFILECOMPRESSLEVEL
 TARFILEFORMAT
 TARFILEDEREFERENCE
 TARFILEDEBUG
 TARFILEENCODING
 TARFILEERRORS
 ZIPFILESUFFIX             ``.zip``
 ZIPFILETRANSFORM
 ZIPFILEMAPPINGS
 ZIPFILEMODE
 ZIPFILECOMPRESSION
 ZIPFILEALLOW64
 ZIPFILECOMPRESSLEVEL
========================= =============================================


LICENSE
-------

Copyright (c) 2018 by Pawel Tomulik <ptomulik@meil.pw.edu.pl>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE

.. _SCons: http://scons.org
.. _Swig: http://swig.org
.. _pipenv: https://pipenv.readthedocs.io/
.. _pypi: https://pypi.org/
.. _scons-tool-archives: https://github.com/ptomulik/scons-tool-archives
.. _scons-tool-loader: https://github.com/ptomulik/scons-tool-loader
.. _Python tarfile: https://docs.python.org/3/library/tarfile.html
.. _Python zipfile: https://docs.python.org/3/library/zipfile.html

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->
