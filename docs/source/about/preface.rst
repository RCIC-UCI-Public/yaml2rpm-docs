.. _what_is_uaml2rpm:

What is YAML2RPM?
=================

At UCI we run a campus-accessible, shared-use, high-performance computing cluster with hundreds of domain-specific applications.
The applications need to be compiled and installed, often with updated toolchains (prerequisites and dependencies). Users 
regularly require multiple versions to be installed.  

We developed :term:`YAML2RPM` to manage the multiple versions, dependencies, and
other details of a resilient software deployment. YAML-formatted specification files are used to describe how to build an 
application, encode dependencies, and where to install. Through programmatic translation via a custom python program, the 
YAML input generates the ingredients to build a RedHat-compatible RPM using the distribution's native ``rpmbuild`` tool. 

The full process creates human-recognizable package names, supports multiple installed versions, and easily encodes dependencies
for repeatable and robust application stacks.  In a full-stack recompilation, over 2000 individual RPMs are created.

.. admonition:: Motivation

   *YAML2RPM set out to solve part of the problem of building and packaging
   relatively complex software.  At its core, it creates packages in the RPM
   format, but without the pain of manually building  and maintaining spec
   files.*

:term:`YAML2RPM` is a Generic Methodology for building RPMs
This software uses the underlying **Rocks methodology** for automatically creating RPM spec
files to create packages.  Where it differs from Rocks is that a
YAML-based specification of a package is used to define the specific details of a
component, instead of a subdirectory structure for each package 
(see the `rocksclusters github rolls <https://github.com/rocksclusters/>`_ for many examples of the subdirectory structure)

Most (open-source) software starts with a source tarball, extracts the tarball, 
configures for the local environment,  executes ``make`` and then executes ``make install``
In the above, ``make`` might be ``cmake`` or some other software-specific tool. The last step,
to turn the result of the steps, community-standard, process into an installable package
is often deemed too time-consuming or difficult. The advantages of creating a package include:

- File system conflicts resulting from different software builds are flagged prior-to-install
- Software dependency resolution staves off many errors when attempting to remove
  a key software package that other packages depend upon
- Binary packages can be `compiled once` and reused in testing, staging, production environments
- System tools (e.g., ``yum``) can be used a common tool to interrogate the file system for
  integrity, ownership of specific files and other items.

This software relies on only one Rocks-created software package, but otherwise is completely compatible with Generic CentOS and RedHat. 

A developer who wants to build :term:`YAML2RPM`-generated packages must still have some familiarity with RPM concepts and ``yum``. 

Approach
------------

The approach used here is one where programmatic translations are used to progressively create a subdirectory structure that mirrors
the way Rocks builds RPMS (`an example of building a qrencode RPM <https://github.com/rocksclusters/base/blob/master/src/qrencode/>`_).
In that structure, an RPM spec file is automatically created and files are put in appropriate 
places in which `rpmbuild <https://linux.die.net/man/8/rpmbuild/>`_ can success fully build a package.  

The generated spec file must define a source in a ``%source`` as well as ``%build``, ``%install``, ``%file`` 
and other RPM-specific directives.  In particular, the ``%source`` is a tarball of this directory in github
(e.g. base/src/qrencode directory). However, prior to creating the tarball, the upstream tarball 
(e.g. qrencode-3.4.0.tar.bz2) must be placed in base/src/qrencode directory.  The automatically generated spec file,
the ``%build`` directive invokes the ``build`` target of the Makefile provided here. In this example the section looks like:

.. code-block:: make

   build:
	   bunzip2 -c $(NAME)-$(VERSION).$(TARBALL_POSTFIX) | $(TAR) -xf -
	   ( 							\
		cd $(NAME)-$(VERSION);				\
		./configure --prefix=$(PKGROOT); 		\
		$(MAKE);					\
	   )

This build target looks very similar to what you would do if your are building software without placing it into a package.
And that is intentional.  In building literally hundreds of packages, the basic approach works quite well, but it comes
that price of excessive code copying. The goal of the YAML-based generation of a package is to remove as much 
gratuitous `copy-and-paste` structure as possible.  

While the above is very simple (and actually a quite common build motif), there are many variations on how 
something is built, what it is dependent upon, and the like. For example, in real use on
academic computing clusters groupings of software have common dependencies.  A routine example is software that depends 
upon a newer version of `gcc`. The new version of gcc must be installed alongside the system version. 
Often multiple versions of a specific software package are requested.

