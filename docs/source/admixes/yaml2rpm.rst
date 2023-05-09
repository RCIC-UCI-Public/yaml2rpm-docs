YAML2RPM 
=========

.. _yaml2rpm:


Purpose
-------

This is a bootstrap admix that provides building blocks needed for all
other admixes. These building blocks include templates, Makefiles, profile
files, and a few python packages that provide yaml files processing.

The goal is to reduce the package-specific configuration/build essentials into 
a yaml file that goes through some automated steps to create an RPM. 

The building blocks provide all essentials to achieve this goal.


Prerequisites
-------------

1. ``Python 3`` and required modules: ``argparse``, ``socket``, ``datetime``.
   There are 4 python modules that will be automatically
   built and installed  and installed by this admix during the building step:

   - ``future``: for compatibility of python 2/3 code
   - ``ruamel-yaml`` & ``ruamel-yaml-clib``: used by the  main script ``gen-definitions.py``
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

Files
-----

``Makefile``
  Provides targets for building/installing on development pristine environment: 
``bootstrap``
  build/install RPMS needed before building yaml2rpm
``download``
  download TARBALLS from vault
``build``
  build yaml2rpm RPMS
``install``
  install yaml2rpm RPMs
``first-build.sh``
  Bash first-build script to bootstrap a vanilla OS install to be able to
  build RPMS using yaml2rpm. Steps in the script include:

  1. Clone the repository that holds the rocks-devel source (rockscluster github)
  2. Build and install rocks-devel RPM
  3. Build and install the yaml2rpm RPMs


Building 
--------

You may want to build the YAML2RPM RPMs and install them from the source git repository.
Do the following in the top-level directory
You will need to set DISPLAY prior to doing this so that Firefox can ask for your permission to read public data

.. code-block:: bash

   ./first-build.sh

After this step is complete the following RPMs are built and installed:

1. ``python-future`` for Python 2/3 compatibility

2. ``python-setuptools`` provides Python setuptools support for building Python modules

3. ``python-ruamel-yaml`` is a ruamel.yaml parser/emitter that is derived from *libyaml*

4. ``python-ruamel-yaml-clib`` C version of reader, parser and emitter for *ruamel.yaml*

5. ``rcic-module-support`` provides support and common code for generated environment modules

6. ``rcic-module-path`` provides support and common code for updating modules path provided by 
   the system with admix installed modules.

7. ``yaml2rpm`` provides templates and support files to convert a yaml specification into an RPM. 
   It utilizes the tooling from `rocks-devel <https://github.com/rocksclusters/core>`_ to generate 
   SPEC files and build the RPMs. 

The four built ``python-*`` packages RPMs provide standard python modules 
that are added to the OS Provide stock distribution of python.
These additional modules are imported by the :term:`main script` in order to
parse yaml files. 

The ``rcic-module-support``, ``rcic-module-path``, and ``yaml2rpm`` provide all the building structure and support files for
the packages builds with YAML2RPM.  Please see the next section for detailed description of included files. 

In order to proceed with next steps simply execute them (for future logins they will be automatically sourced by the login shell):

.. code-block:: bash

   . /etc/profile.d/rcic-modules.sh
   . /etc/profile.d/yaml2rpm.sh


RPMs 
----

Details about what is inside specific RPMs.

rcic-module-support RPM
^^^^^^^^^^^^^^^^^^^^^^^

This RPM provides the following files.

1. Two *tcl* files provide standard header and footer 
   that are sourced in generated specific environmental modules files for 
   invoking autoloading functionality.

   This allows us to create very standard definitions for the modules
   and to minimize the text rewriting that is added to each module.
   These 2 files define variables and functions that handle automated loading/unloading of modules.

   ``rcic-module-head.tcl``
     module file header

   ``rcic-module-tail.tcl``
     module file footer

2. The following yaml template files provide nearly all the definitions that are needed for
   creating packages yaml files. These files are included in specific package
   yaml files via include directives as shown below. 

   ``pkg-defaults.yaml``
     This file is automatically read during the build
     process. It provides defaults used for defining site-specific variables, 
     paths for installation of applications and their modules, etc. 

   ``rcic-admix-requires.yaml`` 
     This is a template automatically used for specifying generic
     variables during the admix bootstrap built.

   ``rcic-module.yaml`` 
     This file defines generic variables for most module files
     generated by :term:`main script` from yaml description files.
     Any definition can be overwritten in respective yaml file. 
     To use, place the following line at the top of the yaml file

     .. code-block:: yaml

        !include rcic-module.yaml
  
   ``rcic-package.yaml``
     This file defines common definition to use as defaults for the variables in the
     package yaml files.  For example, the source distribution file extension, generic build
     configuration, base RPM name, etc. To use  place this line at the top of the yaml file 

     .. code-block:: yaml

        !include rcic-package.yaml

   ``rpm.yaml``
     This file defines RPM specifications that need to be included in generated
     RPM spec files.  The variables  once defined can be accessed  in specific
     packages yaml files via their names.To use, place the following line 
     at the top of the yaml file usually after the ``!include rcic-package.yaml``:

     .. code-block:: yaml

        !include rcic-package.yaml
        !include rpm.yaml

