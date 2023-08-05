pub2
====

Pub2 is a self-publishing framework.

.. image:: https://img.shields.io/github/stars/iandennismiller/pub2.svg?style=social&label=GitHub
    :target: https://github.com/iandennismiller/pub2

.. image:: https://img.shields.io/pypi/v/pub2.svg
    :target: https://pypi.python.org/pypi/pub2

.. image:: https://readthedocs.org/projects/pub2/badge/?version=latest
    :target: http://pub2.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/iandennismiller/pub2.svg?branch=master
    :target: https://travis-ci.org/iandennismiller/pub2

.. image:: https://coveralls.io/repos/github/iandennismiller/pub2/badge.svg?branch=master
    :target: https://coveralls.io/github/iandennismiller/pub2?branch=master

Overview
--------

Pub2 is a self-publishing framework.  It integrates with Jekyll to provide LaTeX publishing.

macOS Quick Start
^^^^^^^^^^^^^^^^^

The following commands install pub2 and its dependencies (TeX Live and ImageMagick).

::

    brew cask install mactex
    brew install https://raw.githubusercontent.com/iandennismiller/pub2/master/etc/pub2.rb

To demonstrate pub2, the following commands initialize the current directory and build a sample.  The results appear in the `pub2` folder.

::

    pub2 init
    pub2 build
    open pub2/*.pdf

Installation
^^^^^^^^^^^^

pub2 can be installed using pip.  This works well with virtualenv.

::

    pip install pub2

See :doc:`installation` to install on macOS, Windows, and Linux (Debian/Ubuntu or Redhat/CentOS).

Documentation
^^^^^^^^^^^^^

http://pub2.readthedocs.io
