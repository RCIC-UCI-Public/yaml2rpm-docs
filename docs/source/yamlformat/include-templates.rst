.. _include_tempaltes:

Include templates 
=================

**Table of contents:**

.. contents::
   :local:

The include templates are yaml files that provide common definitions for the
builds of packages or their modules. 

.. _rpm.yaml:

rpm.yaml
--------

This file provides common RPM directive for the spec files. 
It is included either in the package yaml file
or another common yaml file via an include directive :yvars:`!include rpm.yaml`.

When building packages we sometimes need to define specific settings that
need to go to a spec file. Since we create spec files automatically 
we need to provide a way to add such definitions in the  packages yaml files
with a minimal writing and effort.

We put common default and specific cases definitions in ``rpm.yaml`` file
(distributed by ``yaml2rpm`` RPM).  Directives are eventually 
transformed to a package spec file. 

To use place the following line at the top of the yaml package file:

  .. code-block:: yaml

    !include rpm.yaml


Below we describe all the definitions and their use and possible overrides.

:yvars:`rpmJarRepack: 1`

   Default setting for jar repack. It sets value of :yvars:`__jar_repack`
   to 1 in the resulting spec file which means repack java jar files when making RPM.
   Sometimes it is not a desired action. To disable repacking 
   include in your yaml file the following:

   .. code-block:: yaml

      rpmJarRepack: 0

:yvars:`rpmAutoRequires:"AutoReqProv: {{rpmAutoReqProv}}"`
  
  And the default that is set is  :yvars:`rpmAutoReqProv: "Yes"`.
  This setting is for RPM building and it means use automatic process to
  figure out RPM requires and provides.  In some rare instances, may need to overwrite,
  in your package yaml file include:

  .. code-block:: yaml

     rpmAutoReqProv: no

:yvars:`rpmBuildIdLinks:"compat"`

  Defines how and if *build_id* links are generated for ELF files.
  Sometimes having these links in RPM is not desirable as they may conflict
  for two different versions of RPM packages which can prevent from installing the
  RPMs.  To turn off build id links, set this variable in the package yaml
  file as: 

  .. code-block:: yaml

     rpmBuildIdLinks: none

:yvars:`rpmFilters:""`

  Define local filters empty. This means system rpm macros
  for finding RPM's requires and provides will be used.
  Sometimes need to override provides, requires or both. 
  We define a few filters for such common situations:

  +------------------------------------+----------------------------------------------+
  | Filter name in ``rpm.yaml``        | Usage in package yaml files                  |
  +====================================+==============================================+
  | :yvars:`filterRequires`            | :yvars:`rpmFilters: \*filterRequires`        |
  +------------------------------------+----------------------------------------------+
  | :yvars:`filterProvides`            | :yvars:`rpmFilters: \*filterProvides`        |
  +------------------------------------+----------------------------------------------+
  | :yvars:`filterRequiresProvides`    | :yvars:`rpmFilters: \*filterRequiresProvides`|
  +------------------------------------+----------------------------------------------+
  | :yvars:`filterPerl`                | :yvars:`rpmFilters: \*filterPerl`            |
  +------------------------------------+----------------------------------------------+

  When none of the defined filters give a desired action we can still override :yvars:`rpmFilters`
  in package yaml file.  For example, when building Python RPM (see full ``python.yaml`` in *python-admix*)
  we redefine filters and macros to use Python and its libraries from the current build.

  .. code-block:: yaml

     rpmFilters:
         - '\nProvides: libpython{{family_version}}.so.1.0()(64bit)\n'
         - '%define __python %{buildroot}/$(PKGROOT)/bin/python{{major_version}}'


