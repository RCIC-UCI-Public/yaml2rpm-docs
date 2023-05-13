General structure
=================

.. _admix_internals:

Almost all admixes follow the same layout structure
Here we describe the general structure and the common files
and directories.

All admix repositories are stored in our public github
on https://github.com/RCIC-UCI-Public

.. raw:: html

   <style> .blue {color:mediumblue} </style>

.. role:: blue

Repository layout
------------------

Here we show the admix structure on a real example of **foundation-admix**.
After clowning of the admix git repo the directory structure is

.. code-block:: bash

   git clone https://github.com/RCIC-UCI-Public/foundation-admix.git


|  :blue:`foundation-admix/`
|      .foundation-admix.metadata
|      :blue:`.git/`
|      .gitignore
|      Makefile
|      README.md
|      :blue:`yamlspecs/`
|           Makefile
|           common.yaml
|           packages.yaml
|           set-centos8.yaml
|           versions.yaml
|           versions-centos8.yaml
|           cmake.yaml
|           cmake-module.yaml
|           curl.yaml
|           foundation-module.yaml
|           git.yaml
|           git-lfs.yaml
|           ninja.yaml
|           pigz.yaml
|           rubygem-hpricot.yaml
|           rubygem-mustache.yaml
|           rubygem-rdiscount.yaml
|           rubygem-ronn.yaml
|           scons.yaml
|           scons-module.yaml
|           swig.yaml

Files description
-----------------

``.foundation-admix.metadata``
  The file naming schema is *.NAME-metadata* where `NAME` is the admix top-level directory.

  This file provides information about the packages' distribution sources that are used
  for the builds. All sources are stored in the google drive (added to google drive manually).
  When a command ``make download`` es executed at the top level directory to
  fetch needed sources from the google drive  drive this file provides needed info.
  The file format is as follows (one line per source distribution):

  |  **71861ee4f13a74bfbcdb  sources/cmake-3.22.1.tar.gz 1WmIylB7qKJRu**
  |  **da46835a76f218adc01e  sources/pigz-2.6.tar.gz     1kgHDuBVBcXzK**

  The first field is the SHA1 sum checksum from ``sha1sum``, the second field
  provides  destination directory and the downloaded file name, and the last
  field shows from what google drive URL to fetch (for this display 1st and 3rd
  fields are cut short  to fit in one line)

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
  and has all standard build-related targets suitable for most of the admixes

``README.md``
  Text file describing the admix


Files in yamlspecs/
^^^^^^^^^^^^^^^^^^^

This directory has specific packages yaml files that are used for creating RPMs.

Reserved yaml files
~~~~~~~~~~~~~~~~~~~

The two files must always be present in any admix:

1. ``packages.yaml`` - yaml format, describes specifics of
   this admix build.

   .. literalinclude:: files/foundation-admix-packages.yaml
      :language: yaml

   There are a few variables  set in this file that have a meaning for
   different stages of the build.

   - **site** - includes site-specific yaml file. Needed in this case to
     differentiate a build for CentOS 7 and CentOS 8.
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

2. ``versions.yaml`` - yaml format, usually contains packages names and versions.

   .. literalinclude:: files/versions.yaml
      :language: yaml

   Depending on needs additional info can be added. Note, here we include ``site.yaml`` file
   (installed via yaml2rpm RPM) via include statement and thus provide site-specific info about
   compilers, OS release, etc used for the build.


Packages yaml files
~~~~~~~~~~~~~~~~~~~

Specific packages yaml files describe what needs to be done to configure,
compile and create RPMs with the resulting binaries and libraries. Some
packages need an addition yaml file that describes how to build an
environment module for it, others do not.

In the **foundation-admix** we are creating RPMs for a few packages that
provide tools often used when compiling and building other software. While system
installed RPMs have default versions of these tools, often a particular software
package requires a newer version. For this reason we add such tools via built
RPMs in this admix: ``cmake``, ``git``, ``scons``, ``swig``, ``curl``, ``ninja``, and a few ``rubygems``.
Each package has a corresponding yaml description file.

``foundation-module.yaml``
  This file describes an environment module build for this admix.
  Since the tools are used mainly during configuration and compilation
  we install them in a specific path and provide a single environment module
  that enables these tools usage.

  .. literalinclude:: files/foundation-module.yaml
     :language: yaml


Layout after build
------------------

After the build commands repository structure changes and includes:

:blue:`BUILD/ RPMS/ SOURCES/ SPECS/ SRPMS/`

These are standard directories created during the ``rpmbuild`` command. The
command is run via a Makefile target and all prerequisites directory structure
and spec files are generated via Makefiles targets as well.

In addition, when installing RPMS locally on a development machine for a
verification  and testing  via

.. code-block:: bash

   make install-admix

the following directories are created at the top-level of the admix repo
to hold the local yum repository from which created RPMS are installed.

:blue:`cache/ localrepo/ yum.conf yum.repos.d/`
