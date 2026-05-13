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
There is no strict naming convention, usually we pick the software name: *name.yaml*.

An example ``ucx.yaml`` from `buildlibs-admix repository <https://github.com/RCIC-UCI-Public/buildlibs-admix/>`_:

  .. literalinclude:: files/ucx.yaml
     :language: yaml

Some variable here are standard for all, others are software specific.

**Standard variables**

  These variables are standard and must be present in each package yaml file
  unless indicated otherwise.

  - :yvars:`!include rcic-package.yaml` - the  include statement specifies 
    template files to include when parsing this yaml file.

    These include files  define common variables that are needed in all builds and
    using the include directive simplifies the common code reuse and minimizes
    the overall code footprint.

    Here, a ``rcic-package.yaml`` is a standard template file that defines
    defaults for the variables used during the build. This is the most common
    template included in the packages yaml files. Other files to include can be:

	- specific common files defined for an admix and these common files in turn would include ``rcic-packages.yaml``.
	- ``rpm.yaml`` a template that defines variables for RPM specs. 

  - :yvars:`package` - a short package name description. Very short usually one-two words. 
  - :yvars:`name` - a package name that will be used in the RPM name. Try to
    keep this as close to the software name as possible. We try to keep the
    same naming convention here as the software developers use. The names can
    contain dashes, capital letters, very infrequently numbers.
    For example: 

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
    
  - :yvars:`versions: !include versions.yaml` - include statement specifies
	what versions file to include when parsing.  Once included the variables
	defined there become available via :yvars:`versions.VarName`.

  - :yvars:`version` - the version of the package. 
  - :yvars:`release` - the release number to use for RPM. If not present defaults to 1.

**Specific  variables**
  TODO

.. _package_module_yaml:

Package module file
--------------------

TODO

.. _package_common:

Common files
------------

TODO
