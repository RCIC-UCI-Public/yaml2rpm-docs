.. _requirements:

Requirements
=============

Quickstart
----------

For a quick start testing on a standard CentOS machine 

- If you want to use prebuilt RPMS you can follow :doc:`quickstart`
- If you want to build YAML2RPM RPMS and install them from source repo, see :ref:`building rpm`

Prerequisites
--------------

1. Python 3.

   Required Python modules (provided via OS RPMS):

     - ``argparse``
     - ``socket``
     - ``datetime``. 

   The following  4 Python modules will be automatically
   built and installed during the building step:

     - ``future``: for compatibility of Python 2/3 code
     - ``ruamel-yaml``: used by the  main script :command:`gen-definitions.py`
     - ``ruamle-ycml-clib``: used by the  main script :command:`gen-definitions.py`
     - ``setuptools``: for building Python dependent packages.

#. If you are using a very stripped-down CentOS image (similar to the official CentOS 9 image in Amazon, you will
   want to make certain you have the following packages and package groups installed

   .. code-block:: bash

      yum groupinstall "Development Tools" "Console Internet Tools"
      yum install redhat-lsb wget zlib-devel environment-modules
      . /etc/profile.d/modules.sh

#. Install the development RPMS

   Go to the `Development RPMS repository <https://github.com/RCIC-UCI-Public/development-RPMS>`_ 
   for the latest prebuilt RPMs and instructions. After following those instructions, you can build your first RPM from source.