rcic-module-path RPM
^^^^^^^^^^^^^^^^^^^^

1. Two profile configuration files  are added to the generic environmental modules scripts
   location. They provide a setup for using YAML2RPM generated modules.  The
   install path **/etc/profile.d/** is a default for environment profile files on CentOS.

   ``/etc/profile.d/rcic-modules.csh`` 
     for **csh** users 

   ``/etc/profile.d/rcic-modules.sh`` 
     for **sh/bash** users

2. Module setup files provide definitions for where to look for modules, what
   commands to execute for user shell, what additional module paths are handled by
   these scripts and their location. The install path **/opt/rcic/Modules/init** 
   is configurable.

   ``/opt/rcic/Modules/init/bash``
     for **sh/bash** users

   ``/opt/rcic/Modules/init/csh`` 
     for **csh** users

   ``/opt/rcic/Modules/init/rcicmodulespath`` 
     this file describes paths where to look for created
     modules.  As we loosely assign modules into categories, we install module
     files into specific category path easier navigation with the **module**
     commands output.  The categories include a location in the **$HOME** where users
     can add their own created modules. Current categories are described in :term:`categories`.

yaml2rpm RPM
^^^^^^^^^^^^^

Provides :term:`main script` which generates definitions from yaml
description files, all the needed Makefile templates and include files,
example samples, etc.   The main install path (exception is a profile file)
**/opt/rcic/** is configurable. 

1. ``/etc/profile.d/yaml2rpm.sh`` is  a profile file to add environment variables needed during the build
    of software packages RPMs. 
2. ``/opt/rcic/README.md`` - info file form the top level of yaml2rpm github repository. 

3. The :term:`main script` ``/opt/rcic/bin/gen-definitions.py``
   is a python script that does all yaml file processing and creation of
   needed include files, definition files, etc for any specific software package. 

4. ``/opt/rcic/bin/manifest2ansible.py`` is a python script that generates an
   ansible file from a manifest yaml file. Manifest is a list of generated
   RPMs that can be created by a build process in a given admix.

5. Most steps in the build process are executed via targets in Makefiles and
   there is a hierarchy of Makefiles depending on a directory within the admix
   repository. To automatically handle all the needed default variables and
   include them in needed Makefiles and commands we provide the following
   templates. These templates are automatically included by respective Makefiles. 

   ``/opt/rcic/builder/Defaults.mk``
     provides common defaults for generic builds. 
   ``/opt/rcic/builder/Derived.mk``
     provides derived Makefile definitions based on ``Rules.mk``, ``Defaults.mk``, ``Definitions.mk``.
   ``/opt/rcic/builder/Makefile``
     a generic Makefile that is called from generated spec files.
     In particular, in the **%build** section of the generated Makefile, the build target
     of the this Makefile is invoked. Similarly, the install target is called by the 
     **%install** section of the generated spec file
   ``/opt/rcic/builder/Override.mk``
     Empty, can contain specific overwrites for definitions in ``Rules.mk``.
     This file is included in the ``Makefile``
   ``/opt/rcic/builder/version.mk``
     specify file names to be included in the Makefiles.
     This file is used by TODO.

6. The **/opt/rcic/samples/** contains a few examples files that show the usage
   of yaml templates and  includes for a few specific packages. 

7. In the **/opt/rcic/site/** path we install yaml files that provide
   information about commonly used (for creating other packages) 
   software, such as compiler name and version, MPI interconnect and version,
   etc. 

   ``/opt/rcic/site/site.yaml``
     is a link to another site file in the same directory.
   ``/opt/rcic/site/site7.yaml``
     site file with info about software and its versions for CentOS 7 builds.
   ``/opt/rcic/site/site8.yaml``
     site file with info about software and its versions for CentOS 8 builds.
   ``/opt/rcic/site/updates8.yaml``
     site file with updated versions of
     software to use for specific sets of packages when multiple versions of a given software are desired.

8. Makefiles used during the build process.

   ``/opt/rcic/sys/Makefile`` 
     this a template Makefile to drive the bootstrapping/building of RPMS
     Most packages should just use this without any modification.  It is included in each admix 
     in ``yamlspecs/Makefile`` a as

     .. code-block:: make

        include $(YAML2RPM_HOME)/sys/Makefile

   ``/opt/rcic/sys/Makefile.toplevel`` 
     this is a template Makefile that is included into the Makefile at the top level directory of an admix repo. This is a generic Makefile
     that provides all needed targets for the build process.  The include statement is

     .. code-block:: make

        include $(YAML2RPM_HOME)/sys/Makefile.toplevel

   ``/opt/rcic/sys/Makefile.tmpl`` 
     this is template Makefile that is copied into the each admix as ``yamlspecs/Makefile``.



