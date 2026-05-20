.. _python_admix:

Python
======

**Table of contents:**

.. contents::
   :local:

Building
--------

The `python-admix repository <https://github.com/RCIC-UCI-Public/python-admix/>`_ 
is used to build multiple versions of Python.

Python is relatively complex build however it does not require local changes to its Makefile to
accomplish multiple builds.

Here is the full process for rebuilding Python and its associated modules present in the repo:

.. parsed-literal::
   :command:`git clone https://github.com/RCIC-UCI-Public/python-admix.git
   cd python-admix
   make buildall-parallel &> buildall.log &`

.. warning:: 
   This process will install RPMs as it builds. You should do this on a *disposable* build system.

The following sections provide detailed explanation about repo files,
build process, and adding new modules step-by-step.

Files
-----

.. _python_admix_files_top:

At the top level
~~~~~~~~~~~~~~~~~~~~~~

Standard files and directories present in every admix as described in
:ref:`admix top level files <admix_top_level>`.

.. _python_admix_files_yamlspecs:

In yamlspecs/
~~~~~~~~~~~~~

Standard files
^^^^^^^^^^^^^^

We create a set of modules to install for each version of Python.
The sets usually include most commonly used  or specifically requested by
users modules. 

When building RPMs for Python modules we use native Python tools
``pip`` or ``python setup.py`` as each package specifies in its configuration.

Many modules trigger their own chain of dependent Python modules that need to be
installed.  Because of the dependencies there is an order when in the set a 
specific module can be built. Some needs to be build and installed before others
can be compiled. Others need their dependencies only during the run time.
We have to handle such dependencies carefully so that we do not
create circular references during the build.

While we try to keep the sets contents the same, sometimes it is not possible
as the specific modules dependencies change.

``packages.yaml`` (required)
  Yaml format, describes specifics of this admix build.

  .. literalinclude:: files/python-admix-packages.yaml
      :language: yaml
Most of the variables in this file are standard
  (:yvars:`site`, :yvars:`system`, :yvars:`bootstrap`, :yvars:`build`, :yvars:`manifest`, :yvars:`sets`).
  There are a few new variables in this file that allow us
  to  define a list of system RPMS to be added only when building for a specific OS.

  - :yvars:`develext` - set this variable to :yvars:`-devel` if the
    OS release is 7 (in included ``site.yaml``). For all other releases set it to an empty string.
    This allows us to use a single variable :yvars:`libyaml{{develext}}`
    that will be set correctly when building for a different OS.
  - :yvars:`!eval "'{{pillow_libs}}' if {{site.os_release}} >= 8 else ''"` -
    gets evaluated to a variable :yvars:`{{pillow_libs}}` for OS 8+
    or to an empty string otherwise.
  - :yvars:`{{pillow_libs}}` - list system RPMS to be installed for OS 8+.
  - :yvars:`bootstrap` and :yvars:`build` - empty, no packages in the base
    set. All build will be in the specific sets.
  - :yvars:`sets` - lists the sets to be built. Here for a set name we use a short hand
    notation of a Python version (Python 2.7.17, Python 3.8.0, etc).
  - :yvars:`parallel` -  defines  2 level of parallelization. The
    :yvars:`parallel.sets` says build 3 sets in parallel, and
    :yvars:`parallel.pkgs` says within any single set build 4 packages at the same
    time.  This translates into building max 12 python packages at a time.

``versions.yaml`` (required)
  Since there are no packages to build for the base set, this file lists the admix name
  and the specific unique build options to use when building any python package:

  .. literalinclude:: files/python-admix-versions.yaml
      :language: yaml

``python.yaml`` (required)
  This yaml file provides all the instructions to build base Python RPM.

  .. literalinclude:: files/python-admix-python.yaml
      :language: yaml

  Most variables are standard and are described in :red:`TODO ref`.
  The specific variables are as follows:

  - include statements specify tempalte files to include when parsing this yaml file.
    These templates define common variables that are neeed in all builds and
    using the include directive simplifies the comon code reuse and minimizes
    the overall code footprint.

    - :yvars:`!include rcic-package.yaml` -  include ``rcic-package.yaml`` tempalte
      file that defines defaults for the variables used during the build.

      :red:`TODO add reference to this file and describe it in full`
    - :yvars:`!include rpm.yaml` -  include ``rpm.yaml`` template file that
      defines specific RPM directives to use when creating RPMs.
      These definitions will override what :command:`rpmbuild` uses by default.

      :red:`TODO add reference to this file and describe it in full`
  - :yvars:`family_version`, :yvars:`major_version`,
    :yvars:`unique_opts` - are set from values defined in corresonding versions file. 
    They define values specific to a given Pytohn version used for a build.

  - :yvars:`rpmAutoReqProv` - here we overwrite what is defined as a default
    in the included ``rpm.yaml`` file. Set to **no** means there will be no
    automatic collection of requires and provides by the ``rpmbuild``.

  - :yvars:`rpmFilters` - these directives will be added to the spec file.
  - :yvars:`rpm` specifies what extra lines to add to the spec file.
    The definition of :yvars:`*RpmPython` is in ``rpm.yaml`` file.

