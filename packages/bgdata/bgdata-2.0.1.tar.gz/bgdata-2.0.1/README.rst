
.. _readme:

BGDATA
======

.. |bgdata| replace:: **bgdata**

|bgdata| is a simple data package manager.
What is gives is essentially a path to a certain data package.
The package is specified by 4 layers: *project*, *dataset*, *version* and *build*.



Installation
------------

|bgdata| is written in Python and requires Python>=3.4.

|bgdata| can be installed through ``pip``

.. code-block:: bash

   pip install bgdata

or by conda:

.. code-block:: bash

   conda install -c bbglab bgdata



How it works
------------

|bgdata| is configured to have a remote and a local repository where to look for data packages.
When |bgdata| is asked to get a certain package it checks whether
it is in the local repo. If not present, it is downloaded from the remote.

If the *build* is not specified, |bgdata| returns the latest.

|bgdata| can do more things such as work in offline mode or be configured
to use a different path for certain files.

You can find out more in the documentation.


Using bgdata
------------

|bgdata| is a Python package that can be used from Python or from
a bash shell using its command line interface.

From Python it is as simple as using the ``get_path`` function:

.. code-block:: python

   import bgdata
   bgdata.get_path('project', 'dataset', 'version', 'build')

From the command line is is equally simple:

.. code-block:: bash

   bgdata project dataset version build

.. note:: *build* is optional and if not indicated the latest build is used


License
-------

`LICENSE <LICENSE.txt>`_.
