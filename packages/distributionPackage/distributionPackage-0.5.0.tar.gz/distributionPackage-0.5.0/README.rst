distributionPackage
-------------------

|pipeline| |coverage|

.. |pipeline| image:: https://gitlab.com/blueskyjunkie/distribution-package/badges/master/pipeline.svg
   :target: https://gitlab.com/blueskyjunkie/distribution-package/commits/master
   :alt: pipeline status

.. |coverage| image:: https://gitlab.com/blueskyjunkie/distribution-package/badges/master/coverage.svg
   :target: https://gitlab.com/blueskyjunkie/distribution-package/commits/master
   :alt: coverage report

|pypiVersion| |doi0.4.0|

.. |pypiVersion| image:: https://badge.fury.io/py/distributionPackage.svg
   :target: https://badge.fury.io/py/distributionPackage
   :alt: PyPI version


A tool for packaging a set of files for distribution using a YAML manifest definition from the
`packageManifest project <https://gitlab.com/blueskyjunkie/package-manifest>`_.

.. contents::

.. section-numbering::


Main Features
=============

* Simple default operation
* zip or tar-gzip package generation (or both)
* Specify project path to build package from
* Append manifest files to an existing tar or zip package


Installation
============

The simplest way to acquire ``distributionPackage`` is using ``pip``.

.. code-block:: bash

   pip install distributionPackage

It's highly recommended that you install the package into a
`Python virtual environment <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.


Getting Started
===============

Define a package manifest in a YAML file. The default name expected by ``distributionPackage`` is ``manifest.yml``. The example
below constructs a simple manifest for a hypothetical C++ project.

.. code-block:: yaml

   - include:
       files: [ 'README.md', 'LICENSE', 'VERSION' ]
   - global-include:
       files: [ '*.h', '*.cpp' ]
   - prune:
       directory: 'scripts'

Assuming that you have installed ``distributionPackage`` and that the ``makePackage`` command is in your path,

.. code-block:: bash

   makePackage

By default ``makePackage`` will acquire the manifest definitions from ``./manifest.yml``, output a file
``distribution-out.tar.gz`` in the current directory and assume that the current directory is the root directory of the
project to be packaged (for the basis of constructing the package file names from the manifest).

.. code-block:: bash

   makePackage --help

Using the ``--help`` option will describe the various options available.


DOI Archive
===========

.. |doi0.3.0| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1166222.svg
   :target: https://doi.org/10.5281/zenodo.1166222
   :alt: doi v0.3.0

*DOI v0.3.0* |doi0.3.0|

.. |doi0.4.0| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1173381.svg
   :target: https://doi.org/10.5281/zenodo.1173381
   :alt: doi v0.4.0
