scons-tool-kpsewhich
====================

.. image:: https://badge.fury.io/py/scons-tool-kpsewhich.svg
    :target: https://badge.fury.io/py/scons-tool-kpsewhich
    :alt: PyPi package version

.. image:: https://travis-ci.org/ptomulik/scons-tool-kpsewhich.svg?branch=master
    :target: https://travis-ci.org/ptomulik/scons-tool-kpsewhich
    :alt: Travis CI build status

.. image:: https://ci.appveyor.com/api/projects/status/github/ptomulik/scons-tool-kpsewhich?svg=true
    :target: https://ci.appveyor.com/project/ptomulik/scons-tool-kpsewhich

This tool provides `SCons`_ with interface to kpsewhich utility. The kpsewhich
program is a part of `kpathsea`_ library, which in turn is a part of TeX Live
distribution. Its purpose is to search within the `TeX directory structure`_
(TDS) for files such as TeX classes, styles, BibTeX databases, fonts etc. For
more informations see `kpathsea manual`_ and informations about `TeX directory
structure`_ (TDS).

This tool appends new methods to the SCons Environment. It does not provide any
builders, but rather equips SCons Environment with methods that call
``kpsewhich`` program during the SConscript-reading phase. This tool does not
produce any files, it is thought as an extension for obtaining textual
information from external program.

INSTALLATION
------------

There are few ways to install this tool for your project.

From pypi_
^^^^^^^^^^

This method may be preferable if you build your project under a virtualenv. To
add kpsewhich tool from pypi_, type (within your wirtualenv):

.. code-block:: shell

   pip install scons-tool-loader scons-tool-kpsewhich

or, if your project uses pipenv_:

.. code-block:: shell

   pipenv install --dev scons-tool-loader scons-tool-kpsewhich

Alternatively, you may add this to your ``Pipfile``

.. code-block::

   [dev-packages]
   scons-tool-loader = "*"
   scons-tool-kpsewhich = "*"


The tool will be installed as a namespaced package ``sconstool.kpsewhich``
in project's virtual environment. You may further use scons-tool-loader_
to load the tool.

As a git submodule
^^^^^^^^^^^^^^^^^^

#. Create new git repository:

   .. code-block:: shell

      mkdir /tmp/prj && cd /tmp/prj
      touch README.rst
      git init

#. Add the `scons-tool-kpsewhich`_ as a submodule:

   .. code-block:: shell

      git submodule add git://github.com/ptomulik/scons-tool-kpsewhich.git site_scons/site_tools/kpsewhich

#. For python 2.x create ``__init__.py`` in ``site_tools`` directory:

   .. code-block:: shell

      touch site_scons/site_tools/__init__.py

   this will allow to directly import ``site_tools.kpsewhich`` (this may be required by other tools).


USAGE EXAMPLES
--------------

Find files ``article.cls`` and ``amsmath.sty`` used by ``latex``:

.. code-block:: python

    env = Environment(tools = ['tex', 'kpsewhich'])
    files = env.KPSFindFiles(['article.cls','amsmath.sty'], progname='$LATEX')

Find all occurrences of ``unicode.sty`` file in TDS:

.. code-block:: python

    env = Environment(tools = ['kpsewhich'])
    files = env.KPSFindAllFiles('unicode.sty')

Other functions (correspond directly to ``kpsewhich`` function options):

.. code-block:: python

    texmf = env.KPSExpandBraces('a{b,c}d')# kpsewhich -expand-braces 'a{b,c}d'
    texmf = env.KPSExpandPath('$TEXMF')   # kpsewhich -expand-path '$TEXMF'
    texmf = env.KPSExpandVar('$TEXMF')    # kpsewhich -expand-var '$TEXMF'
    texpath = env.KPSShowPath('tex')      # kpsewhich -show-path 'tex'
    home = env.KPSVarValue('TEXMFHOME')   # kpsewhich -var-value 'TEXMFHOME'



CONSTRUCTION VARIABLES
----------------------

The following construction variables may be used to configure the ``kpsewhich``
tool. They may be also provided as keyword arguments to ``KPSXxx()`` methods.

============================== ==============================================
        Variable                                Description
============================== ==============================================
 ``KPSEWHICH``                    the ``kpsewhich`` executable
------------------------------ ----------------------------------------------
 ``KPSEWHICHFLAGS``               additional flags to ``kpsewhich``
------------------------------ ----------------------------------------------
 ``KPSVARIABLES``                 (re)define variables for ``kpsewhich``
============================== ==============================================

``KPSVARIABLES`` must be a dictionary in form ``{ NAME : VALUE }``,
for example:

.. code-block:: python

  KPSVARIABLES = {"TEXMFHOME" : "/home/ptomulik/texmf"}

ARGUMENTS
---------

These arguments are accepted by some ``KPSXxx()`` methods. All the methods accept
``progname``. All other arguments are accepted by ``KPSFindFiles`` and
``KPSFindAllFiles``.

============================== ==============================================
        Variable                                Description
============================== ==============================================
 ``dpi``                         corresponds to ``-dpi`` flag,
------------------------------ ----------------------------------------------
 ``format``                      corresponds to ``-format`` flag,
------------------------------ ----------------------------------------------
 ``path``                        corresponds to ``-path`` flag
------------------------------ ----------------------------------------------
 ``progname``                    corresponds to ``-progname`` flag
------------------------------ ----------------------------------------------
 ``subdir``                      corresponds to ``-subdir`` flag
============================== ==============================================


LICENSE
-------
Copyright (c) 2013-2018 by Pawel Tomulik

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
.. _SCons test framework: https://bitbucket.org/dirkbaechle/scons_test_framework
.. _mercurial: http://mercurial.selenic.com/
.. _TeX directory structure: http://tug.org/twg/tds/
.. _kpathsea: http://tug.org/kpathsea/
.. _kpathsea manual: http://tug.org/texinfohtml/kpathsea.html
.. _pipenv: https://pipenv.readthedocs.io/
.. _pypi: https://pypi.org/
.. _scons-tool-loader: https://github.com/ptomulik/scons-tool-loader/

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->
