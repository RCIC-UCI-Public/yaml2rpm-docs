.. _yaml2rpm:

YAML2RPM
========

.. contents::
   :local:

**This admix must be  built first**
  This is a bootstrap admix that provides building blocks needed for all
  other admixes. These building blocks include templates, Makefiles, profile
  files, and a few python packages that provide yaml files processing.

  The goal is to reduce the package-specific configuration/build essentials into 
  a yaml file that goes through some automated steps to create an RPM. 
  The building blocks provide all essentials to achieve this goal.

Building 
--------

| Make sure your :ref:`requirements` are met.
| Do :ref:`build yaml2rpm <building_yaml2rpm>` as described in Quickstart.


.. _yaml2rpm_files:

Files Description
-----------------

.. _yaml2rpm_files_top:

At the top level
~~~~~~~~~~~~~~~~

``Makefile``
  Provides targets for building/installing on development pristine environment.
  This file is different from all other ``Makefiles`` at the admix top levels.

``first-build.sh``
  Bash first-build script to bootstrap a vanilla OS install to be able to
  build RPMS using :term:`YAML2RPM`. Steps in the script include:

    1. Clone the repository that holds the rocks-devel source (rockscluster github)
    #. Build and install rocks-devel RPM
    #. Build and install the yaml2rpm RPMs

.. _yaml2rpm_yamlspecs:

In yamlspecs/
~~~~~~~~~~~~~

..  Makefile.site TODO rm

**Files**

``bootstrap.inc``
  This file is included on all of the ``bootstrap-*`` subdirectories 
  It defines Download location for bootstrapped sources during the RPM build.

``Makefile``
  A generic Makefile for the bootstrapping/building of RPMS in the admixes.
  It centrally defines targets and directives for the builds that are
  specified in packages yaml files.
  This file is a part of ``yaml2rpm`` RPM and most admixes use it 
  in their ``yamlspecs/Makefile`` via an include statement:

    .. code-block:: make

       include $(YAML2RPM_HOME)/sys/Makefile

``Makefile.tmpl``
  A template for creating ``yasmlspecs/Makefile`` for a new admix.

``Makefile.toplevel``
  A generic Makefile for defining all the targets that can be executed 
  via ``make`` at the admix top level.
  This file is a part of **yaml2rpm** RPM and most admixes use it 
  in their top level``Makefile`` via an include statement:

    .. code-block:: make

       include $(YAML2RPM_HOME)/sys/Makefile.toplevel

``packages.yaml``
  Defines what RPMs are build in the **yaml2rpm** repository.

``rcic-module-path.yaml``
  Defines how to build **rcic-module-path** RPM and what to include in it.
  This includes support and common code for
  updating modules path provided by the system with admix installed modules.

``rcic-module-support.yaml``
  Defines how to build **rcic-module-support** RPM and what to include in it.

``rcic-modules.csh``
  Configuration (legacy, keep for completeness) script for ``csh`` users.
  Updates module path.

``rcic-modules.sh``
  Configuration  script for ``bash`` users.  Updates module path.

``site.yaml``
  This file IS NOT part of the repository. It is a link that is created when building
  **yaml2rpm** RPM. The link is to the current OS site yaml file.
  The RPM, when installed, creates another link in the installation
  directory  ``/opt/rcic/site`` to the correct site file based on the OS.

