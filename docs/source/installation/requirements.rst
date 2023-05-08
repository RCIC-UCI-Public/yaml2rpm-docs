Requirements
=============

.. _requirements:


Quickstart
----------

If you want to use prebuilt RPMS for testing on a standard CentOS machine, you can follow what is below. The following was
tested on the official CentOS 7 Amazon machine image.

If you want to build YAML2RPM RPMS and install them from source repo, see Building

Prerequisites
--------------

1. Python 2 or 3. Required python modules: ``argparse``, ``socket``, ``datetime``. 
   There are 4 python modules that will be automatically
   built and installed during the building step:

   - ``future``: for compatibility of python 2/3 code
   - ``ruamel-yaml`` & ruamle-ycml-clib: used by the  main script ``gen-definitions.py``
   - ``setuptools``: for build python dependent packages.

2. If you are using a very stripped-down CentOS image (similar to the official CentOS 7 image in Amazon, you will
   want to make certain you have the following packages and package groups installed

   .. code-block:: bash

      yum groupinstall "Development Tools" "Console Internet Tools"
      yum install redhat-lsb wget zlib-devel environment-modules
      . /etc/profile.d/modules.sh

3. Install the development RPMS

   Go to the `Development RPMS repository <https://github.com/RCIC-UCI-Public/development-RPMS>`_ 
   for the latest prebuilt RPMs and instructions. After following those instructions, you can build your first RPM from source.


