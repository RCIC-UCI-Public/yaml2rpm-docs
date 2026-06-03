.. _about-admixes:

About
=====

There are a few admixes that serve very specific purpose
and their layout is more complex.
The step-by-step instructions and the details of the builds are explained in
each admix (links below).

| :ref:`yaml2rpm <yaml2rpm>` 
| :ref:`admixbuilder <admixbuilder>`
|   They provide tools for the other admixes to be built.
    Their internal layout, build  and what they provide differ 
    substantially from  the rest of the admixes. These are first basic
    admixes that are needed to build the rest. 

| :ref:`gcc-admix <gcc-admix>`
|   Enables multiple versions of compilers
    needed for compiling various software packages in nearly all other admixes.

| :ref:`perl-admix <perl_admix>`
| :ref:`python-admix <python_admix>` 
| :ref:`R4-admix <R4_admix>`
|   They provide installations of multiple versions of Perl, Python and R.
    Each has a local customization to its layout and build process.

  How they are  built:
    - Define a list of desired libraries/modules/packages.
    - Use the platform-provided software and custom scripts to query what
      is required to determine build order of respective module packages.
    - Auto-generate yaml files (perl-admix,R4-admix) used for building RPMs.
    - Fix (sparingly) generated yaml files to handle edge cases (patching or other problems. R is the most problematic)
    - When the yaml files have been defined and debugged for a particular version, *freeze* them 
      for that specific version. 

| :ref:`protected-admix <protected_admix>`
|   Provides tools compiled from protected (distributed by license) sources
    such as VASP, Quantum Espresso, Rosetta.

Approach when underlying OS changes (minor/major)
process can take a few weeks or a months (major) to work out all the details/differences
admix-by-admix, in order, package-by-package.
The older the software, the more problematic an OS change is. (Sometimes have to give up, e.g. cufflinks)

