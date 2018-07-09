====================
AWS Chalice Workshop
====================

This repository contains code for the AWS Chalice workshop.
You can read the rendered content on ReadTheDocs at:
http://chalice-workshop.readthedocs.io/en/latest/


Repo Layout
===========

* ``docs/`` - The step-by-step documentation for completing each tutorial
  in the workshop. This is a sphinx project and can be used to
  generate both html as well as a pdf of the guide.
* ``code/`` - The code to use for the workshop. Each tutorial will have
  a ``final/`` directory reflecting the end code for application once the
  tutorial is complete.

Building the Docs
=================

Install requirements::

    $ pip install -r requirements.txt


Build html docs::

    $ make html