``python-module.yaml`` (required)
  This file describes an environment module build for each version of Python.

  .. code-block:: yaml 
     
     !include python.yaml
     !include rcic-module.yaml
     ---
     - package: Python module
       category: LANGUAGES
       release: 5

  The variables are:

  - include statements specify tempalte files to include when parsing this yaml file.

    - :yvars:`!include python.yaml` -  specifies a package file to include when parsing this file.
      Each package module file always includes the package yaml file to get needed package definitions.
    - :yvars:`!include rcic-module.yaml` - specifies a tempalte to include when parsing this file.
      The ``rcic-module.yaml`` is a default template file that defines generic variables for most module files.

      :red:`TODO add reference to this file and describe it in full`
  - :yvars:`CATEGORY` - a logical category name to assign this module to.  This
    will result in adding created module file to a directory specified by
    this variable, here to ``LANGUAGES`` (once the RPM is installed).

    :red:`TODO add reference to CATEGORY`
  - :yvars:`release` - an RPM release number to use. Default is 1. 

``Makefile`` (required)
  This is a standard file, it includes a generic template:

  .. code-block:: make

     # Copyright (c) 2000 - 2026 The Regents of the University of California.
     # All rights reserved.
     # This includes the Generic yaml2rpm Makefile - most packaging should
     # be able to use this.
     
     include $(YAML2RPM_HOME)/sys/Makefile

``common.yaml``
  A template that provides a set of variables for build that is used for
  every Python module: 

  .. literalinclude:: files/python-admix-common.yaml
      :language: yaml

  Here we define all the common varialbes that are reused for every package

  - :yvars:`buildtype`  - a value is defined for each version of Python in its
    versions file.  Depending on what is in versions file, either
    :yvars:`install_pip` or :yvars:`install_setup` will be used. 

  - :yvars:`install_pip`: build a package using ``pip install --root ...``
    (for Python 3.14+).

  - :yvars:`install_setup`: build a package using ``python ./setup.py install --root ...``
    (for Python versions up to 3.10.2).

  - :yvars:`pymod_requires` - an empty settting. This provodes a flexible way
    to override in a specific yaml file if needed.

  - :yvars:`build` and :yvars:`install` define build and install commands to be used.
    For the install, one of the defined installation methods will apply.

  - :yvars:`requires` - defines what is required for the package to be built.
    Python package itself is always a requirement. The :yvars:`{{pymod_requires}}` is
    resolved for eaach package as empty by default or to a specific setting
    defined in a given package file.
    
  - :yvars:`files` - show where files from RPM will be installed under the
    main Python installation directory. This is a standard layout for all
    built modules.

``common_bootstrap_wheel.yaml``
  This is an include file that is used in a few specific situations
  for packages where current combination of setuptools+distutils tools does not work for regular builds
  when installing from source wheel files.

  This solves the *bootstrap* circular dependency problem when
  *pip* package requires *tomli* AND *tomli* can only use *pip* to install itself.

  It overrides the definition of ``pip install`` to use the bundled with
  (but not installed) pip wheel file of the base Python distro:

  .. code-block:: yaml

     !include common_wheel.yaml
     ---
     - name: common_bootstrap_wheel
       install:
         makeinstall: >
           export PIP3=`find $$python__PREFIX -name pip-\*-py3\*whl`;
           python $$PIP3/pip install --ignore-installed --root $(ROOT) --no-deps {{src_tarball}}

