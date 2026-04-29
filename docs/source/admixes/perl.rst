.. _perl_admix:

Perl
=====

**Table of contents:**

.. contents::
   :local:

Building
--------

The `perl-admix repository <https://github.com/RCIC-UCI-Public/perl-admix/>`_
is used to build multiple versions of Perl.

Perl is relatively complex build and requires local changes to its ``Makefile``
and a few custom scripts to accomplish multiple builds for multiple versions.

Here is the full process for rebuilding Perl and its associated modules present in the repo:

.. parsed-literal::
   :command:`git clone https://github.com/RCIC-UCI-Public/perl-admix.git
   cd perl-admix
   make buildall-parallel &> buildall.log &`

.. warning::
   This process will install RPMs for two Perl versions (|530| and |534|) as it builds.
   You should do this on a 'disposable' build system.


The following sections provide detailed explanation about repo files,
build process, and adding new modules step-by-step.

.. _perl_admix_files:

Files description
-----------------

.. _perl_admix_files_top:

At the top level
~~~~~~~~~~~~~~~~~~~~~~

Standard files and directories present in every admix as described in
:ref:`what files are in yamlspecs <admixrepo_files_yamlspecs>`.

.. _perl_admix_files_yamlspecs:

In yamlspecs/
~~~~~~~~~~~~~

Standard files
^^^^^^^^^^^^^^

When building Perl modules we not only need to build different versions of
Perl itself but also need to have different modules that were requested by the users
in order to support different types of applications.

Such modules trigger its own chain of dependent Perl modules that need to be
installed. We created 3 different groups (names and division into groups are logical)
to handle such requests for modules related to:

  - bio - bioperl applications
  - gen - genomics  applications
  - meta - metagenomics applications

The division of modules into these three groups is somewhat arbitrary.
There is a specific order when each group can be built because of
so many dependencies. We have to handle such dependencies carefully so that we do not
create circular references during the build.

``packages.yaml`` (required)
  Yaml format, describes specifics of this admix build.

  .. literalinclude:: files/perl-admix-packages.yaml
      :language: yaml

  Most of the variables in this file are standard
  (:yvars:`site`, :yvars:`system`, :yvars:`bootstrap`, :yvars:`build`, :yvars:`manifest`, :yvars:`sets`).
  There are a few new variables in this file that allow us
  to build multiple versions of Perl in parallel and make sure that the
  specific modules for each set can be built only after their dependencies are
  already built and installed.

  - :yvars:`bootstrap` and :yvars:`build` - empty, no packages in the base
    set. All build will be in the specific sets.

  - :yvars:`sets` - lists the logical sets of related packages that are built and installed together
    just like in any other admix. But here each set is defined as a *serialset*, one for each version of Perl.

  - :yvars:`serialsets` - each *serialset* has a name and is a list of sets for a specific Perl version.
    These sets describe related packages for each version of Perl that are built serially in order to satisfy modules dependencies.
    Here we define two *serialsets* :yvars:`serialsets.perl530` and :yvars:`serialsets.perl534`, one for each version of Perl.
    In each *serialset* there are 4 sets defined in exact order to be built.

  There are specific dependencies among modules defined in *bio*, *gen* and *meta* groups and it is
  important to build those sets in that exact order. But there are no
  dependencices between the serial sets for different versions of Perl,
  this is why we can define separate *serialsets* and build RPMS for both Perl versions simultaneously.

  The parallel build for serialsets :yvars:`serialset.perl530` and :yvars:`serialset.perl534`
  will start at the same time (starting with serial sets :yvars:`530` and :yvars:`534` respectively).
  The next build (in order) will start automatically as soon as the previous one is
  finished:

  .. table::
     :class: noscroll-table

     +-------+--------------+---------------+
     | Build | Perl 530     |  Perl 534     |
     | order | serialset    |  serialset    |
     +=======+==============+===============+
     |   1   |  530         | 534           |
     +-------+--------------+---------------+
     |   2   |  530-meta    | 534-meta      |
     +-------+--------------+---------------+
     |   3   |  530-bio     | 534-bio       |
     +-------+--------------+---------------+
     |   4   |  530-gen     | 534-gen       |
     +-------+--------------+---------------+

