.. _admix_common:

Typical Files and Sets
======================

**Table of contents:**

.. contents::
   :local:

There is a standard set of files that is present in all admixes.
Here we describe in details what they are.

.. note:: All yaml files are in yaml format and in our custom parser
   we use standard *Python ruamel.yaml* library for parsing these files. 
   While we added a few extensions to our :ref:`parser <gen-definitions>`  to enable desired
   functionality, we keep all the initial *ruamel.yaml*  rules and naming conventions 
   intact and we do not change its API. 

.. _admix_top_level:

At the top level
----------------

``.ADMIXNAME.metadata``
  The file naming schema is *.ADMIXNAME-metadata* where `ADMIXNAME` is the admix top-level directory
  (and the admix git repository name).

  This file provides information about the packages' distribution sources that are used
  for the builds. All sources are stored in a publicly-accessible S3-bucket. Source tarballs
  are added manually and then the admix metadata file is updated with a new SHA1 signature.  
  When the command :command:`make download` is executed at the top level directory, the files
  named in the metadata file are downloaded. Over the years, we have encountered source 
  tarballs that become unavailable (or in extreme cases, changed by the original authors without updating versions).
  This "cache" of source tarballs stored in an S3-compatible bucket freezes at the point-in-time 
  when a particular software source was added to the admix.

  The metadata file is ASCII and the format is as follows (one line per source
  distribution, partial listing here):

    .. code-block:: text

       73d2447b5550e734f794b42ab7831349f993f0ff  sources/cmake-3.12.3.tar.gz 1tBH7jb4jynI8e6bMA05Cl2a4Q4AwNygS
       b55d925ef2c28da4ef154a8b2e157951caf81125  sources/scons-3.1.1.tar.gz

  The first field is the SHA1 sum checksum  of the distro file made with :command:`sha1sum`,
  the second field provides destination directory and the downloaded file name. 

  .. note::
     You will see some lines in the metadata files with a third field. These were important when data was
     stored in Google Drive instead of S3.  They remain for posterity, but are not used.

``Makefile``
  This is usually a very small standard file that includes one of the top
  level Makefiles:

  .. code-block:: make

     # Copyright (c) 2000 - 2019 The Regents of the University of California.
     # All rights reserved.
     # This includes the Generic toplevel Makefile - most admixes should
     # be able to use this.

     include $(YAML2RPM_HOME)/sys/Makefile.toplevel

  The included ``Makefile.toplevel`` is provided by the `yaml2rpm` RPM
  and has all standard build-related targets suitable for nearly all of the admixes. This is one
  example of "unavoidable code replication".

``README.md``
  Text file describing the admix and sometimes a few specific notes 
  to explain the building.

``.auto-changelog``
  A standard template to automatically create CHANGELOG.md file.
  
``.git/``
  Standard git repository directory for all the metadata.
  
``.gitignore``
  Files that specify to git  what not to track.
  
``.rpms.ADMIXNAME``
  The file naming schema is *.rpms.ADMIXNAME* where `ADMIXNAME` is the admix name (top-level directory).
  This is a text file recording the sizes of built RPMs for the admix (partial
  listing for gcc-admix):
  
    .. code-block:: bash
    
      92381715        gcc_11.2.0-11.2.0-2.x86_64.rpm
      209354          gcc_11.2.0-annobin-10.54-2.x86_64.rpm
      3246969         gcc_11.2.0-binutils-2.37-3.x86_64.rpm
      3179054         gcc_11.2.0-binutils-bootstrap-2.37-3.x86_64.rpm
      480445          gcc_11.2.0-gmp-6.2.1-2.x86_64.rpm
      8087            gcc_11.2.0-module-11.2.0-4.x86_64.rpm
      126123940       gcc_15.2.0-15.2.0-2.x86_64.rpm
      321763          gcc_15.2.0-annobin-12.98-2.x86_64.rpm
      7167773         gcc_15.2.0-binutils-2.45-3.x86_64.rpm
      7084432         gcc_15.2.0-binutils-bootstrap-2.45-3.x86_64.rpm
      427349          gcc_15.2.0-gmp-6.3.0-2.x86_64.rpm
      8092            gcc_15.2.0-module-15.2.0-4.x86_64.rpm
  
  The file is initially generated via running at the top-level admix repo:

    .. parsed-literal::
       :command:`make -s admixdb > .rpms.ADMIXNAME` 
    
  This db file needs to be updated when addmix RPMS change:

    * new RPMS are added
    * some builds are done anew
    * old RPMS are removed
  
``CHANGELOG.md``
  A text file that is generated via running a command (provided by the nodejs
  RPM) at the admix top-level directory.:

    .. parsed-literal::
       :command:`auto-changelog`
  
  This update is usually done when we do big changes form one OS release to
  another or when there was a major change in the templates or yaml files. 

