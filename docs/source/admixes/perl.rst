Perl
=====

.. _perl-admix:

The `perl-admix repository <https://github.com/RCIC-UCI-Public/perl-admix/>`_ builds
multiple versions of Perl. 

Perl is relatively complex build and requires local changes to its Makefile to
accomplish multiple builds for multiple versions.

| Here is the full process for rebuilding Perl using the `perl-admix repository <https://github.com/RCIC-UCI-Public/perl-admix/>`_.
| This process will install RPMs as it builds. You should do this on a disposable build system:

.. code-block:: bash

   git clone https://github.com/RCIC-UCI-Public/perl-admix.git
   cd perl-admix
   make download
   cd yamlspecs
   (make bootstrap &> /tmp/bootstrap-gcc.log make &> /tmp/build-gcc.log) &

Build details
-------------

When building Perl modules we not only need to build different versions of
Perl but also need to have different modules that were requested by the users
in order to support different types of applications. 
Such modules trigger its own chain of dependent Perl modules that need to be
installed. We created 3 different groups (names and division into groups are logical)
to handle such requests for modules related to : 
  
  - bio - bioperl applications
  - gen - genomics  applications
  - meta - metagenomics applications

The division of modules into these three groups is somewhat arbitrary.
In addition, there is a specific order when each can be built because of
so many dependencies. We have to handle such dependencies so that we do not
create circular references during the build.

``packages.yaml`` (required)
  Yaml format, describes specifics of this admix build.

  .. literalinclude:: files/perl-admix-packages.yaml
      :language: yaml

  Most of the variables in this file are standard
  (:yvars:`site`, :yvars:`system`, :yvars:`bootstrap`, :yvars:`build`, :yvars:`manifest`).
  There are a few new variables in this file that allow us 
  to build multiple versions of Perl in parallel and make sure that the
  specific modules for each set can be built only after their dependencies are
  already built and installed. 

  - :yvars:`bootstrap` and :yvars:`build` - empty, no packages in the base
    set. All build will be in the specific sets.
  - :yvars:`sets` - lists the logical sets of related packages that are built (and installed) together
    just like in any other admix. But here each set is defined as a *serialset*, one for each version of Perl.
    Each *serialset* is a list of sets. These *serialsets* will be build in parallel, but within each
    parallel build the defined serial sets will be built serially.
  - :yvars:`serialsets` - lists the sets of related packages that are built serially
    in order to satisfy modules dependencies. 
    Here we define two *serialsets* :yvars:`perl530` and :yvars:`perl534`, one for each version of Perl.
    In each *serialset* there are sets listed in exact order to be built serially. 

  There are specific dependencies among modules defined in *bio*, *gen* and *meta* and it is
  important to build those sets in that exact order. But there are no
  dependencices between the serial sets for different versions of Perl,
  this is why we can define separate *serialsets* and build RPMS for both Perl versions simultaneously.
  The build for *serialsets* 530 and 534 will  start at the same time and then any
  following set (in the same column) will start as soon as the previous one is
  finished: 

  .. table::
     :class: noscroll-table

     +-------+--------------+---------------+ 
     | build | Perl 530     |  Perl 534     |
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
  Since there are no packages to build, this file just lists the admix:

  .. literalinclude:: files/perl-admix-versions.yaml
      :language: yaml

``perl.yaml`` (required)
  This is a yaml file that provides all the instructions to build base Perl RPM.

  .. literalinclude:: files/perl-admix-perl.yaml
      :language: yaml

  The variables in the file are as follows:

  - :yvars:`!include` -  specifies what templates to include when parsing this file. 
    These templates define common variables that are neeed in all builds and
    using the include directive simplifies the comon code reuse and minimizes
    the overall code footprint.

    * ``rcic-package.yaml`` defines defaults for the variables used for the buildd.

      :red:`TODO add reference to this file and describe it in full`
    * ``rpm.yaml`` defines specific RPM directives to use when creating
      RPM files. These definitions will override what :command:`rpmbuild` uses by default.

      :red:`TODO add reference to this file and describe it in full`

``perl-module.yaml`` (required)
  This file describes an environment module build for each version of Perl.

  .. literalinclude:: files/perl-admix-perl-module.yaml
      :language: yaml

  The variables in the file are as follows:

  - :yvars:`!include` -  specifies what templates to include when parsing this file. 

    * ``perl.yaml`` - each package module file always includes the package
      yaml that provide needed package definitions.
    * ``rcic-module.yaml`` - this is a default template file that defines
      generic variables for most module files.

      :red:`TODO add reference to this file and describe it in full`
  - :yvars:`CATEGORY` - a logical category name to assign this module to.  This
    will result in adding created module file to a directory specified by
    this variable, here to ``LANGUAGES`` (once the RPM is installed).
  - :yvars:`release` - an RPM release number to use. A default is 1. We can
    increase the release when some changes are done to the yaml file 
    and when a new RPM is created the release is updated. This allows old and new RPMs
    to be present in the yum repo without a conflict and yum will use the latest availalbe for
    the installation or for the update when requested.

``add-filters.sh`` (required)
  This file  is used to create filters for rewriting Perl RPMs provides/requires
  Filters are created in the package temporary build directory where building RPM.
  Naming convention: ``filter-provides-NAME.sh`` and ``filter-requires-NAME.sh``
  where NAME is a specific perl module name taken from a package yaml file variable :yvars:`name`.
  For perl package these files will be ``filter-provides-perl.sh`` and
  ``filter-requires-perl.sh``.

  See the file contents in `perl-admix repository <https://github.com/RCIC-UCI-Public/perl-admix/>`_.
