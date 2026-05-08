.. _gen-definitions:

Reference gen-definitions.py
============================

.. raw:: html

   <style> .blue {color:mediumblue} </style>

.. role:: blue


The python program, ``gen-definitions.py`` is the workhorse for interpreting yaml-formatted package specifications.
It is compact, can be inspected and is under 1000 lines with all blanks, comments, and usage statements.  Its 
primary role is to generate the ``Definitions.mk`` file used in the :ref:`rocks-devel stage <dd_rocks_devel>` stage
of building an RPM.  It has other uses and is called in different ways for various Makefile targets.  
The following is the output (typos included) when
called with the ``--help`` flag. The major arguments are highlighted.

**gen-definitions.py help**

``gen-defintitions`` takes one (or more) yaml-formatted files and a ``versions.yaml`` file to produce output. 

  .. literalinclude:: files/gen-definitions-help
      :language: text 

  Highlighting a few flags that a developer of yaml-formatted package file would use interactively

  - **--versions** - use named versions file inplace of ``versions.yaml``. For example, if a yaml file
    has an ``!include versions.yaml`` statement, the file named here will be included instead 
  - **--query** - For any key in the yaml file, print the final evaluation of the variable.  
  - **--module** - Generate an `environment-modules <https://modules.readthedocs.io/en/latest/>`_ definition
    instead of ``Defaults.mk``  

As some examples, refer to the :ref:`gcc admix layout <ov_gcc_admix>` for the files and layout of the admix.

**query**

Here are some example queries

  .. parsed-literal::

       :blue:`gen-definitions.py --versions=versions-gcc15.yaml --query=gcc_version gcc.yaml`
         15.2.0
       :blue:`gen-definitions.py --versions=versions-gcc11.yaml --query=gcc_version gcc.yaml`
         1.2.0
       :blue:`gen-definitions.py --versions=versions-gcc8.yaml --query=gcc_version gcc.yaml`
         8.4.0
       :blue:`gen-definitions.py --versions=versions-gcc8.yaml --query=pkgname gmp.yaml`
         gcc_8.4.0-gmp
       :blue:`gen-definitions.py --versions=versions-gcc11.yaml --query=pkgname gmp.yaml`
         gcc_11.2.0-gmp
       :blue:`gen-definitions.py --query=gcc versions-gcc8.yaml`
         8.4.0
       :blue:`gen-definitions.py --query=annobin versions-gcc8.yaml`
         10.54

.. note::
   Notice the naming of the gmp packages when ``pkgname`` is the query argument.  This is standard
   prefixing (e.g. gcc_8.4.0) to label the gmp package relative to the compiler it was built with.
   Both of the gmp packages above can be installed on an end system without conflict


**module**

Environment module files are generated from yaml files that have an ``!include rcic=module.yaml`` 
line. Here is the particular example

  .. code-block:: bash

    gen-definitions.py -m --versions=versions-gcc11.yaml gcc-module.yaml


  .. literalinclude:: files/gcc-module-11
     :language: text

  - compare this output to the :ref:`gcc-module.yaml <ov_gcc_module>`  to see how the generic definition
    differs from the final module file


Parallelism
-----------

There are certain steps in a full build where a large number of yaml files need to be processed. The most notable step
is when a manifest with ``make manifest`` is requested for a particular admix. Each package.yaml defined in a
set's manifest must be queried with the ``--query=pkgname`` argument.  Yaml processing is heavyweight. In admixes with
100's of packages in a set, this can be very time consuming if performed sequentially. In this case,
all of the package.yaml files for a particular set are handled in parallel. Internally, gen-definitions.py uses
the python multiprocessing library




