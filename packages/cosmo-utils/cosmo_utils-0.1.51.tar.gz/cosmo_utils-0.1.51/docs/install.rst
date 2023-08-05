.. _step_by_step_install:

********************
Package Installation
********************

To install Cosmo-Utils, you can use `pip` or clone the repository from 
Github and build the source code.

Using pip
=========

The simplest way to install `Cosmo-Utils` is with pip. To install it with 
pip ::
    
    pip install cosmo-utils

This will install the latest official release of the code.

Upgrading via pip
-----------------

Whenever there is a new release, you can upgrade your current version by 
running ::

    pip install --upgrade cosmo-utils

This will ensure that you have the most up-to-date version of `Cosmo-Utils`.

Building from Source
======================

If you don't install the latest relases using pip,
you can instead clone the source code and call the setup file.
This is the most common way to install `Cosmo-Utils` if you want 
versions of the code that have been updaed since the latest official
release. In this case, after installation it is particularly important
that you follow the instructions in :ref:`verifying_your_installation` 
section below.

The first step is to clone the `Cosmo-Utils` repository::

    git clone https://github.com/vcalderon2009/cosmo_utils
    cd cosmo_utils

Installing one of the official relases
--------------------------------------

All official releases of the code are tagged with their version name, 
e.g. v0.1.0. To install a particular release::

    git checkout v0.1.0
    python setup.py install

This will install the v0.1.0 release of the code. Other official release 
versions (e.g. 0.1.1) can be installed similarly.

Installing the most recent master branch
-----------------------------------------

If you prefer to use the most recent version of the code::

    git checkout master
    python setup.py install

This will install the master branch of the code that is currently under 
development. While the features in the official releases have a stable 
API, new features being developed in the master branch may not.
However, the master branch may have new features and/or performance 
enhancements that you may wish to use for your science application.
A concerted effort is made to ensure that only thoroughly tested and 
documented code appears in the public master branch, though `Cosmo-Utils`
users should be aware of the distinction between the bleeding edge 
version in master and the official release version available through pip.

.. _verifying_your_installation:

Verifying your installation
==============================

After installing the code and its dependencies, fire up a Python interpreter
and check that the version number matches what you expect:

.. code-block:: python

    import cosmo_utils
    print(cosmo_utils.__version__)

If the version number is not what it should be, this likely means you have a 
previous installation that is superseding the version you tried to install.
This *should* be accomplished by doing `pip uninstall cosmo-utils`
before your new installation, but you may need to uninstall the previous 
build "manually". Like all python packages, you can find the installation 
location as follows:

.. code-block:: python

    import cosmo_utils
    print(cosmo_utils.__file__)

This wil show where your active version is located on your machine. You 
can manually delete this copy of `Cosmo-Utils` prior to your new installation
to avoid version conflicts. (There may be multiple copies of `Cosmo-Utils` in 
this location, depending on how many times you have previously installed 
the code - all such copies my be deleted prior to reinstallation).
