Principles 
===========

.. _principles:

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

:proposed:`Use existing packaging system`
  for a given OS including dependency resolution.
  Using native OS tools for building, installing and verifying  packages
  allows us to rely on existing OS tools which simplifies  packages
  management. We can make custom names and dependencies as needed and never
  have a name conflict with the OS-provided RPMs.

:proposed:`Small code base`
  is easy to debug and maintain. 
  Very minimal dependency on Python packages, a few packages we need we
  install. The :term:`main script` that does all the yaml processing is
  custom built. We wrote a couple of specific yaml processing extensions 
  allow us to use more programmatic concepts in the yaml description files. 

:proposed:`Human-readable package definition files`
  are simple and usually terse 
  yaml files. They have all the information needed by the :term:`main script`
  processing.

:proposed:`Package definition reuse as much as possible`
  Often packages have
  common approach for  some aspects of their build. We reuse existing 
  definitions via inclusion of common blocks that define a lot of default 
  functionality. 

**Easily build many packages and many versions of packages** 
  with a very small personnel cost. The packages coexist without 
  imposing on each other.  

**Simultaneous installation of multiple versions of the same software**
  with environment modules for a runtime selection. 
  Environmental modules are the main route for the
  users to easily switch among different packages and versions.
