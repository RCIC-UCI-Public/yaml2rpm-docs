.. _quickstart:

Quickstart
==========

Make sure the :ref:`requirements` are met.

Yaml2rpm is best built directly from the git repository.  Part of that build process will create RPMs
that can be installed on other machines. On a reasonable system with good network connectivity (or locally-mirrored
repositories) it takes roughly 2 minutes to set up a system to build RPMS using yaml2rpm.

Building Yaml2rpm
-----------------

Run the following commands to checkout the admic repo and to build
all its RPMs:

   .. parsed-literal::

      :command:`git clone https://github.com/RCIC-UCI-Public/yaml2rpm`
      :command:`cd yaml2rpm`
      :command:`./first-build.sh`

When the above has completed, you will see the following line of output

   .. code-block:: bash

      === First Build completed ===
      Start a new bash shell or logout/login to make certain all scripts from /etc/profile.d are sourced


As of Rocky 10, 18 RPMs are added to the system during the first-build. Of these, the following
RPMs are built (the rest are OS- or EPEL-supplied packages):

    * **rocks-devel** - core Makefile structure generate spec files 
    * **python-ruamel-yaml** - specific YAML parser
    * **python-ruamel-yaml-clib** - specific YAML parser library
    * **rcic-module-support** - provides support and common code for the environment modules
    * **rcic-module-path** - support and common code for updating system modules path
    * **yaml2rpm** - main code and tools

| See the detailed RPMs description in :ref:`yaml2rpm`.
| The information about what exact RPMS were added can be discovered using ``yum history``.

If you don't want to exit the shell, but instead want to source profile.d
scripts that were added by RPMs, then do the following:

   .. parsed-literal::
      :command:`. /etc/profile.d/rcic-modules.sh`
      :command:`. /etc/profile.d/yaml2rpm.sh`

Any subsequent container start from the same overlay will do sourcing automatically. 

First RPM Build 
---------------

Yaml2rpm was built to create collections of similar software that we term **admixes**.
Here, the **buildtools-admix** is used as an example. The complete admix has
several packages at different versions of software, but this section highlights just one, *curl*
that we use to build a specific RPM.

.. The usual way to build an entire admix is, at the top-level execute:
   .. parsed-literal::
      :command:`make buildall`
      or alternatively when we do parallel build
      :command:`make buildall-parallel`

These following steps to build *curl* RPM break down some of the things
that happen. The first is adding via ``yum`` OS-supplied packages that are required to build software in the admix.

1. Clone the repo

   .. parsed-literal::
      :command:`git clone https://github.com/RCIC-UCI-Public/buildtools-admix
      cd buildtools-admix/yamlspecs`

#. Prep the build environment with additional OS packages that are needed for the build.

   .. parsed-literal::
      :command:`gen-definitions.py --query=system packages.yaml | xargs yum -y install`

#. Download source distro and build RPM.

   Curl is in a set of software (named *2024* in this example). The source tarball for the particular version
   defined in the set needs to be downloaded, and then the package itself needs to be created:

   .. parsed-literal::
      :command:`make SET=2024 PKG=curl download
      make SET=2024 curl.pkg`

   You could also create the environment module that goes with this version of curl:

   .. parsed-literal::
      :command:`make SET=2024 curl-module.pkg`

   With the steps above, two RPMs have been created and can be installed on any system. These are
   the *products* of the process.  You can list the RPMs to see similar output as below:

   .. parsed-literal::
      :command:`ls -l ../RPMS/x86_64/`
      total 949
      -rw-r--r--. 1 root root 992780 May  1 11:11 curl_7.81.0-7.81.0-1.x86_64.rpm
      -rw-r--r--. 1 root root   7744 May  1 11:15 curl_7.81.0-module-7.81.0-1.x86_64.rpm

#. Inspect created RPMs.

   Dependencies *are* encoded in the RPMs. For example, if you attempt to install just the module above with

   .. parsed-literal::
      :command:`yum install ../RPMS/x86_64/curl_7.81.0-module-7.81.0-1.x86_64.rpm`

   Errors similar to the following are expected:

   .. parsed-literal::
      Last metadata expiration check: 0:10:43 ago on Fri May  1 11:09:09 2026.
      Error:
       Problem: conflicting requests
        - nothing provides curl_7.81.0 needed by curl_7.81.0-module-7.81.0-1.x86_64 from @commandline
      (try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)

#. Create local repo.

   All admixes have a *createlocalrepo* make target when executed from the top-level of the admix. 
   This can followed by a yum install. When both the curl and the curl-module
   RPMs are available in a local (to this admix) yum repository, the dependency will be resolved:

   .. parsed-literal::
      :command:`make createlocalrepo
      yum -c yum.conf install curl_7.81.0-module`
