YAML2RPM documentation to use with RTD 
======================================

This repo https://github.com/RCIC-UCI-Public/yaml2rpm-docs
provides YAML2RPM documentation that is created with Read The Docs (RTD).

The resulting website served at RTD  server as

- https://yaml2rpm.readthedocs.io
- https://yaml2rpm.rdfd.io  (equivalent shorthand notation)

Building HTML locally for testing
---------------------------------

1. Install prerequisites

   .. code-block:: console

      pip3 install sphinx
      pip3 install sphinx_rtd_theme

2. Check out repo and build

   .. code-block:: console

      git clone git@github.com:RCIC-UCI-Public/yaml2rpm-docs.git
      cd yaml2rpm-docs/docs
      make html

3. Point your local browser to `build/html/index.html`.


Initial Setup Notes
-------------------

1. The github repo was imported into the RTD per the tutorial:
   https://docs.readthedocs.io/en/stable/tutorial/

   The repo for this tutorial is https://github.com/readthedocs/tutorial-template/

2. Added manual integration of the github repo with Read the Docs (RTD) project
   https://docs.readthedocs.io/en/stable/guides/git-integrations.html

   Note, manual integration involves 

   * creating integration in **Console -> Admin -> Integrations**  on RTD console
   * and then adding this info to the github repo in **Settings -> Webhooks**

     Edit:

     - Payload URL (http url from RTD)
     - content type (application/json)
     - choose enable ssl verification

     - choose **let me select individual events** and choose

       - branch or tag creation
       - branch or tag deletion
       - pull requests
       - pushes
       - Active

     Save. After this is set any changes to the github repo files per above
     events will trigger a build automatically.

   Had to add ``.readthedocs.yaml`` file in order to specify what type of a build
   RTD need to do. This is needed to fix a recent update to  urllib3 which
   is used in docker container and a recent (early May) urllib3 release is
   incompatible with the Ubuntu docker image used by the RTD. 
   See RTD issues on https://github.com/readthedocs/readthedocs.org/issues/10290
   Info in RTD tutorials is at https://docs.readthedocs.io/en/stable/config-file/v2.html

3. Useful RTD project links

   Only maintainer/admin can access  these:

   - console https://readthedocs.org/projects/yaml2rpm/
   - build info https://readthedocs.org/projects/yaml2rpm/builds/

   Email about failed builds is sent to the maintainer.


Useful info links 
-----------------

- Automatic module documentation with **automodapi** 
  
  - https://sphinx-automodapi.readthedocs.io/en/latest/automodapi.html
  - https://sphinx-automodapi.readthedocs.io/en/latest/

- read the docs build process explanation https://github.com/readthedocs/readthedocs.org/blob/main/docs/user/builds.rst
- how to create reproducible builds https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html
  
  It includes some explanation about ``.readthedocs.yaml`` and
  other respective config files (conf.py and requirements.txt if this one
  exists) per recent RTD changes (2023).

- getting started with sphinx https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html

Updates
-------

2023-08-23

As of September 2023 RTD migrates projects to version 2.
A file .readthedocs.yaml  is updated per https://blog.readthedocs.com/migrate-configuration-v2/
