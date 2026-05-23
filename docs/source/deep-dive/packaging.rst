.. _dd_packaging:

Packaging
=========

This section is a deep dive into packaging. It's presented so that when things "go wrong", one has a fighting chance
to understand and unwind btibb process of how a package is made. A ``<pkg>.yaml`` file in the ``yamlspecs`` 
subdirectory of an admix is a very terse listing of what makes a particular package. Its contents revolve around:

  1. The name of the package
  2. The description of the package
  3. The source tarball of the package
  4. How to build it
  5. (Optional) directives to |rpmb| to successfully create the rpm version of the software

With a large number of packages, common build patterns emerge. For example, many software sources follow
the pattern

  * ./configure <configure arguments>
  * make
  * make install

A ``<pkg>.yaml`` for software that follows this pattern needs only specify the configure arguments, name, name of
source tarball for code and directory for final installation.

.. tip::
   Yaml2rpm uses several "transformations" to create a directory infrastructure and rpm spec file so that |rpmb|
   can successfully create the final rpm package

The next sections provide some detail of the transformations and how the build process shows up on the file system.

.. _dd_building_rpms:

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

.. _dd_rpmdirs:

.. figure:: /images/RPM-Directory-Structure.png
      :align: center
      :alt: Directory Structure for building an RPM binary package

      The Directory structure **required** by an interpreted by |rpmb| to create an RPM.

In :numref:`dd_rpmdirs`,` all source code and patches are placed in the ``SOURCES`` directory. 
The instructions for building the binary RPM is placed in the ``SPECS`` directory.  
The ``~/.rpmmacros`` file is interpreted so that 
this RPM directory structure can be anywhere desired. The *output* (binary RPM) is placed in the RPMS directory.

.. tip::
   Each admix has the entire RPM directory structure localized to its tree.  This entire structure is generated as 
   part of the build process and is *output*. Nothing in this RPM tree should ever be committed to a source 
   code repository. 

The yaml2rpm build process *must* create this tree and appropriately place files there so that |rpmb| can
perform its task. 


Rocks-devel RPM Process
-----------------------

The authors of the `Rocks Cluster Toolkit <https://www.rocksclusters.org>`_ recognized that managing spec files at scale
is a daunting task and did not scale well for a small development group of 2-3 people. 
Using a Makefile infrastructure with
a common (and extensive) set of rules, the definition of a single RPM package was reduced to a single directory.

From this structure, the RPM directory structure needed by |rpmb| is generated and |rpmb| is then used
to create the binary package.  This rocks-devel directory structure does *not* contain an RPM spec file. 
Instead, the make-driven process generates a specfile. That specfile invokes the ``build:`` and ``install:`` 
targets defined in the per-package Makefile.  Any specific instructions (e.g., ``./configure``, ``python setup.py``,
``R CMD INSTALL``, ...) to compile/install a piece of software are encoded directly into the Makefile. 

This has the distinct advantage where building a software package mostly focuses on the specific compilation
requirements instead of the arcane aspects of spec files.  The binary RPM is a *byproduct*. 
This allowed the Rocks developers to create 100s of packages.


.. _dd_rocks_devel:

.. figure:: /images/rocks-devel-processing.png
      :align: center
      :alt: Directory Structure for a rocks-devel compatible package

      The essential files in a directory that can be transformed by the rocks-devel Makefile infrastructure 
      to build an RPM.

:numref:`dd_rocks_devel` illustrates the high-level view and directory structure for creating an RPM using rocks-devel.
The Makefile references/includes files defined in ``$(ROCKSROOT)``.  That variable is defined by 
``/etc/profile.d/rocks-devel.sh``, which is part of the ``rocks-devel`` rpm. 

There are some key items to note here
   
    1. There is no *spec* file. The specfile is *generated*. The resulting spec file 
       is placed in the ``SPECS`` directory
    2. The entire directory is tarred and becomes the source for the generated spec file. That tar.gz file 
       is places in the ``SOURCES`` directory for |rpmb| to use
    3. Since the entire directory is tarred as the source, it can include patch files, filter files, or other items
       specific to a particular package
    4. Files like ``Defaults.mk``, ``Definitions.mk`` are interpreted by the rocks-devel Makefile structure

*Are there drawbacks to this approach?*

Yes, there are some tradeoffs. 

  * The resulting, generated, SRPM (Source RPM) is not portable. The full path of
    the BUILD directory and the rocks-devel directory are encoded in the  SRPM.  
  * For large tarballs supplied (100+MB) by the initial software "vendor", additional space (and time) is used
    to make the SOURCES-compatible tarball


Yaml2rpm Process
----------------

The yaml2rpm process was motivated by some observations when attempting to manage a production cluster that serves
multiple departments at a research university.

   * Multiple versions of the same basic software (e.g., gcc, python, ncbiblast, ...) need to co-exist in the same 
     system
   * Administrator-managed NFS software areas (e.g. hand-compiled) often have "broken" software trees because
     dependencies are inadvertently changed (or removed).  NFS software areas are a potential performance
     bottleneck for large clusters.
   * The rocks-devel process build individual packages, but when two versions of the same software are required then
     two subdirectories with nearly identical entries are required. The multiversion case was often just a single
     version number change + source tarball.
   * A particular application can have multiple dependencies. Without a naming convention, these are quite difficult to
     encode
   * Common build *memes* resulted in significant duplication of "Makefile code"
   * An order of magnitude in the number of packages required for a campus-community cluster vs. a lab-cluster (the 
     Rocks targeted use case), made the rocks-devel process cumbersome

.. tip::
   The yaml2rpm process creates a temporary rocks-devel-compatible directory and then invokes the rocks-devel process
   to to build the RPM


