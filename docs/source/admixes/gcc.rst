.. _gcc-admix:

gcc-admix
=========

**Table of contents:**

.. contents::
   :local:

Building
--------

The `gcc-admix repository <https://github.com/RCIC-UCI-Public/gcc-admix/>`_ is used to build multiple versions of GCC,
environment module file for them, and some compatible libraries.  Those packages can then be installed
and used to build other software.

GCC (the GNU compiler collection) is relatively complex build.  It is often useful to have an updated version of gcc on your 
system without destroying the system-supplied gcc. The GCC build has to be done in a certain way, packages need to be named
to be non-conflicting and other items. If you have completed the Quickstart you can build an updated version of gcc
and its related set of packages.

Here is the full process for building GCC and associated modules present in the repo:

  .. parsed-literal::
     :command:`git clone https://github.com/RCIC-UCI-Public/gcc-admix.git
     cd gcc-admix/
     make download
     make buildall-parallel &> buildall.log &`

After the build ends, you should have a compatible set of RPMS for gcc and some key supporting libraries.

.. warning::
     This process will install RPMs as it builds. You should do 
     this on a 'disposable' build system. It takes hours to compile a gcc.

The following sections provide detailed explanation about repo files,
build process, and adding new modules step-by-step.

Files description
-----------------

See the :ref:`introduction <admixrepo_general>`.


Build details
-------------

See the :ref:`introduction <admixrepo_general>`.