``common_wheel.yaml``
  This is an include file used for installing from source wheel files for packages where current combination
  of setuptools+distutils does not work for regular build.

  .. code-block:: yaml

     !include common.yaml
     ---
     - name: common_wheel
       no_src_dir: True
       extension: whl
       suffix: py3-none-any
       hash:
       src_tarball: "{{name}}-{{version}}-{{suffix}}.{{extension}}"
       pypiurl: https://files.pythonhosted.org/packages/{{hash}}
       vendor_source: "{{pypiurl}}/{{src_tarball}}"
       build:
         pkgmake: echo 'Using wheel distro'
       install:
         makeinstall: >
           pip3 install --root $(ROOT) --no-deps {{src_tarball}}

``NAME.yaml`` files
  The rest of the yaml files (excluding sets and versions) are used to build
  specific Python module packages.  Each one will include one of the common
  templates depending on what is used for the source distribution.

  For example, ``lark.yaml`` to build *lark* module from a source wheel file is:

  .. code-block:: yaml

     !include common_wheel.yaml
     ---
     - package: lark
       name: lark
       version: "{{versions.lark}}"
       hash: "{{versions.lark_hash}}"
       description: |
         A modern parsing library {{version}}
     
  Another example, ``sympy.yaml`` to build *sympy* module from a source tar.gz file is:

  .. code-block:: yaml

     !include common.yaml
     ---
     - package: sympy
       name: sympy
       version: "{{versions.sympy}}"
       vendor_source: https://github.com/{{name}}/{{name}}/archive/refs/tags/{{version}}.{{extension}}
       description: |
         Python Library for symbolic mathematics

.. _python_admix_sets:

Set specific
^^^^^^^^^^^^

The set files and corresponding versions files enable us to create multiple
versions of desired modules for multiple versions of Python:

  .. table::
     :class: noscroll-table

     +---------+---------------+-------------------+
     | Python  | Set           |  Versions         |
     | version | file          |  file             |
     +---------+---------------+-------------------+
     | 2.7.17  | set-217.yaml  | versions-217.yaml |
     |         |               |                   |
     | 3.8.0   | set-380.yaml  | versions-380.yaml |
     |         |               |                   |
     | 3.10.2  | set-310.yaml  | versions-310.yaml |
     |         |               |                   |
     | 3.14.3  | set-314.yaml  | versions-314.yaml |
     +---------+---------------+-------------------+

Any individual set can be built separately, for example:

   .. parsed-literal::
      :command:`make buildall SET=314`

Sets define individual packages for each Python version.
For example ``set-380.yaml`` (partial listing):

  .. code-block:: yaml

     !include packages.yaml
     ---
     versions: versions-380.yaml
     bootstrap:
       - python
       - python-module
       - setuptools
       - pip
       - cython
       - numpy
       ...
     build:
       - virtualenv
       - pyyaml
       - sqlalchemy
       - pytz
       ...

The :yvars:`bootstrap` entries must be built and immediately installed in the
listed order. For the entries in :yvars:`build` the order is not important
and the resulting built RPMs are not immediately installed. 

The versions files define each package version and any additional variables:

  .. code-block:: yaml

     !include versions.yaml
     ---
     buildtype: setup
     release: 5
     python_version: "3.8.0"
     python_family: "3.8"
     python_major: "3"
     setuptools: "46.0.0"
     pip: "20.0.2"
     cython: "0.29.15"
     numpy: "1.18.1"
     virtualenv: "20.0.10"
     pyyaml: "5.3"
     sqlalchemy: "1.3.15"
     sqlalchemy_rel: "1_3_15"
     pytz: "2019.3"
     pytz_hash: "82/c3/534ddba230bd4fbbd3b7a3d35f3341d014cca213f369a9940925e7e5f691"

Here any variable with :yvars:`_hash`  shows a specific portion of the source
distro in *pypi.org*.  Using it allows us to keep a single :yvars:`vendor_source`
line for multiple versions of each package. There is no single naming schema
how developers name their packages or create distro files. 
We sometimes need to define additional variables to handle such variations. 
For example, :yvars:`sqlalchemy_rel` is needed for *sqlalchemy* package to make the distro name.

.. _python_admix_scripts:

Scripts
^^^^^^^

There are a few scripts that we created to enable specific tasks.
See the scripts files contents in `python-admix repository <https://github.com/RCIC-UCI-Public/python-admix/>`_.
All the scripts are specific to python-admix.

``filter-requires-scipy.sh``
  This bash script is used to parse requires during the ``rpmbuild`` run  for
  ``scipy.yaml`` and removes some third party hard-coded  versions of
  *libquadmath* libraries. As a result only OS-installed libraries names are
  left in requires and they satisfy the package needs. 

