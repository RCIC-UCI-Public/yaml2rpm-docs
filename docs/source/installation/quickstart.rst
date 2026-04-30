.. _quickstart:

Quickstart
==========

Yaml2rpm is best built directly from the git repository.  Part of that build process will create RPMs
that can be installed on other machines. On a reasonable system with good network connectivity (or locally-mirrored
repositories) it takes roughly 2 minutes to set up a system to build RPMS using yaml2rpm. We **highly
recommend** that you prepare and build in a :ref:`singularity container<dd_container>`. Like many builds,
the build system itself is modified. In this case, numerous system-level RPMs are added as are newly created RPMs.
Building inside of container protects the physical system from this inevitable change.

Building Yaml2rpm
-----------------


   .. parsed-literal::

      :command:`git clone https://github.com/RCIC-UCI-Public/yaml2rpm`
      :command:`cd yaml2rpm`
      :command:`./first-build.sh`


When the above has completed, you will see the following line of output
   .. code-block:: bash

      === First Build completed ===
      Start a new bash shell or logout/login to make certain all profile.d scripts


As of Rocky 10, 18 RPMs are added to the system during the first-build. Of these, the following
RPMs are built (the rest are OS- or EPEL-supplied packages). The information can be discovered using
``yum history``.

    * ``rocks-devel`` core Makefile structure generate spec files 
    * ``python-ruamel-yaml`` specific YAML parser
    * ``python-ruamel-yaml-clib`` specific YAML parser library
    * ``rcic-module-support``
    * ``rcic-module-path``
    * ``yaml2rpm``

If you don't want to exit the shell, but instead want source profile.d scripts, then do the following

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