.. _admix_yamlspecs:

In yamlspecs/
-------------

Each software package that needs to be build has a corresponding package
yaml file and often environment module yaml file. There are a few other
scenarios, possible combinations are:

  - package and module files 
  - only module file 
  - only package file 

See their description in :ref:`yamlpkg`.

.. _packages_yaml:

packages.yaml
~~~~~~~~~~~~~

**Usage:**
  This file is required for every admix (except *admixbuilder*).
  It is located in ``yamlspecs/`` and describes specifics of the admix build.

  During a build process ``Makefile`` various targets query this file to determine what packages need
  to be build and installed and in what order.
  If set files are present in the admix, they include this file to inherit most common variables. 

  An example ``packages.yaml`` from `gcc-admix repository <https://github.com/RCIC-UCI-Public/gcc-admix/>`_:
   
    .. literalinclude:: files/gcc-admix-packages.yaml
       :language: yaml

**Standard variables**
  There are a few variables in this file that have a meaning for
  different stages of the build and install on the **build machine**.
  These **variables names** are standard for all admixes:

  - :yvars:`site` - when present, includes site-specific yaml file. We include
    a *site file* when we need to differentiate a build for CentOS 8, Rocky 9, and eventually Rocky 10.
    Only one site file can be included here When not present, no site yaml is needed. 
  - :yvars:`system` - lists system RPMs to be installed via :command:`yum`.
    This is a one time action to add specific OS provided RPMs. Can be empty (same as absent).
  - :yvars:`bootstrap` - lists RPMs to be build and immediately installed.
    This is needed when a specific software package requires another software
    to be present. :red:`The order in this section is important!`  Can be empty
    (same as absent) which means no packages dependency in this admix.
  - :yvars:`build` - lists packages to be build in this admix. The listing order
    is not important. When empty all builds are done in sets.
  - :yvars:`manifest` - lists package names  provided by this admix build for installing on
    a build machine and eventually on a target machine. This variable is used in :command:`make manifest` command and the
    output provides a listing of all created RPMs names and can be used for the installation of these RPMs.
    Can be defined via other variables. If empty, the value is overwritten in set files. 
  - :yvars:`sets` - lists the logical sets of related packages that are built and installed together.
    When not present :yvars:`bootstrap` and :yvars:`build` define all the RPMs to be built.

**Admix-specific variables**
  There can be admix-specific variables defined in each admix ``packages.yaml`` file.
  Usually, we define these extra variables then include the file in set
  files. This way that we minimize copy/paste or repeat of the definition
  and have one place where it needs to be changed. Here, for example:

  - :yvars:`bootstrap0` - defines one RPM to be build. The variable is used in all set files in this admix
    when they include this file. 
  - :yvars:`build0` - similar to above, defines one RPMs to be build. Used in all set files in this admix.
    Note, here one other variable is used, :yvars:`build_set_specific` which
    is empty. This will be the only variable that will need to be uniquely
    defined for each specific set. 

.. _special_constructs:

