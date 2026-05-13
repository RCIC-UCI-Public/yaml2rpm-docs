.. _admix_common:

Admix Common Files and Sets
===========================

**Table of contents:**

.. contents::
   :local:

There is a standard set of files that is present in all admixes.
Here we describe in details what they are.

.. note:: All yaml files are in yaml format and in our custom parser
   we use standard *Python ruamel.yaml* library for parsing these files. 
   While we added a few extensions to our :ref:`parser <gen-definitions>`  to enable desired
   funcitonality, we keep all the initial *ruamel.yaml*  rules and naming conventions 
   intact and we do not change its API. 

.. _packages_yaml:

packages.yaml
-------------

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
     conditions (==, <, <=, >,  >=). The 
     :yvars:`!eval "outcome-if-true if var1 COMPARES var2 else outcome-if-false"` means

       .. code-block:: text

          if var1 COMPARES var2 is true:
              expression evaluates to outcome-if-true
          else:
              expression evaluates to outcome-if-false*

     For example, a line :yvars:`!eval "'antlr-tool' if {{site.os_release}} >= 9 else ''"`
     in `fileformats-admix repository <https://github.com/RCIC-UCI-Public/fileformats-admix/>`_
     in ``packages.yaml`` file evaluates to *antlr-tool* if the OS is 9 or later, and is empty otherwise.

  #. :yvars:`!include` - another special construct allows an extension (in our parser) to load
     additional files and parse their entries. 

     A line  **!include site.yaml** means that at the read time of
     ``packages.yaml`` the default system ``site.yaml`` file will be included
     for parsing and any variables defined there will be available as :yvars:`site.VARNAME`.

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
-------------

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

  A few examples of dictionary variables from different ``verions.yaml`` files:

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
---------

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

TODO
