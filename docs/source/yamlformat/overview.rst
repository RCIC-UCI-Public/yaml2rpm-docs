.. _admixrepo_general:

General layout
==============

.. contents::
   :local:


All admix repositories are stored in our public github on https://github.com/RCIC-UCI-Public

Here we describe the general structure and the common files and directories.
Almost all admixes follow the same layout structure described in this section.
Specific info for more complex builds can be found in the *COMPLEX ADMIXES*.

.. raw:: html

   <style> .blue {color:mediumblue} </style>

.. role:: blue


.. _ov_gcc_admix:

.. _admixrepo_structure:

Repository structure
--------------------

Here we show the admix structure on a real example of **gcc-admix**.
This admix is key to many other software packages that require specific versions of gcc.

After cloning of the admix git repo the directory structure is

.. code-block:: console

   git clone https://github.com/RCIC-UCI-Public/gcc-admix.git

After cloning the git repo, the directory structure is:

|  :blue:`gcc-admix/`
|      .gcc-admix.metadata
|      .rpms.gcc-admix
|      :blue:`.git/`
|      .gitignore
|      CHANGELOG.md
|      Makefile
|      README.md
|      :blue:`yamlspecs/`
|             Makefile
|             annobin-gcc15.yaml
|             annobin.yaml
|             binutils-bootstrap.yaml
|             binutils.yaml
|             common.yaml
|             gcc-module.yaml
|             gcc-versions.yaml
|             gcc.yaml
|             gmp.yaml
|             isl.yaml
|             libiconv-1.16.patch
|             libiconv.yaml
|             mpc.yaml
|             mpfr.yaml
|             packages.yaml
|             set-gcc11.yaml
|             set-gcc15.yaml
|             set-gcc6.yaml
|             set-gcc8.yaml
|             versions-gcc11.yaml
|             versions-gcc15.yaml
|             versions-gcc6.yaml
|             versions-gcc8.yaml
|             versions.yaml


.. _admixrepo_files:

Files description
-----------------

Files at the top level
~~~~~~~~~~~~~~~~~~~~~~

``.gcc-admix.metadata``
  The file naming schema is *.NAME-metadata* where `NAME` is the admix top-level directory.

  This file provides information about the packages' distribution sources that are used
  for the builds. All sources are stored in a publicly-accessible S3-bucket. Source tarballs
  are added manually and then the admix'es metadata file is updated with a new sha1sum.  
  When the command ``make download`` is executed at the top level directory, the files
  named in the .metafile are downloaded. Over the years, we have encountered source 
  tarballs that become unavailable (or in extreme cases, changed by the original authors without updating versions).
  This "cache" of source tarballs stored in an S3-compatible bucket freezes at the point-in-time 
  when a particular software source was added to the admix.

  The metadata file is ASCII and the format is as follows (one line per source distribution):

  .. code-block:: bash

         80bb9891aeaeceee6374a32302c0a918c9e70b67  sources/binutils-2.45.tar.gz
         4a3781743561d062d7993c97862c6c3fd4a177a5  sources/binutils-2.45.tar.gz.sig
         ba53f88cc7265f7a9039b8943eb31e7568afc54f  sources/gcc-15.2.0.tar.gz
         f0f1368673173e28aa80763220e3e43e97026774  sources/gcc-15.2.0.tar.gz.sig

  .. note::
     You will see some .metadata files with a third field. These were important when data was
     stored in Google Drive instead of S3.  They remain for posterity, but are not used

  The first field is the SHA1 sum checksum  of the distro file made with  ``sha1sum``,
  the second field provides destination directory and the downloaded file name. The third field, if it
  exists, is ignored.

``Makefile``
  This is usually a very small standard file that includes one of the top
  level Makefiles:

    .. code-block:: make

       # Copyright (c) 2000 - 2019 The Regents of the University of California.
       # All rights reserved.
       # This includes the Generic toplevel Makefile - most admixes should
       # be able to use this.

       include $(YAML2RPM_HOME)/sys/Makefile.toplevel

  The included ``Makefile.toplevel`` is provided by the ``yaml2rpm`` RPM
  and has all standard build-related targets suitable for nearly all of the admixes. This is one
  example of "unavoidable code replication" 

``README.md``
  Text file describing the admix


