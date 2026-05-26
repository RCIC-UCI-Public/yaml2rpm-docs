
.. _next_steps:

Next Steps
===========

Read the remainder of the documentation. It explains in-depth admixes purpose, layouts,
and their files. 

For inpatient people working on the same OS (currently Rocky 9.7)
can do a :ref:`superbuild <superbuild>` next. 

For step by step build:

1. While on the container, clone the *admixbuilder* repository:

    .. parsed-literal::
      :command:`cd /export/repositories
      git clone https://github.com/RCIC-UCI-Public/admixbuilder`

2. If working on a newer OS will have to clone and build admixes one by one
   in order described in ``admixbuidler/buildorder``. At this point already have
   *yaml2rpm* built, the next admix is *buildtools-admix*:

     .. parsed-literal::
       :command:`cd /export/repositories
       git clone https://github.com/RCIC-UCI-Public/buildtools-admix
       cd buildtools-admix
       make buildall &> out &`

   Check the output and resulting RPMs. If there are errors need to figure
   out what RPM had problems and apply fixes, then uninstall empty or bad RPMs
   (see list of built RPMS in ``RPMS/``)
   and restart the *buildall* target anew until all RPMs are build and valid. 

3. Install the admix RPMs, at the top level of the repo do:

     .. parsed-literal::
       :command:`make install-admix YES=-y`

4.  Proceed with building the next admix.

