RPM Directives
==============

.. _rpm_directives:


When building packages we sometimes need to define specific settings that
need to go to a spec file. Since we create spec files automatically 
we need to provide a way to add such definitions in the  packages yaml files.

We put common default and specific cases definitions in ``rpm.yaml`` file
(distributed by ``yaml2rpm`` RPM).  Directives are eventually 
transformed to a package spec file. 

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

     :yvars:`!include rpm.yaml`

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