:yvars:`rpm:`

  This is a default definition of what goes into RPM's spec file and is sufficient for most builds.
  The package yaml files simply use include directive to use this definitions:

  .. code-block:: yaml

     !include rpm.yaml

  In this :yvars:`rpm` block (see ``rpm.yaml`` file int he repo):

    * set common defaults
    * redefine the *__spec_install_post* macro to load the correct modules so that
      *brp-python-bytecompile* can access libraries and correct version of python
    * set default :yvars:`rpmFlters` empty
    * define :yvars:`extras`  that are sufficient for many builds.

  When we need to override :yvars:`extras` variable in :yvars:`rpm`,  we use a few specific
  definitions that cover remaining build cases.

  For example,  for use with packages that provide 3-party precompiled software
  there is no need to execute *brp-* commands on existing binaries/libraries.
  We redefine *__os_install_post* to handle this case.  To use, specify in package yaml file:

  .. code-block:: yaml

     rpm:
       extras: *RpmNone

  And the block defined via :yvars:`extrasnone` will be used in spec file.

  The special *extras* definitions to handle specific builds:

  +-------------------------------------------------+----------------------------------+
  | The :yvars:`extras` definitions in ``rpm.yaml`` | Usage in package yaml files      |
  +=================================================+==================================+
  |  :yvars:`extrasnone`                            | :yvars:`extras: \*RpmNone`       |
  +-------------------------------------------------+----------------------------------+
  |  :yvars:`extrasconda`                           | :yvars:`extras: \*RpmConda`      |
  +-------------------------------------------------+----------------------------------+
  |  :yvars:`extraspython`                          | :yvars:`extras: \*RpmPython`     |
  +-------------------------------------------------+----------------------------------+

.. _rcic-module.yaml:

rcic-module.yaml
----------------

This file defines generic variables and defaults  for most module files
generated by ``gen-definitions.py`` from yaml description files.
It is distributed by ``yaml2rpm`` RPM.  

This template significantly reduces each module yaml file that needs to be written.

To use place the following line at the top of the module yaml file
right after the package file name. For example for *eugen* software
the module yaml file ``eigen-module.yaml`` is:

  .. code-block:: yaml

    !include eigen.yaml
    !include rcic-module.yaml

.. note:: If multiple yaml files are included this one must be the last

The required inclusion of ``eigen.yaml`` which in turn includes
``rcic-packages.yaml`` and ``rpm.yaml`` files. A few variables 
that are initially defined in these included files 
need to be overwritten in this template file as indicated below.
Any definition can be overwritten in respective module yaml file.

**Specific definitions and their use**

:yvars:`no_src_dir: True`
  There is no source distribution file for the module. 
  This overwrites  one defined in yaml package file. 
:yvars:`envmodule: True`
  Defines that the build is for the environment module.
:yvars:`src_tarball: none`
  There is no source distribution file for the module. 
  This overwrites  one defined in yaml package file. 
:yvars:`category:`
  Initially empty here, set to a correct value in the module yaml file.
  See available categories in :ref:`category`.
:yvars:`pkgname: "{{baserpm}}-module"`
  Sets the RPM name form the base RPM for the package.
:yvars:`shortname: "{{name}}"`
  A default. Can override when needed in module yaml file. 
:yvars:`build:`
  Redefine targets inherited from the package yaml files as there are no
  builds associated with module files.

  .. code-block:: yaml

     configure: echo
     pkgmake: echo
:yvars:`install:`
  Redefine targets inherited from the package yaml files as the only install
  is the module file in a specific path. 

  .. code-block:: yaml

     makeinstall: echo
     installextra:

:yvars:`requires: "{{module.requires}}"`
  Default. Defines what RPMS are prerequisites for the given module RPM to be
  installed.  This  corresponds to the software package RPM, ``rcic-module-support``
  RPM, and any modules that were used for the compilation of the  software
  package. This can be overwritten for specific modules (rarely needed).

:yvars:`prereq: "{{module.prereq}}"`
  Default. Defines modules that need to be loaded by the environment module file.
  This by default is set to the modules used during the compilation  of the
  software package. This can be overwritten for specific modules (rarely needed).

:yvars:`provides: "{{module.provides}}"`
  Default. This indicate what the module RPM provides. It is very important
  as a correct definition makes a robust RPM distribution. Typically for a
  module RPM provides are (example for a *diamond* package):

  .. parsed-literal::
     :command:`pm -q --provides diamond_2.0.15-module-2.0.15-1.x86_64`
     diamond/2.0.15
     diamond_2.0.15-module = 2.0.15-1
     diamond_2.0.15-module(x86-64) = 2.0.15-1

  The first line ``diamond/2.0.15`` allows :command:`yum` to find neeeded
  dependencies.

:yvars:`files:`
  Set to "{{module.category_path}}" which is a single file 

