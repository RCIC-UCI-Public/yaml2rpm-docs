GCC
==========

.. _gcc-admix:

The `gcc-admix repository <https://github.com/RCIC-UCI-Public/gcc-admix/>`_ uses **YAML2RPM** to build an
updated version of gcc, a module file, and some compatible libraries.  Those packages can then be installed
and used to build other software.

GCC (the GNU compiler collection) is relatively complex build.  It is often useful to have an updated version of gcc on your 
system without destroying the system-supplied gcc. The GCC build has to be done in a certain way, packages need to be named
to be non-conflicting and other items. If you have completed the Quickstart you can build an updated version of gcc
and its related set of packages.

.. warning:: 
  
  This process will install RPMs as it builds. You should do this on a 'disposable' build system. It takes hours to compile a gcc.

Here is the full process for building gcc using the  `gcc-admix repository <https://github.com/RCIC-UCI-Public/gcc-admix/>`_

.. code-block:: bash

   git clone https://github.com/RCIC-UCI-Public/gcc-admix.git
   cd gcc-admix
   make download
   cd yamlspecs
   (make bootstrap &> /tmp/bootstrap-gcc.log; make &> /tmp/build-gcc.log) &

An optional last step would be to *unbootstrap* the system, which will remove any locally-built and installed RPMS that result from
the bootstrap process:

.. code-block:: console

   make unbootstrap

At this point, you should have a compatible set of RPMS for gcc and some key supporting libraries.

Build details
-------------

1. **make download**

   The download script is executed via target ``download`` in the Makefile
   and uses ``.gcc-admix.metadata`` file for a reference about what files to download.
   The file includes  SHA1 signatures  which are checked against downloaded
   file. Once the process completes all download distro files are in **sources/**.

2. **make bootstrap**

   This target does two functions

   **(1) add system RPMs**

   During the bootstrap step a few RPMs  that are needed for compiling gcc are installed via ``yum``.
   These RPMs are defined in ``.packages.yaml`` file in the section ``system:``:

   .. code-block:: yaml
      :caption: packages.yaml - system section

      site: !include site.yaml
      system:
         - glibc-devel.i686
         - libgcc.i686
         - libstdc++-devel.i686
         - ncurses-devel.i686
         - bison
         - flex
         - gmp-devel
         - libmpc-devel
         - !ifeq "{{site.os_release}},8,mpfr-devel,libmpfr-devel"
         - texinfo
         - binutils-devel

   In this yaml snippet there are 2 lines with the extended yaml syntax that
   we added to a regular yaml processing: 

   1. On this line, we specify by name another yaml file to include:

      .. code-block:: yaml

         site: !include site.yaml

      This type of an include, we call it :term:`yaml variable include` brings
      the whole content of another yaml file into a single variable. 
      The ``site.yaml`` contents are slightly different for **CentOS 7** and for
      **CentOS 8**. For example, we define the OS release variable as ``os_release: "8"`` on **CentOS 8**
      and we set it to ``os_release: "7"`` on **CentOS 7**.

      Keeping different information for OS release in different site files allows us to
      use the same build process and the same  code base in the repositories while adding only only minute
      changes to a handful of yaml files.


   2. The following line uses variables defined in ``site.yaml`` to check on what OS we are doing the build:

      .. code-block:: yaml

         - !ifeq "{{site.os_release}},8,mpfr-devel,libmpfr-devel"

      I this specific case, the differences between OSes are in the RPMs names that provide the needed library or
      functionality. Per the above yaml line  
      the build  will install system RPM ``mpfr-devel`` on **CentOS 8** and ``libmpfr-devel`` on **CentOS 7**.
      Here the :term:`yaml conditional` statement allows us to keep the main code base as is.

   **(2) build bootstrap RPMs**

   Once all the requirements of system provided RPMs are satisfied we can
   start building our RPMs in a specific order provided by the 

   .. code-block:: yaml
      :caption: packages.yaml - bootstrap section

      # Modules to build AND install locally. Order IS important
      bootstrap:
         - binutils-bootstrap
         - gcc
         - gcc-module
         - binutils
         - mpfr

   For each line listed in ``bootstrap:`` there will be an RPM built and
   immediately installed via ``yum``. The build process is done in the above specific
   order to satisfy dependencies. 

3. **make**

   Once the **make bootstrap** finishes, we have locally built and installed
   RPMs that allow us to proceed with building of the rest of the RPMs

   .. code-block:: yaml
      :caption: packages.yaml - build section

      # Modules to build. Order is NOT important
      build:
         - gmp
         - libiconv
         - mpc
         - "{{build_set_specific}}"
      build_set_specific:


   Here, ``gmp``, ``libiconv``, ``mpc`` and any other name listed in
   ``{{build_set_specific}}`` is  built.


   The ``packages.yaml`` file defines another variable ``set``:

   .. code-block:: yaml
      :caption: packages.yaml - set section

      sets:
      - gcc8
      - gcc11

   The ``sets``  provide additional information for the build process. We can
   think of definitions in ``packages.yaml`` as a specific collection of packages to
   be built with specific versions. By defining additional sets we can build 
   multiple collections  of packages where each can have different versions of the software or different packages. 

   In the above set definition we create 2 additional builds: one for gcc
   series 8 and another for gcc series 11. We reuse as much as possible the yaml files we
   already created for the packages defined in `packages.yaml`` via inheritance:
   
   .. code-block:: yaml
      :caption: set-gcc8.yaml 

      !include packages.yaml
      ---
      versions: versions-gcc8.yaml
      build_set_specific:
         - !ifeq "{{site.os_release}},7,,annobin"

   In this yaml file we inherit all of ``packages.yaml`` file via include
   statement.  Then in ``versions: versions-gcc8.yaml`` line we specify that
   file ``versions-gcc8.yaml`` specifies software versions to be used when building packages for this set.
   Finally, we redefine one variable ``build_set_specific`` (which was empty in
   included  packages.yaml file) and assign to it the result of conditional
   statement resolution: namely, if we build for **Centos 7** we do nothing
   different in terms of list of packages, and if we build for CentOS 8 we build an  ``annobin`` RPM.


