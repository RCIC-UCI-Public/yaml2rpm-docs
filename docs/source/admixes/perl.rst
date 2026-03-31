Perl
=====

.. _perl-admix:

The `perl-admix repository <https://github.com/RCIC-UCI-Public/perl-admix/>`_ uses **YAML2RPM** to build 
multiple versions of perl. 

Perl is relatively complex build and requires local changes to its Makefile to
accomplish multiple builds.

.. warning:: 
  
  This process will install RPMs as it builds. You should do this on a 'disposable' build system.

Here is the full process for building perl using the  `perl-admix repository
<https://github.com/RCIC-UCI-Public/perl-admix/>`_

.. code-block:: bash

   git clone https://github.com/RCIC-UCI-Public/perl-admix.git
   cd R4-admix
   make download
   cd yamlspecs
   (make bootstrap &> /tmp/bootstrap-gcc.log; make &> /tmp/build-gcc.log) &

Build details
-------------

TODO
