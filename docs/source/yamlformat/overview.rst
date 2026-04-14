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

.. _admixrepo_structure:

Repository structure
--------------------

The following shows the real example of **foundation-admix** admix structure .
Clone the repo:

.. code-block:: console

   git clone https://github.com/RCIC-UCI-Public/foundation-admix.git

After the git repo clowning the directory structure is:

|  :blue:`foundation-admix/`
|      .auto-changelog
|      .foundation-admix.metadata
|      :blue:`.git/`
|      .gitignore
|      .rpms.foundation-admix
|      CHANGELOG.md
|      Makefile
|      README.md
|      :blue:`yamlspecs/`
|           Makefile
|           asciidoctor-module.yaml
|           asciidoctor.yaml
|           common.yaml
|           foundation-module.yaml
|           git-lfs-module.yaml
|           git-lfs.yaml
|           git-module.yaml
|           git.yaml
|           packages.yaml
|           pigz-module.yaml
|           pigz.yaml
|           scons-module.yaml
|           scons.yaml
|           set-2024.yaml
|           swig-module.yaml
|           swig.yaml
|           versions-versions-2024.yaml
|           versions.yaml

.. _admixrepo_files:

Files description
-----------------

Files at the top level
~~~~~~~~~~~~~~~~~~~~~~

Standard files and directories present in every admix:

  ``.auto-changelog``
    A standard template to automatically create CHANGELOG.md file.
  
  ``.foundation-admix.metadata``
    The file naming schema is *.ADMIXNAME-metadata* where `ADMIXNAME` is the admix name (top-level directory).
  
    This file provides information about the packages' distribution sources that are used
    for the builds. All sources are stored in the external drive (added to the drive manually).
    When a command ``make download`` is executed at the top level directory to
    fetch needed sources from the external drive  drive this file provides needed info.
    This is a text file and the format is as follows (one line per source distribution):
  
    .. code-block:: text
  
       ced6676c625c49d78d73cbd3b9aaab8c30b9b4ee  sources/swig-4.0.2.tar.gz
       c1df9dcc002103aefec389200ffe20e9864ac7de  sources/asciidoctor-2.0.23.tar.gz
       f47002b6a90b136c8d3a4d66c0da2f4042b5ae2f  sources/git-lfs-3.5.1.tar.gz
  
    The first field is the SHA1 checksum of the distro file made with ``sha1sum``,
    the second field provides destination directory and the downloaded file name.
    The lines in the file are added manually when a new package is built and a
    new source is initially downloaded from a third-party vendor.
  
  ``.git/``
    Standard git repository directory for all the metadata.
  
  ``.gitignore``
    Files that specify to git  what not to track.
  
  ``.rpms.foundation-admix``
    The file naming schema is *.rpms.ADMIXNAME* where `ADMIXNAME` is the admix name (top-level directory).
  
    This is a text file recording the sizes of built RPMs for the admix:
  
    .. code-block:: bash
    
       784064          asciidoctor_2.0.23-2.0.23-1.noarch.rpm
       7793            asciidoctor_2.0.23-module-2.0.23-1.noarch.rpm
       7941            foundation_v8-module-v8-6.x86_64.rpm
       3937656         git-lfs_3.5.1-3.5.1-1.x86_64.rpm
       7623            git-lfs_3.5.1-module-3.5.1-1.x86_64.rpm
       9500846         git_2.45.1-2.45.1-1.x86_64.rpm
       7463            git_2.45.1-module-2.45.1-1.x86_64.rpm
       76930           pigz_2.6-2.6-1.x86_64.rpm
       7707            pigz_2.6-module-2.6-1.x86_64.rpm
       2128528         scons_4.2.0-4.2.0-1.x86_64.rpm
       7751            scons_4.2.0-module-4.2.0-1.x86_64.rpm
       1148644         swig_4.0.2-4.0.2-1.x86_64.rpm
       7610            swig_4.0.2-module-4.0.2-1.x86_64.rpm
  
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

  ``packages.yaml`` (required)
    Yaml format, describes specifics of this admix build.
  
    .. literalinclude:: files/foundation-admix-packages.yaml
        :language: yaml
  
    There are a few variables  set in this file that have a meaning for
    different stages of the build.
  
    - **site** - includes site-specific yaml file. Needed in this case to
      differentiate a build for CentOS 8 or 9. The ``site.yaml`` file is 
      installed via yaml2rpm RPM.
    - **system** - lists system RPMs to be installed via yum on the build machine.
      This is a one time action to add  specific OS provided RPMS to the build host.
    - **bootstrap** - lists RPMs to be build and immediately installed on the build machine.
      This is needed when a specific software package requires another software
      to be present. The order in this section is important. When empty no such
      packages are built.
    - **build** - lists RPMs to be build on the build machine. The listing order
      is not important. When empty no packages are built 
    - **build0** - another build target that lists RPMs to be build. There amy
      be multiple targets which depends on what packages are installed and how
      sets are built.
    - **manifest** - lists RPM names  provided by this admix build for installing on
      a target machine. This variable is used in ``make manifest`` command and the
      output provides a listing of all created RPM names and can be used for the
      installation of these RPMs.
    - **sets** - lists set names. A set is a collaction of RPMS built
      with the same specific tools such as compiler and dependend packages.
      The name for a set is arbitrary, usually referred to a year when
      applications were added ot to a specific colleciton for a specific
      compiler.
  
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

In the **foundation-admix** we are creating RPMs for a few packages that
provide tools often used when compiling and building other software. While system
installed RPMs have default versions of these tools, often a particular software
package requires a newer version. For this reason, in this admix we build
RPMs for needed versions of such tools: ``git``, ``git-lfs``, ``pigz``, ``scons``, ``swig``.

Each package has a corresponding yaml description file and a module yaml file.
In addition there are two files that allow us to build multiple versions of
some applications. Here we have just one sudh set of applications to build and
the required files to describe this are:

  ``set-2024.yaml``
    Yaml format, similar in structure to ``packages.yaml``. Lists what packages
    will be built for a set and what corresponding versions file to use. 

    .. literalinclude:: files/foundation-admix-set.yaml
       :language: yaml

  ``versions-2024.yaml``
    Yaml format, specifies packages names and versions
    to build for the specific set.

    .. literalinclude:: files/foundation-admix-versions-set.yaml
       :language: yaml

.. _admixrepo_afer_build:

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
