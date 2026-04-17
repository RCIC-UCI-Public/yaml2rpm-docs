.. _quickstart:

Quickstart
==========

If you want to use prebuilt RPMs for testing on a standard CentOS machine, you can follow what is below. The following was
tested on the official Rocky 9 machine image.

If you want to build YAML2RPM RPMs and install them from source repo, see Building section.

**Prerequisites**

1. Python 3 modules

   Required modules are provided by the ``python3-libs`` RPM:

     - ``argparse``
     - ``socket``
     - ``datetime`` 

2. Rocky 9 packages and groups

   If you are using a very stripped-down CentOS image (similar to the official Rocky Linux 9 image in Amazon, you will
   want to make certain you have the following packages and package groups installed
   
     .. parsed-literal::
        :command:`yum groupinstall "Development Tools"`
        :command:`yum install wget zlib-devel environment-modules`
        :command:`. /etc/profile.d/modules.sh`

3. Install the development RPMs

   Go to the `Development RPMs <https://github.com/RCIC-UCI-Public/development-RPMS#development-rpms/>`_ repository 
   for the latest prebuilt RPMs and instructions. After following those instructions, you can build your first RPM from source.

.. _building rpm:

Building
----------

You may want to build the YAML2RPM RPMs and install them from the source git repository.
Do the following in the top-level directory
You will need to set DISPLAY prior to doing this so that Firefox can ask for your permission to read public data.

   .. parsed-literal::
      :command:`./first-build.sh`

After this step is complete the following RPMs are built and installed:

  * Needed Python modules for your default system Python install:

    | ``python-future`` for Python 2/3 compatibility
    | ``python-setuptools`` for building Python packages
    | ``python-ruamel-yaml`` specific YAML parser
    | ``python-ruamel-yaml-clib`` specific YAML parser library
 
  * These RPMS provide all the building structure and support files for
    the packages builds. They include a couple of profiles files that are added to the ``/etc/profile.d``.

    | ``rcic-module-support``
    | ``rcic-module-path``
    | ``yaml2rpm``



In order to proceed with next steps simply execute the following profiles scripts 
(for future logins they will be automatically sourced by the login shell):

   .. parsed-literal::
      :command:`. /etc/profile.d/rcic-modules.sh`
      :command:`. /etc/profile.d/yaml2rpm.sh`


A simple test build
^^^^^^^^^^^^^^^^^^^

:red:`TODO: remove this section, outdated`

For a very simple build of an RPM, create a working directory *workdir*. And then
download the source tarball into the workdir/sources directory. Then create the RPM for ``cmake``,
it will be placed in *workdir/RPMS/x86_64*:

.. code-block:: bash

   mkdir -p workdir/yamlspecs
   cd workdir/yamlspecs; cp /opt/rocks/yaml2rpm/samples/* .
   make download PKG=cmake
   make download PKG=scons
   make

At the end of the process, you should have 4 RPMs in *workdir/RPMS/x86_64/*. You could install them on the local machine
and have an updated version of ``cmake`` and ``scons``, and corresponding environment modules. 
For example, the module for ``cmake`` can be loaded in order to use ``cmake``:

.. code-block:: bash

   module load cmake
   which cmake


The version of ``cmake`` is defined in the ``versions.yaml`` file, if you wanted to update the version, you could edit that file,
download the new source tarball directly from the source website and then rebuild a new package via

.. code-block:: bash

   make download PKG=cmake
   make cmake.pkg
   make cmake-module.pkg

