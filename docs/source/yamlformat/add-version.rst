
.. _add_version:

Add a New Version of Software
=============================

**Table of contents:**

.. contents::
   :local:

It is common that an updated version of software is required.  As an example, we'll look
at `vcftools <https://github.com/vcftools/vcftools/>`_ in the biotools-admix. The baseline
version is "0.1.16" (released in 2018) while the latest is "0.1.17" (released in 2025). 

Locate the Current Source
-------------------------

In the biotools admix, there are several sets. To determine which set(s) the software is currently referenced,
simply ``grep`` all the set files:

  .. parsed-literal::
     :command:`grep vcftools set*`
     set-base.yaml:  - vcftools
     set-base.yaml:  - vcftools-module

Vcftools is only referenced in the base set. One can use ``gen-definitions.py`` to query the vendor source
as follows:

  .. parsed-literal::
     :command:`gen-definitions.py --query=vendor_source  vcftools.yaml`
     \https://github.com/vcftools/vcftools/archive/v0.1.16.tar.gz

Open a browser and visit the git repository and see if there is an additional release.

Add the Information to Existing Set
-----------------------------------

There are numerous sets already existing in the 
:ref: `biotools-admix repository <https://github.com/RCIC-UCI-Public/biotools-admix/>`_.
Since vcftools is only defined in the base set, it's simplest to add to an existing set.
For this example, extending set *2025* makes sense. The contents of ``set-2025.yaml`` are:

  .. code-block:: yaml

     !include packages.yaml
     ---
     versions: versions-2025.yaml
     bootstrap:
     build:
       - dorado
       - dorado-module
       - gatk
       - gatk-module

Notice that the versions file used for this set is ``versions-2025.yaml``. The versions file can be any yaml
file, but convention is to use *versions-<set name>.yaml*, as in this example.
Vcftools has an environment module and programs.  Modify ``set-2025.yaml`` to have contents:

  .. code-block:: yaml

     !include packages.yaml
     ---
     versions: versions-2025.yaml
     bootstrap:
     build:
       - dorado
       - dorado-module
       - gatk
       - gatk-module
       - vcftools
       - vcftools-module

You also need to modify the ``versions-2025.yaml`` to include the updated vcftools version:

  .. code-block:: yaml

     !include versions.yaml
     !include updates8.yaml
     ---
     dorado: "0.9.1"
     gatk: "4.6.2.0"
     vcftools: "0.1.17"

  See :ref:`details <versions_yaml>` for file format. 

Verify Changes
--------------

Now check that the updated vendor source resolves properly. Use ``gen-definitions.py``, but with
the updated ``versions-2025.yaml`` file:

  .. parsed-literal::

     :command:`gen-definitions.py --versions=versions-2025.yaml --query=vendor_source  vcftools.yaml`
     \https://github.com/vcftools/vcftools/archive/v0.1.17.tar.gz

Verify that this a good web reference and then **download the source tarball**:

  .. parsed-literal::

     :command:`make -s SET=2025 PKG=vcftools download`
      --2026-05-12 10:59:12--  \https://github.com/vcftools/vcftools/archive/v0.1.17.tar.gz
      Resolving github.com (github.com)... 140.82.116.4
      Connecting to github.com (github.com)|140.82.116.4|:443... connected.
      HTTP request sent, awaiting response... 302 Found
      Location: \https://codeload.github.com/vcftools/vcftools/tar.gz/refs/tags/v0.1.17 [following]
      --2026-05-12 10:59:13--  \https://codeload.github.com/vcftools/vcftools/tar.gz/refs/tags/v0.1.17
      Resolving codeload.github.com (codeload.github.com)... 140.82.116.10
      Connecting to codeload.github.com (codeload.github.com)|140.82.116.10|:443... connected.
      HTTP request sent, awaiting response... 200 OK
      Length: unspecified [application/x-gzip]
      Saving to: '/export/repositories/biotools-admix/sources/vcftools-0.1.17.tar.gz'

      /export/repositories/biotools-a     [ <=>                                   ] 241.88K  --.-KB/s    in 0.1s    

      2026-05-12 10:59:13 (2.03 MB/s) - '/export/repositories/biotools-admix/sources/vcftools-0.1.17.tar.gz' saved [247685]

Build
-----

It's time to build the package and module:

  .. parsed-literal::
     :command:`make SET=2025 vcftools.pkg vcftools-module.pkg`

Install
-------

Once the RPMs are built need to install to verify that there are no unresolved dependencies.
From the ``yamlspecs/`` directory:

  .. parsed-literal::
     :command:`make -C .. clean createlocalrepo 
     yum -c ../yum.conf install vcftools_0.1.17  vcftools_0.1.17-module`


Make it reproducible
--------------------

If everything works, memorialize all of the above into git.
All commands below are done from the admix top-level directory. 

**1. Upload the latest tarball into S3**
  To upload to S3 (for future builds), you must have *write* permissions on the remote S3 bucket. Place the tarball
  in the same location as all of the other biotools-admix tarballs. Rclone is a convenient way to do this.
  :red:`If and only if in RCIC and your rclone credentials are setup` the simplest way to upload:

  .. parsed-literal::
     :command:`cd sources
     rclone --config=/import/rclone.conf copy .  aws:admix-sources/biotools-admix`

**2. Create the sha1sum**
  Downloading all source distribution files to the ``sources/`` in the admix references the ``<admix-name>.metadata`` file. 
  To add the sha1sum of the latest tarball to the admix metadata file:

  .. parsed-literal::
     :command:`sha1sum sources/vcftools-0.1.17.tar.gz >> .biotools-admix.metadata`

**3. Update the admix rpmdb**
  To add the info about new RPMS to the existing admix RPM database file:

  .. parsed-literal::
     :command:`make -s admixdb`

  From the stdout get 2 lines for newly created vcftools RPMs and add them to
  the ``.rpms.biotools-admix`` file. Alternatively overwrite the file:

  .. parsed-literal::
     :command:`make -s admixdb > .rpms.biotools-admix`

**4. Commit changes to git**
  There were changes in 4 files.:

  .. parsed-literal::
     :command:`git add .biotools-admix.metadata
     git add .rpms.biotools-admix
     git add yamlspecs/set-2025.yaml
     git add yamlspecs/versions-2025.yaml
     git commit
     git push`

Other Verification
------------------

This was a very simple example of adding a new version of existing software. It's build method didn't change,
just the version. 

**Check RPMS**
  Look at the vcftools RPMS and see if their sizes seem rational. In this example, the later version is
  slightly larger than the original. Likely, the build is fine.

  .. parsed-literal::
     :command:`ls -l RPMS/x86_64/vcftools*`
     -rw-r--r--. 1 root root 424527 May  8 03:56 RPMS/x86_64/vcftools_0.1.16-0.1.16-2.x86_64.rpm
     -rw-r--r--. 1 root root   7681 May  8 03:55 RPMS/x86_64/vcftools_0.1.16-module-0.1.16-2.x86_64.rpm
     -rw-r--r--. 1 root root 446793 May 12 11:03 RPMS/x86_64/vcftools_0.1.17-0.1.17-2.x86_64.rpm
     -rw-r--r--. 1 root root   7683 May 12 11:03 RPMS/x86_64/vcftools_0.1.17-module-0.1.17-2.x86_64.rpm

**Check Manifest**
  This additional version is now part of the manifest for the biotools-admix

  .. parsed-literal::
     :command:`make -s manifest | grep vcftools`
     vcftools_0.1.16
     vcftools_0.1.16-module
     vcftools_0.1.17
     vcftools_0.1.17-module


