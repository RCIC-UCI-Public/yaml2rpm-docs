Admixbuilder
=============

.. _admixbuilder:

High-level builder for UCI Admix collection
An :guilabel:`admix` is a loosely related collection of software packages 
built for a specific discipline, for example chemistry, compilers, etc

Purpose
-------

This admix is used for keeping track of what is available for a build in other admixes 

Files
-----

``buildorder``
  is an ASCII text file that specifies an order in which admixes should be built.
  The ordering is needed as some admixes use RPMS that are built in some other
  admixes, such as RPMS for gcc compiler. 


``Makefile``
  Targets in this file  check out all other admixes git repositories, 
  download sources for the admixes builds, make build  for each one and, etc.


``depinfo.yaml``
  This file is generated via a target in ``Makefile``. The file contains modules info
  for all the admixes and all the modules inside them . The generated file format is (per module)

  .. code-block:: yaml
  
     macs_2.2.7.1-module:
       category: BIOTOOLS
       requires:
         - python/3.8.0
       provides:
         - macs/2.2.7.1

``deplist.yaml``
  This file is generated via a target in ``Makefile``. It contains  information about 
  dependencies among the modules such as what other modules a given module in the
  admix requires or provides. The generated file format is (per admix):

  .. code-block:: yaml

     gcc-admix:
       requires:
          - gcc/11.2.0
          - gcc/6.5.0
          - gcc/8.4.0
       provides:
          - gcc/11.2.0
          - gcc/6.5.0
          - gcc/8.4.0


``distro.sh``
  Bash script that creates a Yum repo distro from a set of RPMS in different directories

``depend.py``
  Python script that takes as input a  file (default is ``deplist.yaml``) and create graphs of 
  admixes dependencies.

``trace.py``
  Python script  that takes as an input a ``depinfo.yaml`` file and 
  outputs a list of all packages by admix that depend on a given package.
  This is a dependency tree among all the packages, showing 
  requires, provides, category for all packages

