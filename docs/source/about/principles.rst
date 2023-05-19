.. _principles:

Principles 
===========

.. raw:: html

   <style> .blue {color:#00579e;font-weight: bold} </style>
   <style> .lightblue {color: #0092e0;text-decoration: underline;} </style>
   <style> .proposed {color: #00afaf; font-weight: bold;} </style>
   <style> .orange {color: #e56306; font-weight: bold;} </style>

.. role:: blue
.. role:: lightblue
.. role:: proposed
.. role:: orange

The main design principles are:

.. :proposed:`Use existing packaging system`

**Use existing packaging system**
  We use :term:`DNF` and :term:`RPM` tools which are standard for RPM-based 
  Linux distributions.  Using native OS tools for building, installing and 
  verifying  packages allows us to rely on existing commands which simplifies
  packages management. We can make custom names and dependencies as needed
  and never have a name conflict with the OS-provided RPMs.

**Small code base**
  A small code base is easy to debug and maintain. 
  Very minimal dependency on Python packages, a handful of standard python
  packages we build and install: ``ruamel-yaml``, ``ruamel-yaml-clib``, and
  ``setuptools``. The :term:`main script` that does all the yaml processing is
  custom built. We wrote a couple of specific yaml processing extensions 
  allow us to use more programmatic concepts in the yaml description files. 

Human-readable package definition files
  ---------------------------------------
  Small yaml files are simple and while terse are easily readable without any
  special tools or commands.  They have all the information needed by 
  the :term:`main script` processing.

**Package definition reuse as much as possible**
  Often packages have similar set of steps for some aspects of their build.
  We reuse existing definitions via inclusion of common blocks which define
  a lot of default functionality.  This allows us to minimize definition writing
  while providing a simple way to introduce additional options.

**Easily build many packages and their versions**
  We can build hundreds of software packages as well as  multiple versions of specific
  packages with a very small personnel cost. Once the initial definition yaml
  file correctness is verified the build process of a new RPMs is fully automated.

**Simultaneous installation of multiple versions of the same software**
  The packages coexist without imposing on each other, new installs and old
  uninstalls do not break any other packages. 
  Environmental modules  for a runtime selection are the main route for the
  users to easily switch among different packages and versions.