:yvars:`rpm:`
  We redefine here just one variable :yvars:`extras` and set it as:

  .. code-block:: yaml

     rpm:
       extras: >
         %changelog\n%autochangelog\n\

  The :tt:`%changelog` and :tt:`%autochangelog` are the traditional sections for the RPM
  SPEC file. These are needed here  because :tt:`%source_date_epoch_from_changelog`
  is enabled globally be default in the RPM macros distributed by the OS and
  when enabled requires these macros.

:yvars:`mod_defaults: &Module`
  This is a definition of a default module. Here, the :yvars:`mod_defaults` is 
  a key name and the :yvars:`&Module` defines its reusable anchor.
  The anchor  allows to inherit the entire contents of the defined
  :yvars:`mod_defaults` block in any yaml file, usually yaml module file 
  or in the other definitions in this `rcic-module.yaml` file.
  See full contents of this block in the repo file. 

  In the next few definitions we use this anchor to rewrite some values for
  the default module.

.. _module_definition:

:yvars:`module:`
  This is a basic module that simply inherits everything from :yvars:`mod_defaults`:

    .. code-block:: yaml

       module:
         <<: *Module

  Then in any module yaml file we can simply use  this definition via
  including ``rcic-module.yaml``.

  If changes are needed they can be minimal
  overriding only specific parts of the definition. For example for *awscli* module:

    .. code-block:: yaml

       !include awscli.yaml
       !include rcic-module.yaml
       ---
       - package: awscli module
         category: TOOLS
         module:
           prereq:
           setenv:
           prepend_path:
             - PATH {{root}}/bin

  Here, in :yvars:`module:` we reset :yvars:`prereq`  to empty (no other
  modules were used during the build) and :yvars:`setenv` to 
  empty (no environment variables are needed for *awscli* software package).
  Similarly, we rewrite the :yvars:`prepand_path` to indicate only  :tt:`PATH`
  (original default block has :tt:`PATH`, :tt:`MANPATH`, etc).
  The overwrite is specific to each module, most are minor.

  **Examples of basic modules**:

  | ``bamtools/2.5.2`` - *bamtools* v.2.5.2
  | ``turbomole/7.5``  - *turbomole* v.7.5

:yvars:`moduleCompiler: &ModuleCompiler`
  Definition and an anchor for the modules with compiler specifications in
  their names. Here we overwrite for all such modules what the log name 
  is, what the name is and the path to install (see the file for details).

  Then when we need to write a module with such specs we simply use this
  anchor and some overwrites. For example in ``sqlite3-module.yaml``
  from *simulations-admix*:

  .. literalinclude:: files/sqlite3-module.yaml
     :language: yaml

  Note, here in the last 6 lines we inherit everything that was defined in base module, then apply
  all the updates defined via anchor :yvars:`*ModuleCompiler` and 
  reset in this specifc case :yvars:`prepend_path` (original had more
  definitions then are needed for this case).

  **Examples of modules with compiler specifications**:

  | ``gromacs/2024.2/gcc.11.2.0`` - *gromacs*  v.2024.2 compiled with GCC v.11.2.0
  | ``hdf5/1.13.1/intel.2022.2`` - *hdf5* v.1.13.1 compiled with Intel v.2022.2

:yvars:`moduleCompilerMpi: &ModuleCompilerMpi`
  Definition and an anchor for the modules with compiler, interconnect and a
  few other (cuda) specifications specifications.
  
  Here we overwrite for all such modules what the log name 
  is, what the name is and the path to install (see the file for details).

  To use this definition  in the module yaml file we use the anchor :yvars:`*ModuleCompilerMpi`
  and some overwrites. For example in ``hdf5-parallel-module.yaml``
  from *fileformats-admix*:

  .. literalinclude:: files/hdf5-parallel-module.yaml
     :language: yaml

  **Examples of modules with compiler, interconnect and other specifications**:

  | ``hdf5/1.13.1/intel.2022.2-openmpi.4.1.2`` - *hdf5* v.1.13.1 compiled with Intel v.2022.2  and OpenMPI v.4.1.2
  | ``qe/7.1/intel.2022.2-cudasdk.22.9.openmpi.4.1.2`` - *Quantum Espresso* compiled with Intel v.2022.2, CudaSDK v.22.9 and OpenMPI v.4.1.2