**Special constructs**
  There are two special constructs that we use when we need to do something
  different depending on the  variables values comparison.
  These constructs can be used for any variable definition. 

  1. :yvars:`!ifeq` - this  is a simple, *if-else* construct to compare two values for
     equality and choose the outcome based on the comparison result. The
     :yvars:`!ifeq "var1, var2, outcome-if-true, outcome-if-false"` means

       .. code-block:: text

          if var1==var2 is true:
             variable evaluates to outcome-if-true
          else:
             variable evaluates to outcome-if-false

     In this case, if :yvars:`site.os_release` (a variable :yvars:`os_release` defined in ``site.yaml``)
     is 9, no additional system package is added prior to building gcc. Every
     other OS release will add the *gcc-gdb-plugin* system package.

  #. :yvars:`!eval` - this construct can compare two variables for a few other
     conditions (:tt:`==, <, <=, >,  >=`). The 
     :yvars:`!eval "outcome-if-true if var1 COMPARES var2 else outcome-if-false"` means

       .. code-block:: text

          if var1 COMPARES var2 is true:
              expression evaluates to outcome-if-true
          else:
              expression evaluates to outcome-if-false*

     For example, a line :yvars:`!eval "'antlr-tool' if {{site.os_release}} >= 9 else ''"`
     in `fileformats-admix repository <https://github.com/RCIC-UCI-Public/fileformats-admix/>`_
     in ``packages.yaml`` file evaluates to *antlr-tool* if the OS is 9 or later, and is empty otherwise.

  #. :yvars:`!OScmp` - this construct is specifically for evaluation 
     of a current OS version. The comparison operators are :tt:`<, <=, >, >=, ==`
     and it has true/false outcomes e.g. The :yvars:`!OScmp "coperator, var,  outcome-if-true, outcome-if-false"` means:

      .. code-block:: text

         if <OS version> <comparison operator> var:
             expression evaluates to outcome-if-true
         else:
             expression evaluates to outcome-if-false*

     For example, a line :yvars:`version: !OScmp "<, 10, 'rocky9-', 'rocky10+'"`
     would evaluate to *rocky-9* if the OS is  Rocky 9.7  or earlier and to *rocks-10+* otherwise.


  #. :yvars:`!include` - another special construct allows an extension (in our parser) to load
     additional files and parse their entries. 

     A line  **!include site.yaml** means that at the read time of
     ``versions.yaml`` the default system ``site.yaml`` file will be included
     for parsing and any variables defined there.

  The :yvars:`!eval`, :yvars:`!ifeq` and :yvars:`!OScmp` usage has
  limitations: 

     - use in simple variables 

       .. code-block:: yaml

          autogen: !OScmp "<, 10, ./autogen.sh, autoupdate"

     - use in dictionary variables as a value for a simple variable in a list, for example
	   this definition of *bind* is valid:

       .. code-block:: yaml

          install:
            bind: !OScmp ">=,9,bindfs,mount --bind"
            makeinstall: >
              mkdir -p $(ROOT)/{{root}};
              mkdir -p {{root}};
              {{install.bind}} $(ROOT)/{{root}} {{root}}

     - can not be used as a value of a nested list item in a dictionary.
       This construct will give an error (last line):

       .. code-block:: yaml

          install:
            makeinstall: >
              mkdir -p $(ROOT)/{{root}};
              mkdir -p {{root}};
              !OScmp ">=,9,bindfs,mount --bind" $(ROOT)/{{root}} {{root}}

**Set-related variables**
  In addition to the standard :yvars:`sets` variable there are a few set-related ones.
  They are not present in in all the admixes but are common for complex admixes.

  - :yvars:`parallel` - defines how may sets in a given admix can be build in parallel.
    A default is 3. For example in `R4-admix repository <https://github.com/RCIC-UCI-Public/R4-admix/>`_
    it is defined:

      .. code-block:: yaml

         parallel:
           sets: 6

  - :yvars:`serialsets` - each serialset entry is a name and is a list of sets
    associated with it. These sets describe related packages that are built
    serially. The serialsets are built in parallel. For example, 
    in `perl-admix repository <https://github.com/RCIC-UCI-Public/perl-admix/>`_
    the following definition:

      .. code-block:: yaml

         serialsets:
            perl530:    
               - "530"
               - "530-meta"
               - "530-bio"
               - "530-gen"
            perl534:  
               - "534"
               - "534-meta"
               - "534-bio"
               - "534-gen"

    means serial sets *perl530* and *perl534* will  be built in parallel. In
    each parallel build  respective serial sets will be built one after
    another in the listed order.
   
    Currently, we use *serialsets* only in *perl-admix*.

.. _versions_yaml:

versions.yaml
~~~~~~~~~~~~~

**Usage**
  This file is required for every admix (except *admixbuilder*).
  It is located in ``yamlspecs/`` and usually contains packages names, their versions and
  other related info. This file is almost always included in set versions files
  and is always included in packages yaml files.

  Variables defined in this file are used in the packages yaml files.

  An example ``versions.yaml`` from `gcc-admix repository <https://github.com/RCIC-UCI-Public/gcc-admix/>`_:
   
    .. literalinclude:: files/versions.yaml
       :language: yaml

**Standard variables**
  - :yvars:`admix` - the admix name. Not used directly during the build 
    but is useful when running admixes verification scripts.
  - :yvars:`!include` - This is a standard include directive that specifies
    what other yaml files to include. Can be none or can be a few

