.. _dd_parallel:

Parallelism
===========

Building all admixes is a time-intensive process that can benefit greatly with on-node (SMP) parallelization.
As a baseline, yaml2rpm uses process-based parallelism. Individual packages may themselves use multiple processes
compile more quickly (gcc, is an example). 

:ref:`gen-definitions.py<gen-definitions>` natively uses python's multiprocessing library to process package
yaml files in parallel. This is especially useful when generating manifests for admixes with a very large package
count (e.g., R). 

runparallel
~~~~~~~~~~~

The ``runparallel`` python script can excute multiple processes in parallel while prefixing the standard output of
each process. The admixbuilder git repository contains a script called ``superbuild.sh`` that will clone, build,
and install admixes in a specific order.  It builds the admixes in groups where the admixes in each group
can be built simultaneously. The groups are then in built in order. Superbuild.sh is fast (but not necessarily
optimal).

``runparallel`` is similar to the epel parallel package but is quite a bit smaller - it is NOT intended to replace the 
epel package. Instead it provides just the capability required for parallel building in about 250 lines of python.

superbuild.sh
~~~~~~~~~~~~~

Superbuild is what we use to rebuild everything from scratch. On a 32 core system with NVMe storage a full build
takes about 14 hours. It builds groups of admixes in order. Each individual group builds its defined admixes in 
parallel

   .. code-block:: bash
    
      ./superbuild.sh &> superbuild.out &

For example, the file ``admixgroups/group0`` contains the commands

   .. code-block:: bash

     make ADMIXES=gcc-admix buildall-parallel
     make ADMIXES=buildtools-admix buildall-parallel
     make ADMIXES=cuda-admix buildall-parallel
     make ADMIXES=perl-admix buildall-parallel


This simply says build the gcc-admix, buildtools-admix, cuda-admix, and perl-admix at the same time.
In addition, build everything in each admix in parallel. 

Inspect the contents of the files in admixgroups to see the groupings and overall ordering of a superbuild.