**Files in yamlspecs/**

Standard files and directories present in every admix:

  ``.auto-changelog``
    A standard template to automatically create CHANGELOG.md file.
  
    The first field is the SHA1 checksum of the distro file made with ``sha1sum``,
    the second field provides destination directory and the downloaded file name.
    The lines in the file are added manually when a new package is built and a
    new source is initially downloaded from a third-party vendor.
  
  ``.git/``
    Standard git repository directory for all the metadata.
  
  ``.gitignore``
    Files that specify to git  what not to track.
  
  ``.rpms.gcc-admix``
    The file naming schema is *.rpms.ADMIXNAME* where `ADMIXNAME` is the admix name (top-level directory).
  
    This is a text file recording the sizes of built RPMs for the admix (partial listing):
  
    .. code-block:: bash
    
      92381715        gcc_11.2.0-11.2.0-2.x86_64.rpm
      209354          gcc_11.2.0-annobin-10.54-2.x86_64.rpm
      3246969         gcc_11.2.0-binutils-2.37-3.x86_64.rpm
      3179054         gcc_11.2.0-binutils-bootstrap-2.37-3.x86_64.rpm
      480445          gcc_11.2.0-gmp-6.2.1-2.x86_64.rpm
      635275          gcc_11.2.0-libiconv-1.16-2.x86_64.rpm
      8087            gcc_11.2.0-module-11.2.0-4.x86_64.rpm
      115719          gcc_11.2.0-mpc-1.2.1-2.x86_64.rpm
      1667322         gcc_11.2.0-mpfr-4.1.0-2.x86_64.rpm
      126123940       gcc_15.2.0-15.2.0-2.x86_64.rpm
      321763          gcc_15.2.0-annobin-12.98-2.x86_64.rpm
      7167773         gcc_15.2.0-binutils-2.45-3.x86_64.rpm
      7084432         gcc_15.2.0-binutils-bootstrap-2.45-3.x86_64.rpm
      427349          gcc_15.2.0-gmp-6.3.0-2.x86_64.rpm
      644718          gcc_15.2.0-libiconv-1.18-2.x86_64.rpm
      8092            gcc_15.2.0-module-15.2.0-4.x86_64.rpm
      136476          gcc_15.2.0-mpc-1.3.1-2.x86_64.rpm
      645882          gcc_15.2.0-mpfr-4.2.2-2.x86_64.rpm

  
    The file is generated via running a command ``make admixdb`` at the top-level admix repo 
  
  ``CHANGELOG.md``
    A text file that is generated via running ``auto-changelog`` command (provided by
    the  nodejs RPM) at the admix top-level directory. 
  
  ``Makefile``
    This is usually a very small standard file that includes one of the top
    level Makefiles:
  
      .. code-block:: make
  
         # Copyright (c) 2000 - 2019 The Regents of the University of California.
         # All rights reserved.
         # This includes the Generic toplevel Makefile - most admixes should
         # be able to use this.
  
         include $(YAML2RPM_HOME)/sys/Makefile.toplevel
  
    The included ``Makefile.toplevel`` is provided by the ``yaml2rpm`` RPM
    and has all standard build-related targets suitable for the admix.
  
  ``README.md``
    Text file describing the admix and sometimes a few specific notes 
    to explain the building.

Files in yamlspecs/
~~~~~~~~~~~~~~~~~~~

This directory has specific packages yaml files that are used for creating RPMs.
The first three files must always be present in any admix with these exact names:

``packages.yaml`` 
  yaml format, describes specifics of this admix build.

  .. literalinclude:: files/gcc-admix-packages.yaml
      :language: yaml

  There are a few variables  set in this file that have a meaning for
  different stages of the build.

  - **site** - includes site-specific yaml file. Needed in this case to
    differentiate a build for CentOS 8, Rocky 9, and eventually Rocky 10.
  - **system** - lists system RPMs to be installed via yum on the build machine.
    This is a one time action to add  specific OS provided RPMS to the build host.
  - **bootstrap** - lists RPMs to be build and immediately installed on the build machine.
    This is needed when a specific software package requires another software
    to be present. The order in this section is important.
  - **build** - lists RPMs to be build on the build machine. The listing order
    is not important.
  - **manifest** - lists RPM names  provided by this admix build for installing on
    a target machine. This variable is used in ``make manifest`` command and the
    output provides a listing of all created RPM names and can be used for the
    installation of these RPMs.

.. note::
   What does ``!ifeq "{{site.os_release}},9,,gcc-gdb-plugin"`` mean? This is a simple, if-else construct.
   In this case, if os_release is 9, no additional system package is added prior to building gcc. Every
   other os release will add the gcc-gdb-plugin system package.

``versions.yaml`` 
  yaml format, usually contains packages names and versions.

  .. literalinclude:: files/versions.yaml
     :language: yaml

  Depending on needs additional info can be added. Some versions.yaml files will include ``site.yaml`` file
  (installed via yaml2rpm RPM) via include statement and thus provide site-specific info about
  compilers, OS release, etc used for the build.

.. note::
   This versions.yaml does not define the version of gcc. In this admix, the version of gcc is 
   in a ``versions-gcc<n>`` file

``Makefile``
  This is usually a  very small standard file that includes one of the top level Makefiles:

    .. code-block:: make

       # Copyright (c) 2000 - 2019 The Regents of the University of California.
       # All rights reserved.
       # This includes the Generic yaml2rpm Makefile - most packaging should
       # be able to use this.

       include $(YAML2RPM_HOME)/sys/Makefile

  ``versions.yaml`` (required)
    Yaml format, usually contains packages names and versions.
  
    .. literalinclude:: files/foundation-admix-versions.yaml
       :language: yaml
  
    Depending on needs additional info can be added. Note, here we include ``site.yaml`` file
    (installed via yaml2rpm RPM) via include statement and thus provide site-specific info about
    compilers, OS release, etc used for the build.
  
  ``Makefile`` (required)
    This is usually a very small standard file that includes one of the top level Makefiles:
  
      .. code-block:: make
  
         # Copyright (c) 2000 - 2019 The Regents of the University of California.
         # All rights reserved.
         # This includes the Generic yaml2rpm Makefile - most packaging should
         # be able to use this.
  
         include $(YAML2RPM_HOME)/sys/Makefile
  
  ``foundation-module.yaml``
    This file describes an environment module build for this admix.
    Since the tools are used mainly during configuration and compilation
    we install them in a specific path and provide a single environment module
    that enables these tools usage.
  
    .. literalinclude:: files/foundation-admix-module.yaml
       :language: yaml

The rest of the files are description yaml files for specific packages and sets. They 
provide instructions what needs to be done to configure, compile and create RPMs with 
the software binaries, libraries and other files. Most packages need an additional yaml file that
describes how to build an environment module for it.

In the **gcc-admix** we are creating RPMs for different versions of gcc.  The ``yamlspecs`` directory 
when fully interpreted builds 35 RPMs for four different versions of gcc. The total yaml source
for all packages is 354 lines (including blank/comment lines).  This format is

  * Terse
  * Designed to for reuse across different versions


.. _ov_gcc_module:

``gcc-module.yaml``
  This file describes an environment module build for each version of the gcc compiler.

  .. literalinclude:: files/gcc-module.yaml
     :language: yaml

  You will see references to ``{{root}}`` which is variable. The format is inspired by ansible and
  Jinja2. One of the features that separates yaml2rpm from Jinja2 is the simplicity of recursive 
  definitions. Yaml2rpm naturally supports recursively-defined variables.  Recursion in Jinja2 is possible,
  but it takes extra declarations in each Jinja2 block.  For yaml2rpm, all variables are recursive.


Sets
----

The concepts of sets is very straightforward -- a set of packages are RPMs that are related to one another
and should be built "together".  Fundamentally, these are versions of software that make sense together. In
the gcc admix, it's reasonable to examine the gcc8 set

``set-gcc8.yaml``
  This file describes the packages that need to be built to create the gcc8 compiler and associated 
  RPMs.  

  .. literalinclude:: files/set-gcc8.yaml
     :language: yaml

  There are a few variables  set in this file that have a meaning for
  different stages of the build.

  - **versions:** - which versions file should be used. By convention, set-<setname> goes with
    versions-<setname>. But that is not hard-coded, it is explicitly coded in each set file. 
  - **bootstrap:** - This is a composite of ``{{bootstrap0}}`` and ``{{bootstrap1}}`` and are the
    packages that need to be built and installed in specific order on the *build host*. In gcc,
    a bootstrap version of binutils (``{{bootstrap0}}``) is built and installed and then it is rebuilt once the specific
    compiler version is built.  
  - **build_set_specific:** - This is particular to the gcc-admix. Some versions of gcc need annobin, others do not.  
    ``packages.yaml`` defines this variable to be empty. This set includes all the definitions of in packages.yaml
    and then *overrides* for this specific set.

.. note::
   Set files almost always include the baseline packages.yaml file. The gcc admix illustrates some of the flexibility
   that comes with the set + override construction. 

``versions-gcc8.yaml``

  This file lists the versions needed by the gcc8 set  

  .. literalinclude:: files/versions-gcc8.yaml
     :language: yaml

  This versions file includes the admix'es ``versions.yaml`` file and then adds variables ``gcc``, ``gcc_series``,
  and ``mpfr``. 

When taken together: gcc.yaml, packages.yaml, versions.yaml, set-gcc8.yaml, and versions-gcc8.yaml are all
that are needed to build the suite of gcc version 8.4.0 RPMS (9 in total).  Exchange set-gcc11.yaml and
versions-gcc11.yaml and gcc versions 11.2.0 RPMS (another 9) are built.  

Layout after build
------------------

After the build commands repository structure changes and includes:

  :blue:`BUILD/  RPMS/  SOURCES/  SPECS/  SRPMS/`

These are standard directories created during the ``rpmbuild`` command. The
command is run via a Makefile target and all prerequisites directory structure
and spec files are generated via Makefiles targets as well.

In addition, when installing RPMS locally on a development machine for a
verification and testing the following directories are created at the top-level of the admix repo
to hold the local yum repository with created RPMS:

  :blue:`cache/  localrepo/  yum.conf  yum.repos.d/`

These  files and directories provide a local to admix yum repository from
which built RPMS can be installed.

To create a local admix yum repo at the top admix level:

  .. code-block:: bash

     make clean createlocalrepo

To install all built RPMs for the admix:

  .. code-block:: bash

     make install-admix
