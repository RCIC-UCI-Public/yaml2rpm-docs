Python
======

.. _python-admix:

The `python-admix repository <https://github.com/RCIC-UCI-Public/python-admix/>`_ uses **YAML2RPM** to build 
multiple versions of python. 

Python is relatively complex build and requires local changes to its Makefile to
accomplish multiple builds.

.. warning:: 
  
  This process will install RPMs as it builds. You should do this on a 'disposable' build system.

Here is the full process for building python using the  `python-admix repository
<https://github.com/RCIC-UCI-Public/python-admix/>`_

.. code-block:: bash

   git clone https://github.com/RCIC-UCI-Public/python-admix.git
   cd R4-admix
   make download
   cd yamlspecs
   (make bootstrap &> /tmp/bootstrap-gcc.log; make &> /tmp/build-gcc.log) &

Build details
-------------

TODO