``versions.yaml`` (required)
  Since there are no packages to build for the base set, this file just lists the admix name:

  .. literalinclude:: files/perl-admix-versions.yaml
      :language: yaml

``perl.yaml`` (required)
  This yaml file provides all the instructions to build base Perl RPM.

  .. literalinclude:: files/perl-admix-perl.yaml
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
  - :yvars:`bioperl_tarsources`, :yvars:`metacpan_tarsources`,
    :yvars:`genomics_tarsources` - show definitions for the source distribution
    files for a specific Perl version and specific group. Each of 3 distribution files will
    get uncompressed and untarred to get the individual modules packages
    sources. These 3 files are not used for building perl package
    itself but the names are used in the ``Makefiles`` when running specific targets.
    For each version of perl a different source distribution file is available
    and is defined in the corresponding versions file.

  - :yvars:`filter_requires` :red:`TODO check if still need`
  - :yvars:`rpmFilters` - here is set to **\*filterPerl**.  The definition is
    in ``rpm.yamls`` template.
  - :yvars:`provides` - specifies what to add to *provides* when RPM is
    created.  For example, for Perl |530| RPM package **perl_5.30.0(:VERSION) = 5.30.0**
    will be added. This is similar to what system-installed Perl package would
    have for its version.

``perl-module.yaml`` (required)
  This file describes an environment module build for each version of Perl.

  .. literalinclude:: files/perl-admix-perl-module.yaml
      :language: yaml

  The variables are:

  - include statements specify tempalte files to include when parsing this yaml file.

    - :yvars:`!include perl.yaml` -  specifies a package file to include when parsing this file.
      Each package module file always includes the package yaml file to get needed package definitions.
    - :yvars:`!include rcic-module.yaml` -  specifies a tempalte to include when parsing this file.
      The ``rcic-module.yaml`` is a default template file that defines generic variables for most module files.

      :red:`TODO add reference to this file and describe it in full`
  - :yvars:`CATEGORY` - a logical category name to assign this module to.  This
    will result in adding created module file to a directory specified by
    this variable, here to ``LANGUAGES`` (once the RPM is installed).

    :red:`TODO add reference to CATEGORY`
  - :yvars:`release` - an RPM release number to use. Default is 1 Or a release
    specified in the included package yaml file (if exists there).
    We can increase the release when some changes are done to the yaml file
    so that when a new RPM is created the release is updated. This allows old and new RPMs
    releases to be present in the yum repo without a conflict and yum will use the latest availalbe for
    the installation or for the update when requested.

.. _perl_admix_makefile:

Makefile
^^^^^^^^

The ``Makefile`` is specific to perl-admix.

* It includes a generic template via :yvars:`include $(YAML2RPM_HOME)/sys/Makefile` directive
  that provides defaults used for building RPMs;
* adds targets to override defaults. For example :yvars:`thawyamls`, :yvars:`thawsources`
  or :yvars:`addfilters`.
* add specific targets that are defined for the 3 groups of modules of for a
  creation of additional modules. For example, :yvars:`sysperl`, or any of
  targets that have *bio*, *meta* or *gen* in their names.

When executing any target defined in ``Makefile`` **always give it a set name
as an argument**, for example:

   .. parsed-literal::
      :command:`make bootstrap SET=534-bio`
      :command:`make -n metaprep SET=534-meta1`

The targets and definitions are grouped per 3 defined groups of modules
and for creation of additional modules (see names with *desired*)
and are easy to differentiate via a group name, for example for a **meta** group:

   .. code-block:: make

      # specific to metacpan/ modules
      BASE_SRCVER = $(shell $(GENERATE) --query=metacpan_tarsources perl.yaml)
      BASELINE = $(shell cat metacpan/buildorder)
      BASERPMS = $(addprefix perl_$(PERLVER)-,$(BASELINE)) perl_$(PERLVER)-baseline-metacpan

      ### metacpan targets
      # Only do real work if the set has meta in the name
      ifeq ($(findstring meta,$(SET)),meta)
      metaprep:
              for name in $(shell cat metacpan/buildorder) baseline-metacpan; do              \
                  /bin/cp metacpan/$$name.yaml .;                                             \
              done

