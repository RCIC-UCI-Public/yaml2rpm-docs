.. _requirements:

Requirements
=============

.. important:: We **highly recommend** that you prepare and build in a :ref:`singularity container<dd_container>`. Like many builds,
   the build system itself is modified. In this case, numerous system-level RPMs are added as are newly created RPMs.
   Building inside of container protects the physical system from this inevitable change.

For a quick start testing on a standard CentOS machine  or a singularity container:

1. Python 3 and its ``argparse``, ``socket``, ``datetime`` modules 
   (provided via OS RPMS).

#. If you are using a very stripped-down CentOS image (similar to the official CentOS 9 image in Amazon, you will
   want to make certain you have the following packages and package groups installed

   .. parsed-literal:: 
      :command:`yum groupinstall "Development Tools" "Console Internet Tools"
      yum install redhat-lsb wget zlib-devel environment-modules
      . /etc/profile.d/modules.sh`
