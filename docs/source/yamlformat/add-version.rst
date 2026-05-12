
.. _add_version:

Adding a New Version of Software
================================

**Table of contents:**

.. contents::
   :local:

It is common that an updated version of software is required.  As an example, we'll look
at `vcftools <https://github.com/vcftools/vcftools/>`_ in the biotools admix. The baseline
version is "0.1.16" (released in 2018) while the latest is "0.1.17" (released in 2025). 

Locating the Current Source
---------------------------

In the biotools admix, there are several sets. To determine which set(s) the software is currently referenced,
simply ``grep`` all the set files.

.. parsed-literal::

   :blue:`grep vcftools set*`
   set-base.yaml:  - vcftools
   set-base.yaml:  - vcftools-module

Vcftools is only referenced in the base set. One can use ``gen-definitions.py`` to query the vendor source
as follows

.. parsed-literal::

   :blue:`gen-definitions.py --query=vendor_source  vcftools.yaml`
   https://github.com/vcftools/vcftools/archive/v0.1.16.tar.gz

Open a browser and visit the git repository and see if there is an additional release.

Add the Information to Existing Set
-----------------------------------

There are numerous sets already existing in the biotools admix. 
Since vcftools is only defined in the base, it's simplest to add to
an existing set.  For this example, extending set *2025* makes sense. The contents of set-2025 are:

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
file, but convention is to use *versions-<set name>.yaml*, as in this example. Vcftools has both a module and program. 
Modify ``set-2025.yaml`` to have contents

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

You also need to modify the `versions-2025.yaml` to include the updated vcftools version

.. code-block:: yaml

   !include versions.yaml
   !include updates8.yaml
   ---
   dorado: "0.9.1"
   gatk: "4.6.2.0"
   vcftools: "0.1.17"

.. note::
   Most entries in versions files are simple key-value pairs. Inspect the *versions.yaml* file in this admix
   and look at the *pysam* entry. Notice that that the value is a *dictionary*. 
   Further inspect ``pysam.yaml`` and see how 
   the  elements of the dictionary are referenced (e.g., ``{{versions.pysam.pymajor}}``).

Verify Changes
--------------

Now check that the updated vendor source resolves properly. Use gen-definitions.py, but with
the updated versions-2025.yaml file.

.. parsed-literal::

   :blue:`gen-definitions.py --versions=versions-2025.yaml --query=vendor_source  vcftools.yaml`
   https://github.com/vcftools/vcftools/archive/v0.1.17.tar.gz

Verify that this a good web reference and then **download the source tarball**. 


.. parsed-literal::

   :blue:`make -s SET=2025 PKG=vcftools download`
    --2026-05-12 10:59:12--  https://github.com/vcftools/vcftools/archive/v0.1.17.tar.gz
    Resolving github.com (github.com)... 140.82.116.4
    Connecting to github.com (github.com)|140.82.116.4|:443... connected.
    HTTP request sent, awaiting response... 302 Found
    Location: https://codeload.github.com/vcftools/vcftools/tar.gz/refs/tags/v0.1.17 [following]
    --2026-05-12 10:59:13--  https://codeload.github.com/vcftools/vcftools/tar.gz/refs/tags/v0.1.17
    Resolving codeload.github.com (codeload.github.com)... 140.82.116.10
    Connecting to codeload.github.com (codeload.github.com)|140.82.116.10|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: unspecified [application/x-gzip]
    Saving to: '/export/repositories/biotools-admix/sources/vcftools-0.1.17.tar.gz'
    
    /export/repositories/biotools-a     [ <=>                                                    ] 241.88K  --.-KB/s    in 0.1s    
    
    2026-05-12 10:59:13 (2.03 MB/s) - '/export/repositories/biotools-admix/sources/vcftools-0.1.17.tar.gz' saved [247685]


Build
-----
It's time to build the package and module:

.. parsed-literal::

    make SET=2025 vcftools.pkg vcftools-module.pkg

Make it reproducible
--------------------


If everything works,  memorialize all of the above into git 

1. Upload the latest tarball into S3 (for future builds)
2. Add the sha1sum of the latest tarball to the admix metadata file
3. Commit changes to git


Upload
~~~~~~

To upload the tarball to S3, you must have *write* permissions on the remote S3 bucket. Place the tarball
in the same location as all of the other biotools-admix tarballs. Rclone is a convenenient way to do this

From the top-level directory of the admix and if in RCIC and your rclone credentials are setup, the simplest way to get new file in place is

.. parsed-literal::

   cd sources
   rclone --config=/import/rclone.conf copy . aws:admix-sources/biotools-admix

Create the sha1sum
~~~~~~~~~~~~~~~~~~

Downloading all files in an admix references the ``<admix-name>.metadata`` file. From the the top-level
of the admix simply execute

.. parsed-literal::

   sha1sum sources/vcftools-0.1.17.tar.gz >> .biotools-admix.metadata

Commit and push changes
~~~~~~~~~~~~~~~~~~~~~~~

.. parsed-literal::
   git add .biotools-admix.metadata
   git add yamlspecs/set-2025.yaml yamlspecs/versions-2025.yaml
   git commit
   git push

Other Verifications
-------------------

This was a very simple example of adding a new version of existing software. It's build method didn't change,
just the version. 

Built RPMS
~~~~~~~~~~

Look at the vcftools RPMS and see if their sizes seem rational. In this example, the later version is
slightly larger than the original. Likely, the build is fine.

.. parsed-literal::
   
   :blue:`ls -l RPMS/x86_64/vcftools*`
   -rw-r--r--. 1 root root 424527 May  8 03:56 RPMS/x86_64/vcftools_0.1.16-0.1.16-2.x86_64.rpm
   -rw-r--r--. 1 root root   7681 May  8 03:55 RPMS/x86_64/vcftools_0.1.16-module-0.1.16-2.x86_64.rpm
   -rw-r--r--. 1 root root 446793 May 12 11:03 RPMS/x86_64/vcftools_0.1.17-0.1.17-2.x86_64.rpm
   -rw-r--r--. 1 root root   7683 May 12 11:03 RPMS/x86_64/vcftools_0.1.17-module-0.1.17-2.x86_64.rpm

Manifest
~~~~~~~~

This additional version is now part of the manifest for the biotools-admix

.. parsed-literal::

   :blue:`make -s manifest | grep vcftools`
   vcftools_0.1.16
   vcftools_0.1.16-module
   vcftools_0.1.17
   vcftools_0.1.17-module


