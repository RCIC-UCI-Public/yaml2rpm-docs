.. _yamlpkg:

Package YAML Format
===================

Any software package can have  a few yaml files that we use to build RPMs.
These are package yaml files, package module yaml files and sometimes 
common files to be included in them. The following sections provide detailed
description and examples.

**Table of contents:**

.. contents::
   :local:

.. _package_yaml:

Package file
------------

A particular software package yaml file provides all the info
and instructions needed to create an RPM. 
There is no strict naming convention, usually we pick the software name: ``SWNAME.yaml``

An example ``ucx.yaml`` from `buildlibs-admix repository <https://github.com/RCIC-UCI-Public/buildlibs-admix/>`_:

  .. literalinclude:: files/ucx.yaml
     :language: yaml

Some variable here are standard for all, others are software specific.

**Standard variables**
  These variables must be present in each package yaml file unless indicated otherwise.

  :yvars:`!include rcic-package.yaml`
    The  include statement specifies template files to include when parsing this yaml file.

    These included files  define common variables that are needed in all builds and
    using the include directive simplifies the common code reuse and minimizes
    the overall code footprint.

    Here, a ``rcic-package.yaml`` is a standard template file that defines
    defaults for the variables used during the build. This is the most common
    template included in the packages yaml files. Other files to include can be:

      - Specific common files defined for an admix.
        These common files in turn would include ``rcic-packages.yaml``.
      - ``rpm.yaml`` a template that defines variables for RPM specs. 
        See :ref:`rpm.yaml` for details.

  :yvars:`package`
    A short package name description. Very short usually one-two words. 
  :yvars:`name`
    A package name that will be used in the RPM name. Try to
    keep this as close to the software name as possible. We try to keep the
    same naming convention here as the software developers use. The names can
    contain dashes, capital letters, very infrequently numbers.  For example: 

    +---------------+------------------------------------------------------+
    | Name          | Description                                          |
    +===============+======================================================+
    | picard-tools  | Set of Java command line tools                       |
    +---------------+------------------------------------------------------+
    | sqlite3       | SQLite3 library                                      |
    +---------------+------------------------------------------------------+
    | SPAdes        | toolkit for assembly and analysis of sequencing data.|
    +---------------+------------------------------------------------------+
    | ucx           | optimized communications layer for MPI               |
    +---------------+------------------------------------------------------+
    
  :yvars:`versions`
    Include statement specifies what versions file to include when parsing.
    Once included the variables defined there become available via :yvars:`{{versions.VarName}}`.

  :yvars:`version`
    The version of the package. 
  :yvars:`release`
    The release number to use for RPM. If not present defaults to 1.
  :yvars:`vendor_source`
    Specifies where we the source distribution file is from. In rare
    occasions this is just an explanation string, for example for the sources
    that are protected by the license.
  :yvars:`compiler`
    If present, defines what compiler to use (gcc, intel, etc). 
    If absent, the compiler info is taken from the ``site.yaml`` file.
  :yvars:`compiler_version`
    Defines a compiler version to use.
  :yvars:`description`
    A description that is passed  into the RPM and into the environment module file (if present). 
  :yvars:`shortdescription`
    Similar to :yvars:`description` but more concise. 
    If absent then :yvars:`description` is used by default.
  :yvars:`addfile`
    If present, defines  what additional files are needed for the build. Sometimes these
    are patches or filter scripts. They must exists at the same directory
    level as the package yaml file.
  :yvars:`build`
    A dictionary variable  that defines build specifics via its key-value pairs.  
    The defaults are taken from ``rcic-package.yaml`` file that is installed
    via ``yaml2rpm`` RPM. The defaults are overwritten as needed by each
    package yaml file. The standard variables here are

    | :yvars:`configure`
    | :yvars:`configure_args`
    | :yvars:`modules`
    | :yvars:`pkgmake`
    | :yvars:`target`

    Dictionary variables are accessed via its names and keys, for example :yvars:`{{build.modules}}`.
  :yvars:`install`
    Defines the install target :yvars:`makeinstall` for the Makefiles. 

**Specific  variables**
  These variables define setting that are specific to a single  software package.
  They define special cases for the configure, compile and install or anything
  else that is needed during these steps. This is an extension to the
  standard variables. For the ``ucx.yaml`` above:
  
  :yvars:`add_config_args`
    Defines specific configuration options only for specific *ucx* versions. 
  :yvars:`opts`
    Gets set to the value of above variable only for certain *ucx* versions.
    Then when used in :yvars:`{{build.configure_args}}` it is either empty for
    some versions and set to :yvars:`add_config_args` for others.

  Additional simple or dictionary variables  can be added as needed.
  They are referenced in exactly the same way as standard variables.

.. _package_module_yaml:

Package module file
--------------------

