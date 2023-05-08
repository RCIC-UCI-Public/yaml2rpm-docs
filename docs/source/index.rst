.. note::
   This project is under active development.

.. warning::
   The documentaion pages are currently a template


YAML2RPM Documentation
======================

Welcome to the documentation for YAML2RPM.

We developed YAML2RPM to manage the multiple versions, dependencies, and other details of a resilient software deployment.
**YAML**-formatted specification files are used to describe how to build an application, encode dependencies, and where to install.
Through programmatic translation via a **custom python program**, the YAML input generates the ingredients to build a 
RedHat-compatible RPM using the distribution's native **rpmbuild** tool. The full process creates human-recognizable package names,
supports multiple installed versions, and easily encodes dependencies for repeatable and robust application stacks.
In a full-stack recompilation, over 2000 individual RPMs are created.

The documentation will describe the process, point out many advantages and describe many examples in detail.
Our approach makes routine packaging of applications very straightforward and reduces difficult builds to 
manageable ones. YAML2RPM and our recipes for building 100s of applications are open source.

**yaml2rpm** has its documentation hosted on Read The Docs.

.. toctree::
   :glob:
   :caption: About Yaml2rpm

   about/preface
   about/architecture

.. toctree::
   :caption: Installation

   installation/requirements
   installation/api

.. toctree::
   :caption: Admixes

   admixes/admixbuilder
   admixes/gcc

.. toctree::
   :caption: Reference

   references/glossary
   references/changelog
