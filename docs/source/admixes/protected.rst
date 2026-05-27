.. _protected_admix:

protected-admix
===============

**Table of contents:**

.. contents::
   :local:

Building
--------

The `protected-admix repository <https://github.com/RCIC-UCI-Public/protected-admix/>`_
is used to build multiple versions of VASP, Rosetta and QE.

.. warning::
   There are limitations how each can be distributed and used:

   - Rosetta and EQ source distributions are protected (brought by PIs who paid for it).
   - VASP source distribution and resulting binaries are protected. The sources
     are available to PIs who bought the licences and the resulting binaries can
     only be available to these PI's groups. See :ref:`protected_install` for details.

Hence we can not put in a public storage any of the sources.  This means:

  1. In the repo the source metadata file  ``.protected-admix.metadata`` file is empty
     to make sure :command:`make download` does nothing.
  #. We keep as a reference the sizes for the above distribution sources 
     in a separate file that is not used in any of the make targets: ``.protected-admix.metadata.info``
  #. The files are kept in a specific CRSP location and must be downloaded
     by authorized people into ``sources`` via :command:`sftp` prior to the  building in this admix.

     .. parsed-literal::
        :command:`mkdir sources/`
        sftp files listed in ``.protected-admix.metadata.info`` to ``sources/``
        check their sizes with
        :command:`sha1sum sources/\*`

Once have the sources, the build process is the same as for any admix:

  .. parsed-literal::
     :command:`git clone https://github.com/RCIC-UCI-Public/perl-admix.git
     cd perl-admix
     make buildall-parallel &> buildall.log &`


The following sections provide detailed explanation about repo files,
build process, and adding new modules step-by-step.

Files description
-----------------

At the top level
~~~~~~~~~~~~~~~~~~~~~~

Standard files and directories present in every admix as described in
:ref:`admix top level files <admix_top_level>`.
Exception is ``.protected-admix.metadata.info`` described above.

In yamlspecs/
~~~~~~~~~~~~~

Standard files
^^^^^^^^^^^^^^

We build a few sets in this admix as we have to build a few different versions
of VASP.

When building Perl modules we not only need to build different versions of
Perl itself but also need to have different modules that were requested by the users
in order to support different types of applications.


``packages.yaml``
  Yaml format, describes specifics of this admix build.
  The *build* target is intentionally empty, and there is no *bootstrap*.
  All work is done in sets.
  All variables in this file are :ref:`standard <packages_yaml>`.

``versions.yaml``
  Defines variables for Rosetta and QE packages the *base* set
  and the admix name.

``Makefile``
  Standard file.

``rosetta.yaml``
  This yaml file provides all the instructions to build *Rosetta* RPM.

``rosetta-module.yaml``
  Describes how to build environment module for Rosetta. 

``qe-7.1.patch``
  A patch file to apply when building QE version 7.1.

``qe.yaml``
  For building Quantum Espresso (QE) RPM.

``qe-module.yaml``
  This file describes an environment module build for QE.

``qe-cuda.yaml``
  For building cuda-enabled Quantum Espresso (QE) RPM.

``qe-cuda-module.yaml``
  This file describes an environment module build for cuda-enabled QE.

``vasp<X>.yaml``
  For building specific VAPS version. The ``X`` stands for a shorthand
  version notation.

``vasp<X>-module.yaml``
  This file describes an environment module build for VASP (For a specific version X).
  
``vasp<X>-\*.patch``
  Various patches for respective VASP versions.

Set specific
^^^^^^^^^^^^

The set files and corresponding versions files enable us to create multiple
versions of desired modules for multiple versions of VASP.

Here, we have two versions of Perl and 3 groups, plus the *base* set for each
version.  This results in the following matrix of sets and their corresponding
versions:

  .. table::
     :class: noscroll-table

     +---------+-------------------+------------------------+
     | VASP    | Set               |  Versions              |
     | version | file              |  file                  |
     +---------+-------------------+------------------------+
     | 5.4.4   | set-vasp5.yaml    | versions-vasp5.yaml    |
     +---------+-------------------+------------------------+
     | 6.1.2   | set-vasp6.yaml    | versions-vasp6.yaml    |
     +---------+-------------------+------------------------+
     | 6.3.2   | set-vasp63.yaml   | versions-vasp63.yaml   |
     +---------+-------------------+------------------------+

Any individual set can be built separately, for example:

   .. parsed-literal::
      :command:`make bootstrap SET=vasp6`

Scripts
^^^^^^^

There are a few scripts that we created to enable filtering of requires 
from the resulting RPMS. 

``filter-requires-qe.sh``
  This bash script is used to create filters for rewriting QE RPMs *requires*.
  In order to use it  the following is added to the ``qe.yaml``:

    .. code-block:: yaml
       addfile:
          - filter-requires-{{name}}.sh

       rpmFilters: \*filterRequires

  The :yvars:`addfile` defines what file to add  when processing sources for
  this package. The :yvars:`rpmFilters` tells to use this file when creating
  RPM specs.

``filter-requires-vasp63-cuda.sh``
  This script is used to create filters for rewriting *requires* for
  cuda-enabled VASP version 6.3.2.
  The handling of the requires filter is similar to one above. See details
  in the repo file.

.. _protected_install:

Installing
----------

The Rosetta and QE RPMs are installed as usual.

.. important::
   We do not install VASP RPMs on the cluster due to the software licensing
   restrictions where the binaries should be availalbe only to the groups who
   paid for the software.  Only VASP module RPMS are installed on the cluster.

The package yaml files  for VASP provide a convenient way to build RPMs
without hand interaction. Once they are built we can extract the binaries from
each RPM and install them on the cluster in a designated location ``/data/opt/apps/vasp`` and change group
ownership:

  - for vasp/5.4.4 group *vasp5*
  - for vasp/6.1.2 group *vasp6*
  - for vasp/6.3.2 group *vasp63*

The extraction is  done with cpio commands, for example, for VASP 5.4.4 RPM
from the top level of admix:

   .. parsed-literal::
      :command:`rpm -qlp RPMS/x86_64/vasp_5.4.4_gcc_6.5.0-5.4.4-1.x86_64.rpm`
      /opt/apps/vasp
      /opt/apps/vasp/5.4.4
      /opt/apps/vasp/5.4.4/bin
      /opt/apps/vasp/5.4.4/bin/vasp_gam
      /opt/apps/vasp/5.4.4/bin/vasp_ncl
      /opt/apps/vasp/5.4.4/bin/vasp_std
      :command:`rpm2cpio RPMS/x86_64/vasp_5.4.4_gcc_6.5.0-5.4.4-1.x86_64.rpm | cpio -idmv`

The last command will result in creating in the current directory ``opt/apps/vasp/5.4.4/``
with needed binaries under it.  Transfer the contents  of ``5.4.4/bin`` to
``/data/opt/apps/vasp`` and change group ownership accordingly.