The ``Makefile`` needs to change only when a completely new group of
applications is added, In this case follow the existing definitions schema  in
the file ( see targets with *bio*, *meta* or *gen* in their names).

.. _perl_admix_sets:

Set specific
^^^^^^^^^^^^

The set files and corresponding versions files enable us to create multiple
versions of desired modules for multiple versions of Perl.

Here, we have two versions of Perl and 3 groups, plus the *base* set for each
version.  This results in the following matrix of sets and their corresponding
versions:

  .. table::
     :class: noscroll-table

     +---------+-------------------+------------------------+
     | Perl    | Set               |  Versions              |
     | version | file              |  file                  |
     +---------+-------------------+------------------------+
     | |530|   | set-530.yaml      | versions-530.yaml      |
     |         |                   |                        |
     |         | set-530-bio.yaml  | versions-530-bio.yaml  |
     |         |                   |                        |
     |         | set-530-gen.yaml  | versions-530-gen.yaml  |
     |         |                   |                        |
     |         | set-530-meta.yaml | versions-530-meta.yaml |
     +---------+-------------------+------------------------+
     | |534|   | set-534.yaml      | versions-534.yaml      |
     |         |                   |                        |
     |         | set-534-bio.yaml  | versions-534-bio.yaml  |
     |         |                   |                        |
     |         | set-534-gen.yaml  | versions-534-gen.yaml  |
     |         |                   |                        |
     |         | set-534-meta.yaml | versions-534-meta.yaml |
     +---------+-------------------+------------------------+

Any individual set can be built separately, for example:

   .. parsed-literal::
      :command:`make bootstrap SET=534-bio`

.. note:: Individual sets for a given Perl version need to be build in order they are
          listed in ``packages.yaml`` file because of inter-module dependencies.

.. _perl_admix_scripts:

Scripts
^^^^^^^

There are a few scripts that we created to enable specific tasks.
See the scripts files contents in `perl-admix repository <https://github.com/RCIC-UCI-Public/perl-admix/>`_.
All the scripts are specific to perl-admix.

``add-filters.sh``
  This bash script is used to create filters for rewriting Perl RPMs *provides* and *requires*.
  Filters are created in the package temporary build directory when building RPM.
  Naming convention is: ``filter-provides-NAME.sh`` and ``filter-requires-NAME.sh``
  where NAME is a specific perl module name taken from a package yaml file variable :yvars:`name`.
  For perl package these files will be ``filter-provides-perl.sh`` and ``filter-requires-perl.sh``.
  This script is called automatically by ``Makefile`` by a target
  **addfilters** when building the RPM package.

``depend.py``
  This Python script is called from the ``Makefile`` when there is a need to create
  some new modules for the existing groups or add a new group of modules.
  This script was used to create all yaml files for the modules in groups
  *bio*, *gen* and *meta*.

  The script will take as an input a list of desired Perl modules, query CPAN
  for the modules availability and their prerequisites and create yaml files for found modules.
  In some instances, a module will be provided by the `parent` module distribution.
  In such cases a mapping from parent to module will be given.
  We can then use the created yaml files to build RPMs.
  See a build example in :ref:`perl_admix_add_modules`.

``MyConfig.pm.in``
  This is CPAN's system wide configuration file, it provides
  defaults for CPAN related directories. By default this file
  is generated as ``/root/.cpan/CPAN/MyConfig.pm`` but we need to override
  some definitions.  See a build example in :ref:`perl_admix_add_modules`.

.. _perl_admix_add_modules:

Add new modules
---------------

The steps below outline how one can automate to a large degree creation of the
additional Perl modules RPMs. Because the Perl modules do not always obey the
build process and do not provide all the dependency information, there will be
always a case that will need a manual adjustment.