``versions.yaml``
  Defines versions of the built RPMs. Need to update respective version when a
  yaml file for the RPM changes (``rcic-modulepath.yaml``,
  ``rcic-module-support.yaml, `yaml2rpm``).

``yaml2rpm.sh``
  Configuration script to set environment variables for building RPMS. Is
  installed in ``/etc/profile.d`` as a part of *yaml2rpm** RPM.

``yaml2rpm.yaml``
  Defines how to build **yaml2rpm** RPM and what to include in it.

**Direectories and their files**

``Modules/``
  Contains a subdirectory and files hierarchy that allow us to extend the
  environment modules **MODULEPATH** with the paths where
  we install our built module files for all the software that we build.

    |  ``-- init/``
    |        ``|-- bash``
    |        ``|-- csh``
    |        ``|-- rcicmodulespath``


  The files are a part of **rcic-module-path** RPM and are used by configuration scripts 
  in ``/etc/profile.d`` to set system-wide environment variables and shell
  settings for all users. The ``bash`` and ``csh`` are for different shells
  that may be used by the users. 
  The  ``rcicmodulespath`` describes paths where to look for created
  modules.  As we loosely assign modules into categories, we install module
  files into specific category path for easier navigation with the **module**
  commands output.  The categories include a location in the **$HOME** where users
  can add their own created modules. Current categories are described in :term:`categories`.

``bin/``
  A directory that contains the code used for building RPMs
  and a few utility tools.

  ``gen-definitions.py``
    A Python script. See the detail description in :ref:`gen-definitions`. 

  ``manifest2ansible.py``
    A python script that generates an ansible file from a manifest.
    Manifest is a list of generated RPMs that can be created by a build process in a given admix.

  ``runparallel``
    A Python script to enable parallel builds - running a build in a few
    admixes at the same time or a few sets at the same time

  ``wrapstrip``
    A shell wrapper for strip to discard symbols and other data from object files.
    Catches and discards any errors. 

``bootstrap-bin-python/``
  A legacy setup for building and installing RPM that would have a scripts section
  that uses /usr/sbin/alternatives to link to /usr/bin/python from /usr/bin/python3
  No longer used on Rocky 10+.

``bootstrap-future/``
  A legacy setup to build RPM for Python's future package. Was used at the time of
  Python 2 to Python 3 transition.

``bootstrap-ruamel-yaml/``
  Used to create ``python-ruamel-yaml`` RPM for *ruamel.yaml* parser/emitter. We use it in our
  :ref:`gen-definitions.py <gen-definitions>` script and a few support scripts.

``bootstrap-ruamel-yaml-clib/``
  Used to create ``python-ruamel-yaml-clib`` RPM for C version of reader,
  parser and emitter for *ruamel.yaml*

``bootstrap-setuptools/``
  A legacy setup to build RPM for Python's *setuptools* package. NO longer needed.

``builder/``
  Most steps in the build process are executed via targets in Makefiles and
  there is a hierarchy of Makefiles depending on a directory within the admix
  repository. To automatically handle all the needed default variables and
  include them in needed Makefiles and commands we provide the following
  templates. These templates are automatically included by respective Makefiles. 

  These files only change when a whole build process is changed
  (for example, it did when we enabled parallel sets build) with very  specific updates 
  that are relevant to ALL builds.  This directory is a part of **yaml2rpm** RPM
  and the templates files are:

  ``Defaults.mk``
    provides common defaults for generic builds. 
  ``Derived.mk``
    provides derived Makefile definitions based on ``Rules.mk``, ``Defaults.mk``, ``Definitions.mk``.
  ``Makefile``
    a generic Makefile that is called from generated spec files.
    In particular, in the **%build** section of the generated Makefile, the build target
    of the this Makefile is invoked. Similarly, the install target is called by the 
    **%install** section of the generated spec file
  ``Override.mk``
    Empty, can contain specific overwrites for definitions in ``Rules.mk``.
    This file is included in the ``Makefile``
  ``version.mk``
    Specify file names to be included in the Makefiles.

``include/``
  This directory contains files that are included in  the yaml files for the
  packages or their modules. They define common global block of code or
  variables that we reuse in every RPM build.

  ``pkg-defaults.yaml``
    Sets the basic defaults for the installation of the packages
    such as installation directory, python installation directory for
    adding a few packages to the default Python installed with the system RPMs, 
    additional modules path, etc. See details in the repository file.
    This file is included in two generic files in this directory,  ``rcic-module.yaml`` and 
    ``rcic-package.yaml`` and these  two files are used by packages yaml files.

  ``rcic-admix-requires.yaml``
    This is a template automatically used for specifying generic
    variables during the admix bootstrap built.

  ``rcic-module-head.tcl`` and  ``rcic-module-tail.tcl``
    A standard *tcl* header and footer that are sourced in generated specific
    environmental modules files for invoking autoloading functionality.
    These files  are included automatically in every created module file by ``gen-definitions.py``.  
    This allows us to create very standard definitions for the modules
    and to minimize the text rewriting that is added to each module.

  ``rcic-module.yaml``
    This file defines generic variables and their defaults for most packages
    modules generated by :term:`main script` from the packages module yaml files.
    Any definition can be overwritten in respective yaml file.
    It is used via placing the following line at the top of the package module yaml file:

      .. code-block:: yaml

         !include rcic-module.yaml

    If multiple yaml files are included this one must be the last.
    See examples in any admix in yaml modules files ``<PKGNAME>-module.yaml``.

  ``rcic-package.yaml``
    This file defines defaults for the variables used in the packages yaml files.
    For example, the source distribution file extension, generic build configuration, base RPM name, etc.
    It is used via placing the following line at the top of the package yaml file:

      .. code-block:: yaml

         !include rcic-package.yaml

    See examples in any admix in yaml files ``<PKGNAME>.yaml``.


  ``rpm.yaml``
    This file defines RPM specifications that need to be included in generated
    RPM spec files.  The variables defined there can be accessed in specific
    packages yaml files via their names.To use, place the following line 
    at the top of the yaml file usually after the ``!include rcic-package.yaml``:

      .. code-block:: yaml

         !include rpm.yaml

``site/``
   Yaml files that provide information about commonly used (for creating other packages) 
   software, such as compiler name and version, MPI interconnect and version, etc. 
   Contains multiple site files for different OS versions. Even if we use a
   later version of site file for the current OS, a previous version of site
   file is used in some sets as it defines versions of the software that we
   keep across the OS update for the users.

RPMs 
----

After the build is complete the following RPMs are built and installed.
Note, the paths that start with ``/opt/rcic`` or ``/opt/apps`` are specific to our  install. 
Both paths are set in a few files in this admix ``yamlspecs/``.

**rocks-devel**
  Provides core Makefile structure to generate spec files for RPMs.
  This is based on the Rocks clusters' tooling  `rocks-devel <https://github.com/rocksclusters/core>`_ 
  from `rocks-devel <https://github.com/rocksclusters/core>`_ to generate SPEC files and build the RPMs. 
  RPM installs files in ``/opt/rocks`` and a configuration script ``/etc/profile.d/rocks-devel.sh``
  that is used to set build environment variables. 

**python-ruamel-yaml**
  A Python package for *ruamel.yaml* parser/emitter. Installs in general
  ``site-oackages`` directory of the system's OS installed Python.

**python-ruamel-yaml-clib**
  A Python package for C version of *ruamel.yaml* reader. 
  Installs in general ``site-oackages`` directory of the system's OS installed Python.

**rcic-module-path**
  Provides module setup files defining where to look for modules, what
  commands to execute for user shell, what additional module paths are handled by
  these scripts and their location.  RPM installs environment scripts in 
  ``/etc/profile.d/`` and files in  ``/opt/rcic/Modules``.

**rcic-module-support**
  Provides support and common code for generated environment modules
  RPM installs files in ``/opt/rcic/include``.

**yaml2rpm**
  Provides :term:`main script` (which generates definitions from yaml templates)
  and all the support files such as Makefiles, includes, etc., to convert a yaml specification into an RPM. 
  RPM installs environment configuration script ``/etc/profile.d/yaml2rpm.sh``
  and all the support files in ``/opt/rcic``.  The main install path is configurable. 

  The environment configuration script sets that are used for building RPMs
  and are used in various Makefiles and packages yaml files:

    - ``YAML2RPM_HOME`` is set to :term:`yaml2rpm home`

    -  ``YAML2RPM_INC`` includes paths to the directories that
       provide yaml and Makefile templates and is set to
       ``YAML2RPM_INC=$YAML2RPM_HOME/include:$YAML2RPM_HOME/site:$YAML2RPM_HOME/sys``

    - ``PATH`` is prefixed  with ``$YAML2RPM_HOME/bin``
