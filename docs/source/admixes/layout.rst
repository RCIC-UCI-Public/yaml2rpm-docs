Admix structure
===============

.. _admix_internals:

Almost all admixes follow the same layout structure
Here we describe the general structure and the common files
and directories.

All admix repositories are stored in our public github 
on https://github.com/RCIC-UCI-Public

.. raw:: html

   <style> .blue {color:mediumblue} </style>

.. role:: blue

Repository layout
------------------

Here we show the admix structure on a real example of **foundation-admix**.
After clowning of the admix git repo the directory structure is 

.. code-block:: bash

   git clone https://github.com/RCIC-UCI-Public/gcc-admix.git


|  :blue:`foundation-admix/`
|      .foundation-admix.metadata
|      :blue:`.git/`
|      .gitignore
|      Makefile
|      README.md
|      :blue:`yamlspecs/`
|           Makefile
|           common.yaml
|           packages.yaml
|           set-centos8.yaml
|           versions.yaml
|           versions-centos8.yaml
|           cmake.yaml
|           cmake-module.yaml
|           curl.yaml
|           foundation-module.yaml
|           git.yaml
|           git-lfs.yaml
|           ninja.yaml
|           pigz.yaml
|           rubygem-hpricot.yaml
|           rubygem-mustache.yaml
|           rubygem-rdiscount.yaml
|           rubygem-ronn.yaml
|           scons.yaml
|           scons-module.yaml
|           swig.yaml


After the build commands repository structure changes and includes : TODO

