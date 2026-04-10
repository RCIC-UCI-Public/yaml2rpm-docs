.. _packaging:

Packaging
=========

This section is a deep dive into packaging. It's presented so that when things "go wrong", one has a fighting chance
to understand and unwind the process of how a package is made. A ``<pkg>.yaml`` file in the ``yamlspecs`` 
subdirectory of an admix is a very terse listing of what makes a particular package. Its contents revolve around:

  1. The name of the package
  2. The description of the package
  3. The source tarball of the package
  4. How to build it
  5. (Optional) directives to rpmbuild to successfully create the rpm version of the software

With a large number of packages, common build patterns emerge. For example, many software sources follow
the pattern

  * ./configure <configure arguments>
  * make
  * make install

A ``<pkg>.yaml`` for software that follows this pattern needs only specify the configure arguments, name, name of
source tarball for code and directory for final installation.

.. tip::
   Yaml2rpm uses several "transformations" to create a directory infrastucture and rpm spec file so that ``rpmbuild`` 
   can successfully create the final rpm package

The next sections provide some detail of the transformations and how the build process shows up on the file system.

.. _building rpm:

RPM Background
--------------

`RPM.org <https://rpm.org/docs/4.20.x/man/rpmbuild.8.html>`_ has extensive documentation the entire rpm 
building process, how to create spec files, how to handle various issues, and other, sometimes arcane, 
aspects of creating software packages.  

A package build is driven by `spec <https://rpm.org/docs/4.20.x/manual/spec.html>`_ file that defines 
everything.  The spec file contained in the source RPM for 
`gcc for EL9 <https://dl.rockylinux.org/pub/rocky/9.7/BaseOS/source/tree/Packages/g/gcc-11.5.0-11.el9.src.rpm>`_, 
is more than 4600 lines. While that spec file creates multiple binary RPMs, 
it is very complex.   Yaml2rpm seeks to dramatically reduce this kind of complexity and remove 
the direct authoring and maintenance of spec files.

Building an RPM is performed with `rpmbuild <https://www.man7.org/linux/man-pages/man8/rpmbuild.8.html>`_ with files 
in a specific file system hierarchy

.. _rpm-directory-structure:

.. image:: /images/RPM-Directory-Structure.png
      :align: center
      :alt: Directory Structure for building an RPM binary package

In the image above, all source code and patches are placed in the ``SOURCES`` directory. The instructions for building the binary RPM is placed in the ``SPECS`` directory.  The ``~/.rpmmacros`` file is interpreted so that 
this RPM directory structure can be anywhere desired. The *output* (binary RPM) is placed in the RPMS directory.

.. tip::
   Each admix has the entire RPM directory structure localized to its tree.  This entire structure is generated as 
   part of the build process and is *output*. Nothing in this RPM tree should ever be committed to a source 
   code repository. 

The yaml2rpm build process *must* create this tree and appropriately place files there so that ``rpmbuild`` can
perform its task. 


Rocks-devel RPM Process
-----------------------

The authors of the `Rocks Cluster Toolkit <https://www.rocksclusters.org>`_ recognized that managing spec files at scale
is a daunting task and did not scale well for a development group of 2-3 people. Using a Makefile infrastructure with
a common (and extensive) set of rules, the definition of a single RPM package was reduced to a single directory.
From that directory, the RPM directory structure needed by ``rpmbuild`` was generated and ``rpmbuild`` was then used
to create the binary package.  That directory structure did *not* have an RPM spec file. Instead, the make-driven
process generated a specfile and used the ``build:`` and ``install:`` targets defined in the directory.

This had the distinct advantage where building a software package mostly focused on the specific compilation
requirements instead of the arcane aspects of spec files.  The binary RPM was a byproduct. 
This allowed the Rocks developers to create 100s of packages.


