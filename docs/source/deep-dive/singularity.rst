.. _dd_container:

Building in a Container
=======================

This section describes using a singularity/apptainer container to perform full/partial builds
of an entire stack. This is especially useful when bringing forward an application stack from one minor
release to another or to a major OS release.

Fundamentally, a complete set of admixes relies on system (Rocky) and EPEL packages. These packages can
change names or behavior from release to release. There is no magic, one just has to sort through the various
issues. It was the iterative nature the catalyzed building inside of a container. 

Essential baseline software components on the "hardware" that hosts containers:
  - ZFS or another file system that supports snapshots 
  - Singularity/Apptainer on a building node 
  - Fuse/Fuse-overlayfs 
  - Git 


ZFS Setup
---------

ZFS is used in these examples to provide the writable *overlay* file system for a build. The singularity
container setup described that follows is a read-only baseline. In practice, if multiple developers are
on the same physical system, each would reference the same baseline container, but have a separate overlay file
system for every build instance. 

Snapshots are very practical when debugging/porting a full build of all admixes from one version of the OS
to another.  As an admix is completed, the snapshot of the *overlay* can be made to save a known, good, partial build state. 
As the next admix is being debugged/ported and inevitable build issues show up, snapshot reversion is a practical and 
simple method to improve developer time efficiency.

The baseline container
----------------------

The `admixbuilder git repository <https://github.com/RCIC-UCI-Public/admixbuilder>`_ has detailed instructions about
how to build the baseline container. See the ``container`` subdirectory.

In addition, there are several useful scripts that can be helpful in streamlining process. This section provides examples
of those scripts that are in use at UCI

Bash environment setup
~~~~~~~~~~~~~~~~~~~~~~

Since development/testing of RPM builds is person intensive, these instructions focus on that aspect.
It's also convenient to be able to have multiple build environments on the same physical machine

The following script could be *sourced* to set all variables for a Rocky 10.1 container built above 
and installed in the referenced container directory. It will setup a ZFS file system if it doesn't already
exist.  That file system is used as an overlay/writable system when the container is started.

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
      if [ ! -d ${HOME}/import ]; then
          echo "${HOME}/import does not exist. Creating"
          mkdir ${HOME}/import
      fi    

Starting the Container
~~~~~~~~~~~~~~~~~~~~~~

A helpful aliases  can be defined to start the container and provide a prompt. 

 .. code-block:: bash

    alias startcontainer='sudo singularity exec
	--bind=/opt/data/opt:/data/opt:ro,/dev/fuse:/dev/fuse,${HOME}/import:/import:ro
	--containall --overlay ${MYOVERLAY} ${BASECONTAINER} /bin/bash -il'

Practical Modifications after first boot
----------------------------------------

If you have followed the above to build and start the container, it's useful to add some files to
to ``${HOME}/import`` directory on the physical system and modify some yum repo definitions.

There are a number of items that we routinely want available when operating withing the container's file
system space. The usual mode is to create, on the physical system, the directory ``${HOME}/import``.
Inspect the alias above, and you will see that the contents of this directory or made available to every container
started. 

Copy/create the following in this ``HOME/import`` directory

1. A ``.gitconfig`` for the container's root user (when a container starts you are a root user), that identifies you
   for git commits. Modify it to reflect the real name and email of the person who might commit changes:

   .. code-block:: bash

      # This is Git's per-user configuration file.
      [user]
      # Please adapt and uncomment the following lines:
      name = Peter the Anteater
      email = panteater@uci.edu

2. The developers private ssh-key (used for committing git changes) as ``id_<username>``.

   .. important:: | NONE of these keys should be added as **Deploy keys** to any admixes repositories.
                  | The deploy keys are not protected by a passphrase and can be a security risk. 

3. A simple, very trivial  shell script that starts ssh-agent. This can be named anything you
   desire, simply source the script each time you start the container.  A name like
   ``getset.sh`` (as in "Ready. Get set. Go") intimates its purpose: set up the container so that
   normal development work can occur. 

   .. code-block:: bash

      #!/bin/bash
      pushd /import
      cp .gitconfig /root
      eval $(ssh-agent)
      for id in id*; do 
          ssh-add $id
      done
      popd

4. An rclone configuration for adding new tarballs

   This is an optional ``rclone.conf`` to add new tarballs (must have write
   privilege on the remote S3 container).

Optional but Recommended
------------------------

On the builder physical system, mirror the appropriate Rocky and EPEL yum repos. Then modify the
``/etc/yum.repos.d/xxx.repo`` definitions to pull from these local mirrors. There are two distinct advantages:

  1. **Reproducibility** - "freezing" these repos at a particular point in time enables finer control for 
     reproducible builds.
  2. **Speed** - the repos are referred to frequently during a complete build.


**Start the Container**

.. tip::
   On every container start, execute ``source /import/getset.sh``. This will prep your shell session to
   enable git push.

Yum repo customization
~~~~~~~~~~~~~~~~~~~~~~

Here is a sample customization of ``/etc/yum.repos.d/rocky.repo`` (only the changed sections are included and 
are from the Rocky 10 version). The *mirrolist* url is commented out and the *baseurl* is copied, uncommented,
and then edited to look to the local host.

If any urls reference ``https``, change them to ``http``. The ``epel.repo`` file uses https.

   .. code-block:: bash

       [baseos]
       name=Rocky Linux $releasever - BaseOS
       #mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=BaseOS-$releasever$rltype
       #baseurl=http://dl.rockylinux.org/$contentdir/$releasever/BaseOS/$basearch/os/
       baseurl=http://127.0.0.1/$contentdir/$releasever/BaseOS/$basearch/os/
       gpgcheck=1
       enabled=1
       countme=1
       metadata_expire=6h
       gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-Rocky-10
       
       [appstream]
       name=Rocky Linux $releasever - AppStream
       #mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=AppStream-$releasever$rltype
       #baseurl=http://dl.rockylinux.org/$contentdir/$releasever/AppStream/$basearch/os/
       baseurl=http://127.0.0.1/$contentdir/$releasever/AppStream/$basearch/os/
       gpgcheck=1
       enabled=1
       countme=1
       metadata_expire=6h
       gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-Rocky-10
       
       [crb]
       name=Rocky Linux $releasever - CRB
       #mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=CRB-$releasever$rltype
       #baseurl=http://dl.rockylinux.org/$contentdir/$releasever/CRB/$basearch/os/
       baseurl=http://127.0.0.1/$contentdir/$releasever/CRB/$basearch/os/
       gpgcheck=1
       enabled=1
       countme=1
       metadata_expire=6h
       gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-Rocky-10

.. note::

   For Rocky 9/10 customize ``rocky.repo`` and ``epel.repo``.  For Rocky 10, also customize
   ``rocky-extras.repo``.  This assumes that you have mirrored the repos on the physical host and it will 
   serve the URLs properly.
  
Baseline snapshot
-----------------

When you have completed the customizations, exit from the container and
on a physical host take a ZFS snapshot as a new baseline that represents
the **container baseline + customizations**.
Do this prior to adding  and building yaml2rpm.

Build yaml2rpm
--------------

Follow the :ref:`Quickstart<quickstart>` instructions to build yaml2rpm. Then create another snapshot of 
your build environment.  

At this point, you have a generic environment that can then be used to build
the entire collection of admixes and associated applications.
