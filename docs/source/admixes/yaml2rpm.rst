YAML2RPM 
=========

.. _yaml2rpm:


Purpose
-------

This is a bootstrap admix that provides building blocks needed for all
other admixes. These include templates, Makefiles, a few python packages added
to the default OS distribution. 

The goal is to reduce the package-specific configuration/build essentials into 
a yaml file that goes through some automated steps to create an RPM. 


Prerequisites
-------------

There are 4 python modules that will be automatically
built and installed during the building step:

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

  bootstrap 
    build/install RPMS needed before building yaml2rpm
  download  
    download TARBALLS from vault
  build 
    build yaml2rpm RPMS
  install 
    install yaml2rpm RPMs

``first-build.sh``
  Bash first-build script to bootstrap a vanilla OS install to be able to
  build RPMS using yaml2rpm. Steps:

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

- ``python-future`` for Python 2/3 compatibility
- ``python-setuptools`` provides Python setuptools support for building Python modules
- ``python-ruamel-yaml`` is a ruamel.yaml parser/emitter that is derived from *libyaml*
- ``python-ruamel-yaml-clib`` C version of reader, parser and emitter for *ruamel.yaml*
- ``rcic-module-support`` provides support and common code for generated environment modules
- ``rcic-module-path`` provides support and common code for updating modules path provided by 
  the system with admix installed modules.
- ``yaml2rpm`` provides templates and support files to convert a yaml specification into an RPM. 
  It utilizes the tooling from `rocks-devel <https://github.com/rocksclusters/core>`_ to generate 
  SPEC files and build the RPMs. 

The **python-** RPMs provide 4 needed python modules for your default system python install.
The **rcic-module-support**, **rcic-module-path**, and **yaml2rpm** provide all the building structure and support files for
the packages builds with YAML2RPM. They include a couple of profiles files that are added to the **/etc/profile.d**.

In order to proceed with next steps simply execute them (for future logins they will be automatically sourced by the login shell):

.. code-block:: bash

   . /etc/profile.d/rcic-modules.sh
   . /etc/profile.d/yaml2rpm.sh


RPMs content
------------

While built 4 python packages are standard python modules that are provided as
RPMs to be installed don he system, the  remaining 3 RPMs provide all the
specific code base that is needed to use  YAML2RPM built system.

rcic-module-support
^^^^^^^^^^^^^^^^^^^

This RPM has a few files

A couple of *tcl* files provide standard header and footer that are used when
building any environmental modules.  This allows us to create very standard 
definitions for the modules and minimize text that nee to be added to each
module:

- rcic-module-head.tcl
- rcic-module-tail.tcl

A few template files provide nearly all the definitions that are needed for
creating description yaml files. 

- pkg-defaults.yaml
- rcic-admix-requires.yaml
- rcic-module.yaml
- rcic-package.yaml
- rpm.yaml

rcic-module-path
^^^^^^^^^^^^^^^^

A couple of scripts based on generic environmental modules scripts:

- /etc/profile.d/rcic-modules.csh
- /etc/profile.d/rcic-modules.sh

A few definitions for where to look for modules, what to execute for what
shell, additional module paths are handled by  these scripts which we choose
to install in **/opt/rcic/Modules/init**:

- bash
- csh
- rcicmodulespath

yaml2rpm
^^^^^^^^

Provides main driver (python script) that generates definitions from yaml
description files, all the meeded Makefile templates and includes, and  

- /etc/profile.d/yaml2rpm.sh - a profile file to add needed environment variables needed during the build
- /opt/rcic/README.md
- /opt/rcic/bin/gen-definitions.py 
- /opt/rcic/bin/manifest2ansible.py
- /opt/rcic/builder/Defaults.mk
- /opt/rcic/builder/Derived.mk
- /opt/rcic/builder/Makefile
- /opt/rcic/builder/Override.mk
- /opt/rcic/builder/version.mk
- /opt/rcic/samples/Makefile
- /opt/rcic/samples/cmake-module.yaml
- /opt/rcic/samples/cmake.yaml
- /opt/rcic/samples/common.yaml
- /opt/rcic/samples/packages.yaml
- /opt/rcic/samples/pkg-defaults.yaml
- /opt/rcic/samples/scons-module.yaml
- /opt/rcic/samples/scons.yaml
- /opt/rcic/samples/versions.yaml
- /opt/rcic/site/site.yaml
- /opt/rcic/site/site7.yaml
- /opt/rcic/site/site8.yaml
- /opt/rcic/site/updates8.yaml
- /opt/rcic/sys/Makefile
- /opt/rcic/sys/Makefile.tmpl
- /opt/rcic/sys/Makefile.toplevel

