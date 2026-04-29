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


ZFS Setup
---------

ZFS is used in these examples to provide the writable *overlay* file system for a build. The singularity
container setup described that follows is a read-only baseline. In practice, if multiple developers are
on the same physical system, each would reference the same baseline container, but have a separate overlay file
system for every build instance. 

Snapshots are very practical when debugging/porting a full build of all admixes from one version of the OS
to another.  As an admix is completed, the *overlay* can be snapshotted to save a known, good, partial build state. 
As the next admix is being debugged/ported and inevitable build issues show up, snapshot reversion is a practical and 
simple method to improve developer time efficiency.

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


Practical Modifications after first boot
----------------------------------------

If you have followed the above to build and start the container. There are a number of items that we routinely add
(show up in the overlay) and then take a snapshot as "baseline" for a particular build.

* Developer's private ssh key for committing changes to git
* A .gitconfig for the root user
* An rclone configuration for adding new tarballs
* A simple, simple shell script that starts ssh-agent

Using ``/export/repositories`` as the directory, it's useful to copy in the following files

1. A modified .gitconfig that reflects the name of the person who might commit changes
   .. code-block:: bash

   # This is Git's per-user configuration file.
   [user]
   # Please adapt and uncomment the following lines:
   name = Peter the Anteater
   email = panteater@uci.edu

2. The developers private ssh-key (used for committing git changes) as `id_<username>`

3. The following very trivial shell script
   .. code-block:: bash

   #!/bin/bash
   pushd /export/repositories
   cp .gitconfig /root
   eval $(ssh-agent)
   ssh-add id*
   popd

4. (Optional) rclone.conf to add new tarballs (must have write priv on the remote S3 container)


Optional but Recommended
------------------------

One the builder physical system, mirror the appropriate Rocky and EPEL yum repos. Then modify the
``/etc/yum.repos.d/xxx.repo`` definitions to pull from these local mirrors. There are two distinct advantages:

  1. Reproducibility. "Freezing" these repos at a particular point in time enables finer control for 
     reproducible builds.
  2. Speed. The repos are referred to frequently during a complete build


.. note::

   When you have completed this above customizations. Take a ZFS snapshot as new baseline that represents
   the container baseline + these customizations. Do this prior to adding the yaml2rpm building infrastucture.

