GCC admix
===========

.. _gcc:

A deeper example
----------------

GCC (the GNU compiler collection) is relatively complex build.  It is often useful to have an updated version of gcc on your 
system without destroying the system-supplied gcc.  The GCC build has to be done in a certain way, packages need to be named
to be non-conflicting and other items.   If you have completed the Quickstart above you can build an updated version of gcc
and a set a packages.

.. warning:: 
  
  This process will install RPMs as it builds. You should do this on a 'disposable' build system. It takes hours to compile a gcc.

Here is the full process for building gcc using the gcc-admix repo

This is block-code console

.. code-block:: console

   git clone https://github.com/RCIC-UCI-Public/gcc-admix.git
   cd gcc-admix
   make download
   cd yamlspecs
   (make bootstrap &> /tmp/bootstrap-gcc.log; make &> /tmp/build-gcc.log) &


This is code-block bash

.. code-block:: bash

   git clone https://github.com/RCIC-UCI-Public/gcc-admix.git
   cd gcc-admix
   make download
   cd yamlspecs
   (make bootstrap &> /tmp/bootstrap-gcc.log; make &> /tmp/build-gcc.log) &

An optional last step would be to *unbootstrap* the system, which will remove any locally-built and installed RPMS that result from
the bootstrap process:

.. code-block:: console

   make unbootstrap

At this point, you should have a compatible set of RPMS for gcc and some key supporting libraries.

The YAML Definition file
------------------------

The basic notion of the definition file to record on the bare minimum needed to define a package. 
Since it is usual for groupings of packages to share some common definitions, the generator supports 
a *defaults* file.  Here is a very simple yaml file taken from the samples directory of the *yaml2rpm* package.


.. code-block:: yaml
   :caption: filename.yaml

   package: iperf version 3 network tester
   name: iperf
   version: "3.6"
   extension: tar.gz
   description: >
       iperf3 version {{ version }}. iperf is a tool for active measurements 
       of the maximum achievable bandwidth on IP networks. It supports tuning
       of various parameters related to timing, protocols, and buffers. For
       For each test it reports the measured throughput/bitrate, loss,
       and other parameters.
   vendor_source: https://downloads.es.net/pub/iperf/iperf-{{ version }}.tar.gz
   root: "{{ pkg_defaults.app_path }}/{{ name }}/{{ version }}"
   build:
       modules:
       target:
   install:
       installextra: $(INSTALL) -m 644  README* LICENSE $(ROOT){{ root }}

