
.. _next_steps:

Next Steps
===========

Read the remainder of the documentation.
Start with pages in **ADMIX LAYOUT** and follow with pages from **COMPLEX ADMIXES**. 
They explains in-depth admixes purpose, layouts, and their files which will
provide a better understanding of the build process overall.

For inpatient people working on the same OS (currently Rocky 9.7)
can do a :ref:`superbuild <superbuild>` next. 

For step by step build:

1. While on the container, clone the *admixbuilder* repository:

     .. parsed-literal::
        :command:`cd /export/repositories
        git clone https://github.com/RCIC-UCI-Public/admixbuilder`

   This admix provides tools to work with other admixes. 

#. Will need to clone and build admixes one by one
   in order described in ``admixbuidler/buildorder``. At this point already have
   *yaml2rpm* built, the next admix is *buildtools-admix*:

     .. parsed-literal::
        :command:`cd /export/repositories
        git clone https://github.com/RCIC-UCI-Public/buildtools-admix`

#. Build RPMS in *buildtools-admix* 

   **Serial build**
     This is a good option when building on a new OS and it is likely
     that changes will be needed for some builds. Building serially set by set
     provides a targeted control.

     .. parsed-literal::
        :command:`cd buildtools-admix/
    	make download
        make buildall &> out &`

     Check output file ``out`` and resulting RPMs. If there are errors, need to figure
     out what RPMs had problems and waht they are and apply fixes. Then uninstall
     empty or bad RPMs (see list of built RPMS in ``RPMS/``)
     and redo the *buildall* target anew until all RPMs are build and valid. 
     Note, some errors are expected, they are fortmexecuting some commands in
     make targets and are usually noted as *ignored*, for example:

     .. code-block::

        make[1]: [/opt/rocks/share/devel/etc/rocks-version.mk:375: clean] Error 1 (ignored)


   **Parallel build**
     This is usually a part of the :ref:`superbuild` run but each admix can be
     built in parallel fashion:

     .. parsed-literal::
        :command:`cd buildtools-admix/
    	make download
        make buildall-parallel  &> out &`

3. Install the admix RPMs, at the top level of the repo do:

     .. parsed-literal::
       :command:`make install-admix YES=-y`

4.  Proceed with building the next admix in a similar way.

When underlying OS changes
--------------------------

The OS changes bring sometimes unexpected changes:

- the RPMs names change
- some may be no longer offered
- new RPMs will be required to provide the same functionality

.. note:: It can take a few weeks (major OS change) **to work out all the details/differences
          admix-by-admix, in order, package-by-package**. 

The older the software, the more problematic the OS change is for it.  It may result in:

  - applying patches to the software packages (have to create the patches)
  - in changing versions (previous no longer compiles)
  - updating dependencies 
  - adding additional prerequisite software

We try to keep our software stack in accordance with our users needs.
However, there will be situations when the software no longer can be
build under the new OS.
