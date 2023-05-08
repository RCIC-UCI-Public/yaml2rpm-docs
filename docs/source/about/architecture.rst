Architecture
=============

.. _architecture:


Python scripts
--------------

There is one main driver script called ``gen-definitions.py``
This is the definitions parser that reads info defined in yaml files and creates
necessary output files in order to build RPMS.


Templates
---------

There are a few Makefiles that are used as templates when crating packages

In addition, there are a few templates written in yaml that provide basic 
configuration and settings. These templates are included in the 
specific software yaml description files



