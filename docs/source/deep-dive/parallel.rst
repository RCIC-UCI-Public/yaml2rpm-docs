.. _parallel:

Parallelism
===========

Building all admixes is a time-intensive process that can benefit greatly with on-node (SMP) parallelization.
As a baseline, yaml2rpm uses process-based parallelism. Individual packages may themselves use multiple processes
compile more quickly (gcc, is an example). 

The :ref:`gen-definitions.py<gen-definitions>` natively uses Python's multiprocessing library to process package
yaml files in parallel. This is especially useful when generating manifests for admixes with a very large package
count (e.g., R). 

.. _runparallel:

runparallel
~~~~~~~~~~~

The ``runparallel`` Python script can execute multiple processes in parallel while prefixing the standard output of
each process. The *admixbuilder* git repository contains a script called ``superbuild.sh`` that will clone, build,
and install admixes in a specific order.  It builds the admixes in groups where the admixes in each group
can be built simultaneously. The groups are then in built in order.  The ``superbuild.sh`` is fast but not necessarily
optimal.

The ``runparallel`` is similar to the EPEL *parallel* software package but is quite a bit smaller - it is NOT intended to replace the 
EPEL package. Instead it provides just the capability required for parallel building in about 250 lines of Python.


.. _superbuild:

superbuild.sh
~~~~~~~~~~~~~

This is what we use to build or rebuild everything from scratch. On a 32 core system with NVMe storage a full build
takes about 14 hours. It builds groups of admixes in order. Each individual group builds its defined admixes in 
parallel. At the top level of *admixbuilder* repository checkout execute:

   .. parsed-literal::
      :command:`./superbuild.sh &> superbuild.out &`

The ``suoeprbuild.sh`` calls ``runparallel`` to run builds in parallel for a
specific set of admixes defined in ``admixgroups/group\*`` files. 

For example, the file ``admixgroups/group0`` contains the commands

   .. parsed-literal::
      :command:`make ADMIXES=gcc-admix buildall-parallel`
      :command:`make ADMIXES=buildtools-admix buildall-parallel`
      :command:`make ADMIXES=cuda-admix buildall-parallel`
      :command:`make ADMIXES=perl-admix buildall-parallel`

This simply says build the *gcc-admix*, *buildtools-admix*, *cuda-admix*, and *perl-admix* at the same time.
In addition, build everything in each admix in parallel. 

The files define groups and their order of build and are specific.
We define 7 such groups ``group0`` through ``group6``.
The admixes in the first group ``group0`` have to be build first, then the next group ``group1`` will start
building and so on. The defined  grouping and their order  are established via
packages dependencies. 

Inspect the contents of the files in ``admixgroups/`` to see the groupings and overall ordering of a superbuild.

