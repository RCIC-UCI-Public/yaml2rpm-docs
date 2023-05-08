Template for the Read the Docs tutorial
=======================================

This GitHub template includes fictional Python library
with some basic Sphinx docs.

Read the tutorial here:

https://docs.readthedocs.io/en/stable/tutorial/


Building HTML locally for testing
---------------------------------

1. Install prerequisites

   .. code-block:: console

      pip install sphinx
      pip install sphinx_rtd_theme


2. Check out repo and build

   .. code-block:: console

      git clone git@github.com:RCIC-UCI-Public/yaml2rpm-docs.git
      cd yaml2rpm-docs/docs
      make html

3. Point your browser to `build/html/index.html`.



Notes
-----

Manual  integration of the github repo with Read the Docs (RTD) project
https://docs.readthedocs.io/en/stable/guides/git-integrations.html

Had to add ``.readthedocs.yaml`` file in order to specify what type of a build
RTD need to do. This is needed to fix a recent update to  urllib3 which
is used in docker container and a recent (early May) urllib3 release is
incompatible with the Ubuntu docker image used by the RTD. 
See RTD issues on https://github.com/readthedocs/readthedocs.org/issues/10290