The adjustment usually involves overwriting requires/provides, or changing the
package name, or changing the order in a ``buildorder`` file.
For the requires/provides see examples of the filters in the ``metacpan/Package-Stash.yaml``
or ``metacpan/ExtUtils-Helpers.yaml`` or any other yaml files that contain
:yvars:`filter_requires` or :yvars:`filter_provides`` directives.

For the ``buildorder`` updates, follow error messages during RPMs build and check for errors in the
output file, then adjust the ``buildprder`` (reorder modules in it ) and rerun build RPM command.

The standard, step-by-step outline to add a new set of perl modules is:

1. Create a file ``desired`` that lists desired Perl modules names  one per line using Perl module name
   schema, foe example:

   .. code-block:: text

      Moose
      Moose::Role
      File::Copy::Recursive
      HTML::Template
      XML::Simple

   Note, here there are  two modules that are related, **Moose** is a parent
   module and  **Moose::Role** is a child module.
#. Before the next step make sure there is ``~/.cpan/CPAN/MyConfig.pm`` file.
   We can generate this file before running any CPAN commands via:

   .. parsed-literal::
      :command:`make MyConfig.pm
      mkdir -p  ~/.cpan/CPAN/
      cp MyConfig.pm  ~/.cpan/CPAN/MyConfig.pm`

#. Run a program that will query CPAN for the modules and their prerequisites
   and create yaml files for found modules. In some instances, a module will be provided
   by the `parent` module distribution. Use Perl version for which  you are building the
   desired modules. For example, to create the yaml files for modules listed
   in ``desired`` for Perl |530|:

   .. parsed-literal::
      :command:`cd yamspecs/
      make desired-yaml SET=530`

   The stdout output will show the commands that will be executed by ``make`` and
   print info what Perl module it is working on. At the end it will list
   written yaml files and a mapping info (from parent to child module if exist).

   In our example, the mapping line is

   .. code-block:: python

      MAPPING {'Moose::Role': ('Moose','2.4000'), 'List::Util': ('Scalar::List::Utils','1.70')}

   This means there were two mappings created and they are:

     | (1) ``Moose.yaml`` the parent module **Moose** provides **Moose::Role**
     | (2) ``Scalar-List-Utils.yaml`` parent module  **Scalar::List::Utils** provides  **List::Utils**

   **Output Files**

   After the :command:`make` finishes, there are output files:

     * ``versions-desired`` is just the info file with the following content:

       .. code-block:: text

          To install the specified desired perl modules:
              Moose
              Moose::Role
              File::Copy::Recursive
              HTML::Template
              XML::Simple

          the following packages and their versions will need to be installed:
          File-Copy-Recursive: "0.45"
          HTML-Template: "2.97"
          XML-Simple: "2.25"
          Class-Load-XS: "0.10"
          Devel-OverloadInfo: "0.008"
          Scalar-List-Utils: "1.70"
          Module-Runtime-Conflicts: "0.003"
          Package-Stash-XS: "0.30"
          Moose: "2.4000"

     * ``versions-bootstrap`` with the following content:

       .. code-block:: text

          File_Copy_Recursive: "0.45"
          File_Copy_Recursive_loc: "D/DM/DMUEY"
          HTML_Template: "2.97"
          HTML_Template_loc: "S/SA/SAMTREGAR"
          XML_Simple: "2.25"
          XML_Simple_loc: "G/GR/GRANTM"
          Class_Load_XS: "0.10"
          Class_Load_XS_loc: "E/ET/ETHER"
          Devel_OverloadInfo: "0.008"
          Devel_OverloadInfo_loc: "I/IL/ILMARI"
          Scalar_List_Utils: "1.70"
          Scalar_List_Utils_loc: "P/PE/PEVANS"
          Module_Runtime_Conflicts: "0.003"
          Module_Runtime_Conflicts_loc: "E/ET/ETHER"
          Package_Stash_XS: "0.30"
          Package_Stash_XS_loc: "E/ET/ETHER"
          Moose: "2.4000"
          Moose_loc: "E/ET/ETHER"

     * ``buildorder`` with the following content:

       .. code-block:: text

           - File-Copy-Recursive
           - HTML-Template
           - XML-Simple
           - Class-Load-XS
           - Devel-OverloadInfo
           - Scalar-List-Utils
           - Module-Runtime-Conflicts
           - Package-Stash-XS
           - Moose

     * Yaml file for each module listed in ``buildorder``:

       | ``File-Copy-Recursive.yaml``
       | ``HTML-Template.yaml``
       | ``XML-Simple.yaml``
       | ``Class-Load-XS.yaml``
       | ``Devel-OverloadInfo.yaml``
       | ``Scalar-List-Utils.yaml``
       | ``Module-Runtime-Conflicts.yaml``
       | ``Package-Stash-XS.yaml``
       | ``Moose.yaml``


#. Download all source distributions for the generated yaml files:

   .. parsed-literal::
      :command:`make desired-download SET=530`

   This command will use the :yvars:`vendor_source` in yaml files and
   download the source distributions.

#. Build and install RPMS for desired modules:

   .. parsed-literal::
      :command:`make desired-build SET=530 | tee out 2>&1`

   If there are errors, check them in order they are built
   (in ``buildorder``) and follow the errors to fix. These are the cases where manual adjustment
   of the yaml file will be needed to incorporate the fixes. There is no
   single recipe, the errors are specific to each module and thehe is usually
   enough info in the output to figure out what changes are needed.
   Browse through the module yaml files in repo for existing examples.

#. Once the build goes well and you have all the RPMs, create new versions
   and set files and update ``packages.yaml`` (see other versions files in the repo
   for an exact layout).

   For example, we want to call this newly create collection of modules **trial**
   and the files and updates are as follows:

   * Create ``versions-530-trial.yaml`` with the initial lines:

     .. code-block:: yaml

        !include versions-530.yaml
        ---
        baseline_bioperl: "{{versions.perl}}"

     Add the contents of the ``versions-bootstrap.yaml`` to it.

   * Create ``set-530-trial.yaml`` with the initial lines:

     .. code-block:: yaml

        !include packages.yaml
        ---
        versions: versions-530-trial.yaml
        bootstrap:

     Add the contents of the ``buildorder`` to it.

   * Update the ``packages.yaml`` file and add the :yvars:`530-trial` to the serial set
     :yvars:`perl530` after the already existing sets:

     .. code-block:: yaml

        serialsets:
           perl530:
              - "530"
              - "530-meta"
              - "530-bio"
              - "530-gen"
              - "530-trial"

   .. note:: What if the modules are to be added not to a new set but to already
      existing one, let say **bio**? Instead of creating new versions and set yaml
      files simply:

        * append the contents of ``versions-bootstrap.yaml`` to ``versions-530-bio.yaml``
        * append the contents of ``buildorder`` to ``set-530-bio.yaml``

      No changes are needed in ``packages.yaml`` in this case.

   * Update the ``Makefile``. This is by far the most complex. Carefully
     follow the existing notations for the other groups (*bio*, *meta*, *gen*)
     and add the new targets and definitions for this new set *trial*.

#. To remove built and installed RPMs

   .. parsed-literal::
      :command:`make desired-erase SET=530-trial`

#. Repeat the process for another Perl version.

   Since we usually try to build the same modules for both Perl versions, the
   above steps need to be repeated for Perl |534|. Because of the Perl version
   change the versions of the modules and distribution files are usually
   different and so are the dependencies or additional needed modules.

   Steps:

   * Use the same ``desired`` file
   * Run script with desired version of Perl

     .. parsed-literal::
        :command:`cd yamspecs/
        make desired-yaml SET=534`

   * download the  distro files for new versions:

     .. parsed-literal::
        :command:`make desired-download SET=530`

   * Examine created files, compare them to
     the ones that were created for a previosu Perl version and apply
     similar changes (if there were any manual adjustments).

   * Build and install RPMS:

     .. parsed-literal::
        :command:`make desired-build SET=530 | tee out 2&>1`

   * Once all RPMs are built without errors, create ``set-534-trial.yaml``,
     ``versions-534-trial.yaml``, and update ``packages.yaml``.

   * Remove installed and built RPMS for this set

     .. parsed-literal::
        :command:`make desired-erase SET=534-trial`


.. |530| replace:: 5.30.0
.. |534| replace:: 5.34.1
