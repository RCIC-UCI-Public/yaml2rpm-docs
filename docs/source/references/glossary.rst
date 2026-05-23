Glossary
========

This page includes a number of terms that we use in our documentation.

.. glossary::

   admix
     is a loosely related collection of software packages built for a specific 
     discipline, for example chemistry, compilers, etc.

   categories
     Categories are paths where we install software modules. A category is 
     a loose collection of  software related by science of applicability
     Currently we define the following categories:

     - AI-LEARNING
     - BIOTOOLS
     - CHEMISTRY
     - COMPILERS
     - EARTHSCI
     - ENGINEERING
     - GENOMICS
     - IMAGING
     - LANGUAGES
     - LIBRARIES
     - PHYSICS
     - STATISTICS
     - TOOLS
     - $HOME/modulefiles

     The last item allows users to install their own modules in ``$HOME/modulefiles/``.

   DNF
     is the major version of YUM, a package manager for RPM-based Linux distributions.

   github home
      https://github.com/orgs/RCIC-UCI-Public/repositories
      holds all repositories for YAML2RPM admixes.

   main script
     The python script ``gen-definitions.py`` is a main processing script and driver
     that parses yaml files and generates required definitions and files for RPM build.

   project home
     https://yaml2rpm.readthedocs.io

   RPM 
     The RPM Package Manager (RPM) is a powerful command line driven
     package management system capable of installing, uninstalling,
     verifying, querying, and updating software packages. Each software
     package consists of an archive of files along with information about
     the package like its version, a description, etc.

   rpmbuild
     A command used to build both binary and source software RPM packages.

   YAML2RPM
      Yaml-to-RPM is a Generic Methodology for building and packaging
      relatively complex software as RPMs from yaml description files.
      At its core, it creates packages in the RPM format, but without 
      the pain of manually building and maintaining spec files.

   yaml conditional 
     An extension to the standard yaml processing. A variable takes a
     different value depending on the resolution of a conditioal
     statement of the form: :yvars:`!ifeq "{{varname}},X,val1,val2"`

     which means `if varname is equal to X the result of the
     whole expression is val1 otherwise the result is val2`.

   yaml variable include 
     An extension to the standard yaml processing. Used to include
     the contents of another yaml file into one variable: :yvars:`site: !include name.yaml`

     Then the included file variables can be accessed via their names as :yvars:`{{site.VarName}}`.

   yaml2rpm home
      Top level directory where all support files for YAML2RPM build are
      installed. Currently set to **/opt/rcic**.

