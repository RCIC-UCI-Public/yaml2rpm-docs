Glossary
========

This page includes a number of terms that we use in our documentation.

.. glossary::

   project home
     https://yaml2rpm.readthedocs.io

   github home
      All repositories for YAML2RPM admixes can be found at
	  https://github.com/orgs/RCIC-UCI-Public/repositories

   yaml2rpm home
      Top level directory wher all support files for YAMKL2RPM build are
	  installed. Currently set to **/opt/rcic**.

   main script
     The python script ``gen-definitions.py`` is a main processing script and driver
     that parses yaml files and generates required definitions and files for RPM build.

   categories
     Categories are paths where we install software modules. A category is 
     a loose collection of  software related by science of applicability
     Currently we define the following categories:

     - AI LEARNING
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

     The last item allows users to install their own modules in ``$HOME/modulefiles/``