``site.cfg.template``
  This is a template configuration file that is added to the build
  directory when building RPMs for ``scipy.yaml`` and ``numpy.yaml``.
  The template simply lists specific directories paths for OpenBLAS to use during
  the configuration step (the names are defined by the developers). 
  When building for a different Python version  a different OpenBLAS
  version will be used and the paths in the template are updated to
  the correct ones for the loaded OpenBLAS environment module.

.. _python_admix_add_modules:

Add new modules
---------------

The steps below outline how one can add a new Python module. 
For an example we use *vector* module and we want to add this to Python 3.14.3.

1. Search for a module on `pypi.org <http://pypi.org>`_.
   Once found, note its short description and its source distribution. 
   The distro is in *tar.gz* format so we can create a new ``vector.yaml`` as:

  .. code-block:: yaml

     !include common.yaml
     ---
     - package: vector
       name: vector
       version: "{{versions.vector}}"
       vendor_source: https://files.pythonhosted.org/packages/{{versions.vector_hash}}/{{name}}-{{version}}.{{extension}}
       description: |
         Vector classes and utilities

#. On *pypi.org* follow the download link and copy a link for the
   desired distro file. Edit ``versions-314.yaml`` and add 2 lines at the end:

   .. code-block:: yaml

      vector: "1.8.0"
      vector_hash: "59/3b/fec30a70491bae65ed8f129d8fca50c8345248a5ca8a8fee6740b4f85a6d"

   Note, we use only the version portion for :yvars:`vector` and only the
   source distro file hash portion for the :yvars:`vector_hash`.

#. Edit ``set-314.yaml`` file and add a line at the end: 

   .. code-block:: yaml

      - vector 

#. Now you are ready to download the package distro file: 

   .. parsed-literal::
      :command:`make download PKG=vector SET=314`

   A successful download will result in placing downloaded file in ``../sources/``. 
   Check the sha1sum signature then add it to the ``../.python-admix.metadata``:

   .. parsed-literal::
      :command:`sha1sum ../sources/vector-1.8.0.tar.gz`
      b71cfcf14c7f61d4f4e194c4399aa68a797e8a3b  ../sources/vector-1.8.0.tar.gz
      :command:`vim ../.python-admix.metadata`  # and add the sha1sum output per an existing format


#. Build an RPM for this new module:

   .. parsed-literal::
      :command:`make vector.pkg SET=314`

   The command will echo on the stderr commands and their outputs 
   and will end with something similar to:

   .. parsed-literal::

      Wrote: /export/repositories/python-admix/RPMS/x86_64/python_3.14.3-vector-1.8.0-1.x86_64.rpm
      Executing(%clean): /bin/sh -e /var/tmp/rpm-tmp.2XyfxO
      + umask 022
      + cd /export/repositories/python-admix/BUILD
      + cd python_3.14.3-vector-1.8.0
      + /usr/bin/rm -rf /export/repositories/python-admix/yamlspecs/00STAGE314/tmpbuild/python_3.14.3-vector.buildroot
      + RPM_EC=0
      ++ jobs -p
      + exit 0
      make[1]: Leaving directory '/export/repositories/python-admix/yamlspecs/00STAGE314/tmpbuild'
      touch /export/repositories/python-admix/yamlspecs/00STAGE314/vector.pkg
      echo "===== Completed vector.pkg ( $(date) )========" 
      ===== Completed vector.pkg ( Tue Apr 28 14:45:52 PDT 2026 )========

   The **Wrote** line gives a path to the created RPM.

   Check the RPM for validity:

   .. parsed-literal::
      :command:`rpm -qlp /export/repositories/python-admix/RPMS/x86_64/python_3.14.3-vector-1.8.0-1.x86_64.rpm`
      /opt/apps/python/3.14.3
      /opt/apps/python/3.14.3/lib
      /opt/apps/python/3.14.3/lib/python3.14
      /opt/apps/python/3.14.3/lib/python3.14/site-packages
      /opt/apps/python/3.14.3/lib/python3.14/site-packages/vector
      /opt/apps/python/3.14.3/lib/python3.14/site-packages/vector-1.8.0.dist-info
      ... 

#. Install the new RPM:

   .. parsed-literal::
      :command:`make -C .. clean createlocalrepo
      yum -c ../yum.conf install python_3.14.3-vector`