**Admix-specific variables**
  Most entries in versions files are simple key-value pairs for packages names
  and versions that are used in packages yaml files. In this example:

  - :yvars:`gmp` - has version "6.1.2"
  - :yvars:`gmp_ext` - defines tarball extension for the source distribution.

  These variables are referenced in respective ``gmp.yaml`` file as
  :yvars:`{{versions.gmp}}` (resolves here to "6.1.2") and :yvars:`{{versions.gmp_ext}}` 
  (resolves here to "tar.xz")

  .. note:: Sometimes key-values pairs are not sufficient, in these cases we use *dictionary* values.

  A few examples of dictionary variables from different ``versions.yaml`` files:

  - From `biotools-admix repository <https://github.com/RCIC-UCI-Public/biotools-admix/>`_.
    Specify a compiler and its version:

    .. code-block:: yaml

       compiler:
         name: gcc
         version: "8.4.0"

    The elements of the dictionary can be accessed in packages yaml files as
    :yvars:`versions.compier.name` (resolves here to  "gcc") and :yvars:`versions.compiler_version`
    (resolves here to 8.4.0)

  - From `buildlibs-admix repository <https://github.com/RCIC-UCI-Public/buildlibs-admix/>`_.
    Specify values for *ucx* build:

    .. code-block:: yaml

       compiler:
       ucx:
         version: "1.12.0"
         rel: "2"
         confargs:
         compiler:

    The dictionary variables for multiple *ucx* builds are accessed  in ``ucx.yaml`` as
    :yvars:`{{versions.ucx.version}}` (resolves to "1.12.0" here), :yvars:`{{versions.ucx.rel}}`
    (resolves to "2" here) and so on.

    Note, :yvars:`confargs` and :yvars:`compiler` are empty here and are the defaults for the base
    version of *ucx* that we build. When we build multiple versions of *ucx* we have to set these
    variables differently depending on the *ucx* version specific requirements, so these 
    will be overwritten in respective set version files. 

.. _sets:

Set files
~~~~~~~~~

The concepts of sets is very straightforward - a set of packages RPMs that are related to one another
and should be built together.  Fundamentally, these are versions of software
that make sense to build and install together. 

An admix can have no sets or can have multiple sets, it depends on the
needed software and its logical grouping.  

Any given set has 2 files: a set file and a corresponding versions file. 
The naming schema is simple but both file names in the set need to be consistent.
For simplicity and ease of tracking we use ``set-NAME.yaml`` and ``versions-NAME.yaml``. 
Sometimes as a *NAME* we use a year the software was released or the year we installed,
sometimes specific versions names.  For example (from different admixes):

  +---------------------+--------------------------+--------------------------------------+
  | Set file name       | Versions file name       | Comment                              |
  +=====================+==========================+======================================+
  | set-2022.yaml       | versions-2022.yaml       | for apps built in 2022               |
  +---------------------+--------------------------+--------------------------------------+
  | set-2022-gcc11.yaml | versions-2022-gcc11.yaml | for apps built in 2022 with GCC v.11 |
  |                     |                          |                                      |
  | set-2022-intel.yaml | versions-2022-intel.yaml | for apps built in 2022 with Intel    |
  +---------------------+--------------------------+--------------------------------------+
  | set-py2.yaml        | versions-py2.yaml        | for old apps that use Python 2       |
  +---------------------+--------------------------+--------------------------------------+
  | set-v19.yaml        | versions-v19.yaml        | for Julia v 1.9                      |
  +---------------------+--------------------------+--------------------------------------+

**Set files rules**

1. A set file has the same format as ``packages.yamk``.
   It must include ``packages.yaml`` file via an include directive (see below).
#. A set file must have a corresponding versions file
   and reference it via a :yvars:`versions` variable.

   Here is an example for ``set-2026.yaml`` from `buildlibs-admix repository <https://github.com/RCIC-UCI-Public/buildlibs-admix/>`_
   (partial listing):

   .. code-block:: yaml

      !include packages.yaml
      ---
      versions: versions-2026.yaml
      bootstrap:
        - ucx
        - ucx-module
        - ucx-cuda
        - ucx-cuda-module
        - openmpi
        - openmpi-module

#. A  set versions file has the same format as ``versions.yaml`` file.
   It needs to include ``versions.yaml`` file (unless all variables are redefined). 

   For the ``set-2026.yaml`` in our example, the contents of ``versions-2026.yaml`` are (partial listing):

   .. code-block:: yaml

      !include versions.yaml
      !include site97.yaml
      ---
      ucx:
        version: "1.20.0"
        rel: "1"
        confargs: yes
      openmpi:
        version: "5.0.9"
        major: "5.0"
        rel: "1"
        cudaaware: yes

   Here, any existing definitions for *ucx* in included ``versions.yaml``
   and ``site97.yaml`` will be overwritten by the above definitions.  This
   demonstrates the reuse and inheritance. Both simplify the code.

#. A set must be recorded in ``packages.yaml`` file in the :yvars:`sets` variable
   (partial listing here):

   .. code-block:: yaml

      ---
      site: !include site.yaml
      system:
        - numactl
        - numactl-devel
        - hwloc-devel
        ... 
      bootstrap:
        - ucx
        - ucx-module
      build:
      manifest:
        - "{{build}}"
        - "{{bootstrap}}"
        - "{{system}}"
      sets:
        - base
        - system
        ... 
        - "2024"
        - "2026"
