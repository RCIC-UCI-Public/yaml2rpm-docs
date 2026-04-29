.. _dd_container:

Building in a Container
=======================

This section describes using a singularity/apptainer container to perform full/partial builds
of an entire stack. This is especially useful when bringing forward an application stack from one minor
release to another or to a major OS release.

Fundamentally, a complete set of admixes relies on system (Rocky) and EPEL packages. These packages can
change names or behaviour from release to release. There is no magic, one just has to sort through the various
issues. It was the interative nature the catalyzed building inside of a container. 

Essential baseline software components on the "hardware" that hosts containers

  1. ZFS or another file system that supports snapshots 
  2. Singularity/Apptainer on a building node 
  3. Fuse/Fuse-overlayfs 
  4. Git 


The baseline container
----------------------

The `admixbuilder git repository <https://github.com/RCIC-UCI-Public/admixbuilder>`_ has detailed instructions about
how to build the baseline container. See the ``container`` subdirectory.

In addition, there are several useful scripts that can be helpful in streamling process. This section provides examples
of those scripts that are in use at UCI

Bash environment setup
~~~~~~~~~~~~~~~~~~~~~~

Since developement/testing of RPM builds is person intensive, these instructions focus on that aspect.
It's also convenient to be able to have multiple build environments on the same physical machine

The following script could be *sourced* to set all variables for a Rocky 10.1 container built above 
and installed in the referenced container directory. It will setup a ZFS file system if it doesn't already
exist.  That file system is used as an overlay/writable system when the container is started 


  .. code-block:: bash

      ## RELEASE 10.1
      export RELEASE=10.1
      export CONTAINERRELEASE=10.1
      export CONTAINERS=/opt/singularity/containers
      export NVME=nvme6
      export MYOVERLAY="/disks/${NVME}/builders/${USER}/basebuild-${RELEASE}"
      export BASECONTAINER=${CONTAINERS}/admixbuilder-${CONTAINERRELEASE}.sif

      export ZFSSLICE=$(echo $MYOVERLAY | sed 's#/disks/##')
      zfs list $ZFSSLICE &> /dev/null
      if [ $? -ne 0 ]; then
          echo "ZFS overlay filesystem $ZFSSLICE does not exist. Creating"
          sudo zfs create $ZFSSLICE
      fi


Starting the Container
~~~~~~~~~~~~~~~~~~~~~~

A helpful aliases  can be defined to start the container and provide a prompt. 

 .. code-block:: bash

      alias startcontainer='sudo singularity exec --bind=/opt/data/opt:/data/opt:ro,/dev/fuse:/dev/fuse --containall --overlay ${MYOVERLAY} ${BASECONTAINER} /bin/bash -il'
