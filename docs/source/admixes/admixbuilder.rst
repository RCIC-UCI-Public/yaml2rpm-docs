Admixbuilder
=============

.. _admixbuilder:

High-level builder for UCI Admix collection.

An :term:`admix` is a loosely related collection of software packages 
built for a specific discipline, for example chemistry, compilers, etc

Purpose
-------

This admix is used for keeping track of what is available for a build in other admixes 
and what are relationships among different admixes. 

Prerequisites
-------------

This admix is not required  for building any of the RPMs in other admixes,
This admix provides a collection of `convenience` info.
The prerequisites are easily satisfied via stock RPMs: 

- ``python`` - to use with a few custom scripts
- ``graphviz`` - to create graphical representation of information collected
  from all other admixes.

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
  This file is generated via a target in ``Makefile``. The file contains
  dependencies among the modules such as what other modules a given module in the
  admix requires or provides for all the admixes and for all the modules and 
  packages inside them.  This is a dependency tree among all the packages, showing 
  requires, provides, category for all packages.
  Used by ``depend.py`` script. The generated file format is (per module)

  .. code-block:: yaml
  
     macs_2.2.7.1-module:
       category: BIOTOOLS
       requires:
         - python/3.8.0
       provides:
         - macs/2.2.7.1

  
``distro.sh``
  Bash script that creates a Yum repo distro from a set of RPMS in different directories

``depend.py``
  Python script that takes as input a file (default is ``deplist.yaml``) and
  creates graphs of 
  admixes dependencies written in `graph file language`. We generate
  dependencies  by admix, by category and by admix build order. 

``trace.py``
  Python script that takes as an input a  dependencies info file (default ``depinfo.yaml``)
  and a given package name and  prints  a list of all packages by admix that depend on this package.
  This tool provides an answer to the question: `If i change package X
  version Y  what other packages do i need to rebuild?`

  For example, for a packages ``icu`` this script execution shows  that no other packages will need
  a rebuilt if this package is recompiled:

  .. code-block:: bash

     ./trace.py icu
     Provider: buildtools-admix
         module icu/65.1
         module icu/70.1

     No dependencies found


  For ``trf`` package, theere are dependencies and this all dependent packages
  that will require a rebuilt are listed:

  .. code-block:: bash

     ./trace.py trf
     Provider: biotools-admix
         module trf/4.0.9

     Need to rebuild packages

     biotools-admix:
         repeatmasker_4.1.0
         repeatmasker_4.1.0-module

     genomics-admix:
         kneaddata_0.10.0-module



Graphs
------

Some admixes are more simple, others require complex dependencies. We
have a few  custom scripts that allow us to graphically view the dependencies
among the admixes and the modules that require or provide. 

For example, when ``deplist.yaml`` file is converted to dot format
representation the resulted  directed graphs are :

1. The order graph that shows in what order admixes are to be built due to
   the dependencies among them

   .. image :: images/dot-buildorder.png

2. List of software modules by category shows dependencies among admixes

   .. image :: images/dot-bycategory.png

3. List of software modules by admix showing what modules are required and
   or provided by each

   .. image :: images/dot-byadmix.png