Many software packages need to have environment modules to be useful.
We use package module yaml files to create them. 
The file naming convention is inherited from the package yaml file name,
usually: ``SWNAME-module.yaml``. All module yaml files need to include :ref:`rcic-module.yaml`.

An example for a very simple module file ``bioconda-module.yaml``
from `bioconda-admix repository <https://github.com/RCIC-UCI-Public/bioconda-admix/>`_:

  .. code-block:: yaml

     !include bioconda.yaml
     !include rcic-module.yaml
     ---
     - package: bioconda module
       category: LANGUAGES

  For this, all definitions are taken from the included files. Only a couple
  of required variables are defined here.

A more complex example the ``ucx-module.yaml`` (works with the above ``ucx.yaml``):

  .. literalinclude:: files/ucx-module.yaml
     :language: yaml

**Standard variables**
  These are present in all module yaml files.

  :yvars:`!include`
    Specify what standard templates to include.
    Usually,  there are two files included:

      1. The package yaml file for the software. This is required. This is how we
         inherit all the variables needed for the RPM for this software.

      #. The system-wide template (installed via ``yaml2rpm`` RPM)
         ``rcic-module.yaml``. The template defines all the paths, variables, and
         any other info to put in the resulting module file.
  :yvars:`package`
    Define package. This overwrites what was in the included yaml file.

  :yvars:`module`
    Defines variables to use for the module. Most come from the included
    ``rcic-module.yaml`` file as defaults and  can be overwritten.
    There are a few special variables that are defined in ``rcic-module.yaml``
    file, see :ref:`module definition <module_definition>` for their meaning:

        * :yvars:`<<: *Module` 
        * :yvars:`<<: *ModuleCompiler` 
        * :yvars:`<<: *ModuleCompilerMpi` 

    :yvars:`prepend_path`
      Defines what PATHS this module overrides for :tt:`PATH`,
      :tt:`LD_LIBRARY_PATH``, :tt:`PKG_CONFIG_PATH` or :tt:`MANPATH`. 
      This depends  on the software. When not present defaults from included
      files are sufficient. See all paths in ``rcic-module.yaml`` file in
      `yaml2rpm repository <https://github.com/RCIC-UCI-Public/yaml2rpm/>`_.
    :yvars:`setenv`
      In a similar way,  this variable lists environment variables that are
      set with :command:`setenv` when the module is loaded. Some software
      requires very specific names set. 

  .. _category:

  :yvars:`category`
    Defines a logical category name to assign this module to.
    Categories are s imply logical groups we assign software to. 
    They correspond to the paths we we install RCIC-defined software environment modules.

    Their names  will be added to the :tt:`RCICMODULEPATH`
    environment variable which is then added to :tt:`MODULEPATH`. 
    When the modules RPMs are installed users automatically have access to them all.

    We define categories in ``rcicmodulespath`` file that is installed by ``yaml2rpm`` RPM.
    The names can be either groups of common tools (compilers) or software for a
    specific discipline (physics).  Currently, the categories are:

      +-------------------+-------------+-----------+
      | AI-LEARNING       | EARTHSCI    | LANGUAGES |
      +-------------------+-------------+-----------+
      | BIOTOOLS          | ENGINEERING | LIBRARIES |
      +-------------------+-------------+-----------+
      | CHEMISTRY         | GENOMICS    | PHYSICS   |
      +-------------------+-------------+-----------+
      | COMPILERS         | IMAGING     | STATISTICS|
      +-------------------+-------------+-----------+
      | $HOME/modulefiles |             | TOOLS     |
      +-------------------+-------------+-----------+

    A special category in above listing is :tt:`$HOME/modulefiles`. It provides our users
    with the ability to install their own modules in ``$HOME/modulefiles/`` directory if desired.
    We do not assign any of our build modules to it.

.. _package_common:

Common files
------------

In any admix there can be software packages that share some build or install
options. Instead of rewriting these for multiple files we create 
common files and then include them into package yaml files. The naming
convention is ``common.yaml``  but it can vary depending on what makes
logical sense for a set of files that would include it in the specific admix
(for example ``pycommon.yaml`` in *chemistry-admix*).

For example, in  `buildtools-admix repository <https://github.com/RCIC-UCI-Public/buildtools-admix/>`_
we create ``common.yaml`` and then include it in respective packages files
where needed. The contents of this ``common.yaml``:

  .. literalinclude:: files/common.yaml
     :language: yaml

The ``curl.yaml`` then can use the above definitions when it includes this file:

  .. literalinclude:: files/curl.yaml
     :language: yaml

While there are only a few lines  reused in this example, over many packages it adds up
and having a smaller code base is easier to debug and use.

Having common files is particularly advantageous in admixes for R4, Perl and
Python where many modules have repetitive blocks of code that is moved into
the common files.
