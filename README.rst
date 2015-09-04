============
crux
============

A Python client library for Adobe Experience Manager CRX package manager.

Features
========

* List uploaded packages
* Extract packages from CRX into a file


.. Installation
   ============

   .. code:: python

    pip install circleclient


Usage
=====

Retrieve a package list
-------------------------------

.. code:: python

    from crux import crux

    c = crux.CrxPackageClient('http://192.168.99.100:4502', 'admin', 'password')

    # Retrieve a list of packages
    package_list = c.list_packages()


Download a package
-------------------------------

.. code:: python

    from crux import crux

    c = crux.CrxPackageClient('http://192.168.99.100:4502', 'admin', 'password')

    # Retrieve a package as a file-like object
    f = c.export_package('place/group/here',
                         'package-pkg-1.0.205.zip')