.. _dd_yaml2rpm:

.. figure:: /images/yaml2pm-for-a-single-pkg.png
      :align: center
      :alt: Transformations for yaml2rpm to rocks-devel to rpmbuild
      
      Yaml2rpm transformations from package.yaml file and source tarball to completed RPM 

:numref:`dd_yaml2rpm` illustrates the major steps/transformations that occur to go from yaml-formatted package
file + source tarball to RPM.

.. |rpmb| replace:: :command:`rpmbuild`

Key Makefiles
-------------

There are several generic/templated Makefiles that have different functions

.. _dd_makefiles:

  1. `Software Compilation <https://raw.githubusercontent.com/RCIC-UCI-Public/yaml2rpm/refs/heads/master/yamlspecs/builder/Makefile>`_  (yaml2rpm)
  2. `Spec File Generation <https://raw.githubusercontent.com/RCIC-UCI-Public/yaml2rpm/refs/heads/master/core-tiny/src/devel/devel/etc/Rules-linux-centos.mk>`_ (rocks-devel)
  3. `yamlspecs Makefile <https://raw.githubusercontent.com/RCIC-UCI-Public/yaml2rpm/refs/heads/master/yamlspecs/Makefile>`_ (yamlrpm)

.. note::
   * These are listed in the reverse order in which they are called when building a package. 
   * They are listed in order of what a package developer really needs to know.

Indeed, item 1 above is the most important as this is where the compilation and installation of software occurs.
This is where the specifics of  "how to build a particular" piece of software defined in the yamlfile is 
ultimately executed.

The following are the key build and install snippets from the Software Compilation makefile

.. parsed-literal::

    # Usual build case:
    #        The SRC tarball (which is most often the downloaded tar source, unchanged)
    #        1. unpack the tarball
    #        2. change into the source directory then
    #             a. apply patches
    #             b. apply any changes prior to configure step
    #             c. configure the package
    #             d. build the software
    # Unusual build case:
    #        1. There is no src tarball (often just some files that need installing and packaging)
    #        2. Same as above (but definitions should override steps)
    :blue:`build:`
    	- $(CAT-COMPRESS) $(SRC_TARBALL) |  $(UNTAR)
    	(							\\
    		module purge; 					\\
    		if [ "$(MODULES)" !=  "" ]; then module $(AUTOMODULE) load $(MODULES); fi;	\\
    		[ $(DO_CD) == True ] && cd $(SRC_DIR);    	\\
    		$(PATCH_METHOD) $(PATCH_ARGS) < ../$(PATCH_FILE);  		\\
    		$(PRECONFIGURE);				\\
    		$(CONFIGURE) $(CONFIGURE_ARGS);  		\\
    		$(PKGMAKE) $(BUILDTARGET) ;			\\
    		module purge; 					\\
    	)
    
    :blue:`install::`
    	(							\\
    		module purge; 					\\
    		if [ "$(MODULES)" !=  "" ]; then module $(AUTOMODULE) load $(MODULES); fi;	\\
    		[ $(DO_CD) == True ] && cd $(SRC_DIR);		\\
    		if [ ! -d $(ROOT)/$(PKGROOT) ]; then mkdir -p $(ROOT)/$(PKGROOT); fi; \\
    		if [ "$(MAKEINSTALL)" == "" ]; then		\\
    			$(MAKE) prefix=$(ROOT)$(PKGROOT) $(INSTALLTARGET);	\\
    		else 						\\
    			$(CUSTOM_MAKEINSTALL);				\\
    		fi;						\\
    		if [ "$(MODULENAME)" != "" -a "$(MODULESPATH)" != "" ]; then		\\
    			mkdir -p $(ROOT)/$(MODULESPATH);     				\\
    			$(INSTALL) -m 644 $(MODFILE_DIR)/modulefile $(ROOT)/$(MODULESPATH)/$(MODULENAME);  	\\
    		fi;								\\
    		if [ "$(INSTALLEXTRA)" != "" ]; then $(CUSTOM_INSTALLEXTRA); fi; \\
    		module purge; 					\\
    	)
    
* The generated spec file executes the **build** target in this Makefile when |rpmb| is executing
  the ``%build`` stanza of the generate spec files

* The generated spec file executes the **install** target in this Makefile when |rpmb| is executing the
  ``%install`` stanza of the generated spec file

It's instructive to look at the ``build`` target in describe in plain english the usual steps:

 1. It extracts (untar/unzip) the source tarball of the software (``src_tarball`` in the yamlfile)
 2. Purges all modules and then loads any modules required for compilation (``build.modules`` in the yamlfile)
 3. Changes into the directory extracted in step 1, unless told not to (``no_src_dir: True`` in the yamlfile)
 4. Applies any patches (``build.patchfile`` in the yamlfile)
 5. Configures the software (``build.configure`` and ``build.configure_args`` in the yamlfile)
 6. Compiles the software (``build.pkgmake`` and ``build.target`` in the yamlfile)
 7. Purges all modules

This is the same ordering of "macro" steps the every package build undergoes. There are *defaults* for 
every key in the yamlfile that covers the most common cases (including: configure is ``./configure``,
no patchfile, no modules, pkgmake is ``make``)

Likewise, the install can be examined in the same detail, but is left as an exercise.

Role of gen-definitions.py
~~~~~~~~~~~~~~~~~~~~~~~~~~

:command:`gen-definitions.py` creates the file ``Definitions.mk`` in the  temporary build directory
(:ref:`Item 3 <dd_makefiles>`).  

.. important:: 
   ``Definitions.mk`` defines the variables that are used *verbatim* in the  
   :ref:`Software Compilation <dd_makefiles>` Makefile.


