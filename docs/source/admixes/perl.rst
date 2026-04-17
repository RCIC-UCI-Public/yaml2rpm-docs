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

