.. _quickstart:

Quickstart
==========

Yaml2rpm is best built directly from the git repository.  Part of that build process will create RPMs
that can be installed on other machines. On a reasonable system with good network connectivity (or locally-mirrored
repositories) it takes roughly 2 minutes to set up a system to build RPMS using yaml2rpm. We **highly
recommend** that you prepare and build in a :ref:`singularity container<dd_container>`. Like many builds,
the build system itself is modified. In this case, numerous system-level RPMs are added as are newly created RPMs.
Building inside of container protects the physical system from this inevitable change.

Building Yaml2rpm
-----------------


   .. parsed-literal::

      :command:`git clone https://github.com/RCIC-UCI-Public/yaml2rpm`
      :command:`cd yaml2rpm`
      :command:`./first-build.sh`


When the above has completed, you will see the following line of output
   .. code-block:: bash

      === First Build completed ===
      Start a new bash shell or logout/login to make certain all profile.d scripts


As of Rocky 10, 18 RPMs are added to the system during the first-build. Of these, the following
RPMs are built (the rest are OS- or EPEL-supplied packages). The information can be discovered using
``yum history``.

    * ``rocks-devel`` core Makefile structure generate spec files 
    * ``python-ruamel-yaml`` specific YAML parser
    * ``python-ruamel-yaml-clib`` specific YAML parser library
    * ``rcic-module-support``
    * ``rcic-module-path``
    * ``yaml2rpm``

If you don't want to exit the shell, but instead want source profile.d scripts, then do the following

   .. parsed-literal::
      :command:`. /etc/profile.d/rcic-modules.sh`
      :command:`. /etc/profile.d/yaml2rpm.sh`


First RPM Build 
^^^^^^^^^^^^^^^

:red:`TODO: remove this section, outdated`

Yaml2rpm was built to create collections of similar software that we term **admixes**.
Here, the buildtools-admix is used as an example. The complete admix has several versions of software, but
this sections highlights just one, *curl*.

The usual way to build an entire admix is, at the top-level execute 
``make buildall`` (or ``make buildall-parallel``).  Instead, these examples break down some of the things
that happen. The first is adding an os-supplied packages, via yum, that are required to build software in the admix.

Cloning and then *prepping the build environment with additional os packages*

.. code-block:: bash

   git clone https://github.com/RCIC-UCI-Public/buildtools-admix
   cd buildtools-admix/yamlspecs
   gen-definitions.py --query=system packages.yaml | xargs yum -y install

Curl is in a set of software (named '2024' in this example). The source tarball for the particular version
defined in the set needs to be downloaded, and then the package itself needs to be created 

.. code-block:: bash

   make SET=2024 PKG=curl download
   make SET=2024 curl.pkg

You could also create the enviroment module that goes with this version of curl

.. code-block:: bash

   make SET=2024 curl-module.pkg

With the steps above, two rpms have been created and can be installed on any system. These are
the *products* of the process.  You can list the rpms to see similar output as below

.. parsed-literal:: 

   :blue:`ls -l ../RPMS/x86_64/`
   total 949
   -rw-r--r--. 1 root root 992780 May  1 11:11 curl_7.81.0-7.81.0-1.x86_64.rpm
   -rw-r--r--. 1 root root   7744 May  1 11:15 curl_7.81.0-module-7.81.0-1.x86_64.rpm

Dependencies *are* encoded in the RPMs. For example, if you attempt to install just the module above with

.. code-block:: bash
 
   yum install ../RPMS/x86_64/curl_7.81.0-module-7.81.0-1.x86_64.rpm

Errors similar to the following are expected

.. parsed-literal::

    Last metadata expiration check: 0:10:43 ago on Fri May  1 11:09:09 2026.
    Error:
     Problem: conflicting requests
      - nothing provides curl_7.81.0 needed by curl_7.81.0-module-7.81.0-1.x86_64 from @commandline
    (try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)

All admixes have a "createlocalrepo" make target when executed from the top-level of the admix, 
followed by a yum install. When both the curl and the curl-module rpms are available in a yum repository, the
dependency will be resolved.

.. parsed-literal::

   make createlocalrepo
   yum -c yum.conf install curl_7.81.0-module
