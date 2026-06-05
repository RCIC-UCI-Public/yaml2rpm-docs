.. _admixbuilder:

admixbuilder
============

**Table of contents:**

.. contents::
   :local:

Building
--------

High-level builder for UCI Admix collection.

There are no RPMS build in this admix, it is used for keeping track of 
what is available for a build in other admixes 
and what are relationships among different admixes.

This admix provides a collection of *convenience* info plus checks and balances
for build outcomes in other admixes.
The prerequisites are easily satisfied via stock RPMs: 

**Prerequisites**
  | :tt:`python` - to use with a few custom scripts, should be already installed on your development host.
  | :tt:`graphviz`- to create graphical representation of collected information.
    If not already present can be added via:

    .. parsed-literal::
       :command:`yum install graphviz`

Files
-----

``CHANGELOG.md``
  A standard change log  file that is generated via running :command:`auto-changelog` 
  command (provided by the  nodejs RPM).

``Makefile``
  Targets in this file provides useful commands that can be run for all other
  admixes such as check out admixes git repositories, download sources for the admixes builds,
  make build  for each one and, etc. A few targets create graphs and PDF files.

``README.md``
  Minimal info file about this admix.

``admixgroups/``
  A directory containing files that define
  groups of admixes to be built in order. Used by :ref:`superbuild`.
  Each individual group builds its defined admixes in parallel.
  Currently, we define 7 groups ``group0`` through ``group6``.

``buildorder``
  An ASCII text file that specifies an order in which admixes should be built serially.
  This file is a result of many builds and resolving dependencies. 
  This is a *partial order* ordering: some admixes require to use RPMS that are built in some other
  admixes, and some admixes have no relationship.

``checkRpms``
  Check built RPMS against a known good size. Report discrepancies.
  To run for an individual admix provide admix name as an argument, for example:

  .. parsed-literal::
     :command:`./checkRpms gcc-admix`

``container/``
  Contains info on setting up For Singularity-based builds.

``fcheck.sh`` (optional)
  A legacy simple shell script that can be used after running :command:`superbuild.sh`. 
  It will use build log files to compare number of RPMS made vs. number of RPM installed
  This is a very first approximation as the numbers can be different but still correct.

``getTimes`` (optional)
  Parse log files to get admix build time (in minutes).
  Prints admix name and its build time in minutes. Need to have all admixes
  build log files (from running :command:`superbuild.sh`).

``makeDotFiles`` (optional)
  Create *dot* format  files for building dot graph.

``notes/``
  A bookkeeping info, notes of software that won't install on Rocky 10, versions that
  need changing, and removals, etc.  Catalog SOME of the effects of these changes.

``pdfs/`` (optional)
  PDF representation of *dot* files. 

``plotHist`` (optional)
  Parse log files info (extracted from build logs) to get packages build time (in minutes)
  (input files contain lines with 'Building' and 'Completed' lines for each package).
  Use results to make histogram plots, save plots as ``histogram.png``.
  Mainly give idea of how long packages take to build and what the
  distribution of time is.

``prep.sh`` (optional)
  A legacy script for basic system prep for Rocky 8/9.
  No longer needed when running on a container.

``superbuild.sh``
  See :ref:`superbuild`.

``trace.py`` (optional)
  Python script that takes as an input a  dependencies info file (default ``depinfo.yaml``)
  and a given package name and  prints  a list of all packages by admix that depend on this package.

  This tool provides an answer to the question:
    `If i change package X version Y  what other packages do i need to rebuild?`

  For example, for a packages ``icu`` it shows  that no other packages will need
  to be  rebuilt if this package is recompiled:

    .. parsed-literal:: 
       :command:`./trace.py icu`
       Provider: buildtools-admix
           module icu/65.1
           module icu/70.1

       No dependencies found

  For ``trf`` package, there are dependencies listed that will require a rebuilt:

    .. parsed-literal:: 
       :command:`./trace.py trf`
       Provider: biotools-admix
           module trf/4.0.9

       Need to rebuild packages

       biotools-admix:
           repeatmasker_4.1.0
           repeatmasker_4.1.0-module

       genomics-admix:
           kneaddata_0.10.0-module

``depinfo.yaml``
  This file is generated via a target in ``Makefile``.
  This is a dependency tree among all the packages, showing 
  requires, provides, category for all build packages in all admixes.
  Used by ``trace.py`` when tracing packages dependencies.
  The generated file format is (per module):

  .. code-block:: yaml
  
     macs_2.2.7.1-module:
       admix: biotools-admix
       set: versions
       version: 2.2.7.1
       category: BIOTOOLS
       requires:
         - python/3.8.0
       provides:
         - macs/2.2.7.1

Makefile targets
----------------

Some ``Makefile`` targets are essential, others  wee created at different
times for convenience or a specific presentations (dot graphs).
Log files referenced below are from :command:`superbuild.sh` run.

:bluelight:`Essential targets`

admixdb
  Create ``.rpm.ADMIXNAME.OS`` file in each admix top directory. 
  The *ADMIXNAME* is the admix repo top directory name, and the *OS* 
  is the current OS version.
  Each admix can have a few  such RPM database files, one per OS.
  Once the build in the admix is verified  these files need to be added to the git repo.

ansible
  For each admix creates an ansible file that contains all the RPMS created
  for the install.  At RCIC we use these files for ansible playbooks when
  updating and isntallgin software RPMS.

check
  Checks admix built RPMS against what is known in admix RPM database file
  ``.rpm.ADMIXNAME.OS``. The command picks correct database file for the
  current OS.

clone
  Clone all the admixes repositories.

download
  Download all the software packages source distribution files for all
  admixes.

swtable
  Creates ``sw.csv`` file that contains all the created RPMS in all the
  admixes. This is used in the website documentation. Minor edits are needed
  for some entries (to shorten description field which is the last column).

:bluelight:`Convenience targets`

clean
  Removes previously created ``depinfo.yaml`` so that can execute next target
  below.

depinfo.yaml
  Create named file from  the output of running specific targets in each admix.
  The file is used for creation of *dot* files.

diag
  Diagnostic output of List of admixes to work on.

dot
  Parse ``depinfo.yaml`` and create *dot* files.

dotpdf
  Create *pdf* files form *dot* files.

dotpng
  Create *png* files form *dot* files.

histogram
  Parse all builds log files, get building times for each package 
  into ``allpkgs`` file and create a histogram ``histogram.pong``.

rpmcopy
  Unused, left for a reference.

targets
  List ``Makefile`` targets.

time
  Prints how long in minutes it took to build the admixes.
  Need to have all build logs files from :command:`superbuild.sh` to be
  complete.

.. _graphs:

Graphs
------

Some admixes are simple, others require complex dependencies. We
have a few custom legacy scripts that allow us to graphically view the dependencies
among the admixes and the modules that require or provide. 
These are optional.

For example, when ``depinfo.yaml`` file is converted to dot format:

  .. parsed-literal::
     :command:`make depinfo.yaml
     make dot
     make dotpng
     maake dotpdf`

the resulted  directed graphs are created in *dot*, *png*, and *pdf* format and are:

  1. The order graph ``dot-buildorder`` that shows in what order admixes are to be built due to
     the dependencies among them

     .. image :: images/dot-buildorder.png

  #. List of software modules by category ``dot-bycategory`` shows dependencies among admixes

     .. image :: images/dot-bycategory.png

  #. List of software modules by admix ``dot-byadmix`` showing what modules are required and
     or provided by each
  
     .. image :: images/dot-byadmix.png
