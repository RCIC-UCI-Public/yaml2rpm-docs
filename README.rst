YAML2RPM documentation to use with rial
=======================================

This repo provides YAML2RPM documentation that is
created with Read The Docs.

The resulting website is https://yaml2rpm.readthedocs.io


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

1. The github repo was imported into the RTD per Read the tutorial:
   https://docs.readthedocs.io/en/stable/tutorial/

   The repo for this tutorial is https://github.com/readthedocs/tutorial-template/

2. Added manual integration of the github repo with Read the Docs (RTD) project
   https://docs.readthedocs.io/en/stable/guides/git-integrations.html

   Had to add ``.readthedocs.yaml`` file in order to specify what type of a build
   RTD need to do. This is needed to fix a recent update to  urllib3 which
   is used in docker container and a recent (early May) urllib3 release is
   incompatible with the Ubuntu docker image used by the RTD. 
   See RTD issues on https://github.com/readthedocs/readthedocs.org/issues/10290
   Info in RTD tutorials is at https://docs.readthedocs.io/en/stable/config-file/v2.html


3. Useful readthedocs project links

   Only maintainer/admin can access 

   - console https://readthedocs.org/projects/yaml2rpm/
   - build info https://readthedocs.org/projects/yaml2rpm/builds/


Useful info links 
-----------------

- Automatic module documentation with **automodapi** 
  
  - https://sphinx-automodapi.readthedocs.io/en/latest/automodapi.html
  - https://sphinx-automodapi.readthedocs.io/en/latest/

- read the docs build process explanation https://github.com/readthedocs/readthedocs.org/blob/main/docs/user/builds.rst
