.. _perl_admix:

Perl
=====

.. contents::
   :local:

The `perl-admix repository <https://github.com/RCIC-UCI-Public/perl-admix/>`_ builds
multiple versions of Perl. 

Perl is relatively complex build and requires local changes to its Makefile to
accomplish multiple builds for multiple versions.

| Here is the full process for rebuilding Perl using the `perl-admix repository <https://github.com/RCIC-UCI-Public/perl-admix/>`_.
| This process will install RPMs as it builds. You should do this on a disposable build system:

.. parsed-literal:: 
   :command:`git clone https://github.com/RCIC-UCI-Public/perl-admix.git
   cd perl-admix
   make download
   cd yamlspecs
   (make bootstrap &> /tmp/bootstrap-gcc.log make &> /tmp/build-gcc.log) &`

.. _perl_admix_files_top:

Files at the top level
-----------------------

Standard files and directories present in every admix as described in 
:ref:`what files are in yamlspecs <admixrepo_files_yamlspecs>`.

.. _perl_admix_files_yamlspecs:

Files in yamlspecs/
-------------------

Standard files
~~~~~~~~~~~~~~

When building Perl modules we not only need to build different versions of
Perl itself but also need to have different modules that were requested by the users
in order to support different types of applications. 

Such modules trigger its own chain of dependent Perl modules that need to be
installed. We created 3 different groups (names and division into groups are logical)
to handle such requests for modules related to : 
  
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

  Most variables are standard and are descirbe in :red:`TODO ref`. 
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
    created.  For example, for Perl 5.30.0 RPM package **perl_5.30.0(:VERSION) = 5.30.0**
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

.. _perl_admix_sets:

Sets
~~~~

.. _perl_admix_scripts:

Scripts
~~~~~~~

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
  This is CPAN.pm's system wide configuration file, it provides
  defaults for CPAN related directories. By default this file
  is generated as ``/root/.cpan/CPAN/MyConfig.pm`` but we need to override
  some definitions.  See a build example in :ref:`perl_admix_add_modules`.

.. _perl_admix_add_modules:

How to add new modules
----------------------

The steps below outline how one can automate to a large degree creation of the
additional Perl modules RPMs. Because the Perl modules do not always obey the
build process and do not provide all the dependency information, there will be
always a case that will need a manual adjustment.

The adjustment usually involves overwriting requires/provides, or changing the
package name, or changing the order in a ``buildorder`` file.
For the requires/provides see examples of the filters in the ``metacpan/Package-Stash.yaml``
or ``metacpan/ExtUtils-Helpers.yaml`` or other yaml files that contain **filter_requires** or
**filter_provides** directives.

For the ``buildorder`` updates, follow error messages during RPMs build and check for errors in the
output file, then adjust the ``buildprder`` and rerun build RPM command.

The standard, no change step outline is:

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
#. Before the next step make sure there is ``~/.cpan/CPAN/MyConfig.pm`` file
   We can generate this file before running any cpan commands via:

   .. parsed-literal:: 
      :command:`make MyConfig.pm
      mkdir -p  ~/.cpan/CPAN/
      cp MyConfig.pm  ~/.cpan/CPAN/MyConfig.pm`
  
#. Run a program that will query CPAN for the modules and their prerequisites
   and create yaml files for found modules. In some instances, a module will be provided
   by the `parent` modules distribution. Use Perl version for which  you are building the
   desired modules. For example, to create the yaml files for modules listed
   in ``desired`` for Perl 5.30.0:
   
   .. parsed-literal:: 
      :command:`cd yamspecs/
      make desired-yaml SET=530`

   The stdout output will show the commands that will be executed by ~~make`` and
   print info on what Perl module it is working. At the end it will list yaml
   that were written and a mapping info.

   In our example, the mapping line is 

   .. code-block:: python

      MAPPING {'Moose::Role': ('Moose','2.4000'), 'List::Util': ('Scalar::List::Utils','1.70')}

   This means there were two mappings created and they are:

     | (1) ``Moose.yaml`` the parent module **Moose** provides **Moose::Role**
     | (2) ``Scalar-List-Utils.yaml`` parent module  **Scalar::List::Utils** provides  **List::Utils** 

   **Output Files**

   After the :command:`make` finishes, there are output files created:

     * ``versions-desired`` is the info file with the following content:

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

       The contents of this file needs to be added to the ``versions-<SET>.yaml``.

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

        The contents of this file needs to be added to the ``set-<SET>.yaml``.

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


#. Download all source distributions for generated yaml files:

   .. parsed-literal:: 
      :command:`make desired-download`

#. Build and install RPMS for desired modules:

   .. parsed-literal:: 
      :command:`make desired-build | tee out 2>&1`
   
   If there are errors, check them in order of yaml files being used for build
   and follow the errors to fix. These are the cases where manual adjustment
   of the yaml file will be needed to incorporate the fixes.

#. Once the build goes well and you have all the RPMs, need to create new versions
   and set files and update ``packages.yaml``. For example, we want to call this new set **530-trial**.
   a new set and its version file can be  created and  the set can be added to packages.yaml.

   * Create ``versions-530-trial.yaml`` with these initial lines:

     .. code-block:: yaml

        !include versions-530.yaml
        ---
        baseline_bioperl: "{{versions.perl}}"

     and add the contents of the ``versions-bootstrap.yaml``. See other versions
     files in the repo for an exact layout.

   * Create ``set-530-trial.yaml`` with these initial lines:

     .. code-block:: yaml

        !include packages.yaml
        ---
        versions: versions-530-trial.yaml
        bootstrap:

     and add the contents of the ``buildorder``. See other set
     files in the repo for an exact layout.

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


#. To remove built and installed RPMs

   .. parsed-literal:: 
      :command:`make desired-erase`
