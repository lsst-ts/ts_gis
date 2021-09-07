..
  This is a template for the user-guide documentation that will accompany each CSC.
  This template is provided to ensure that the documentation remains similar in look, feel, and contents to users.
  The headings below are expected to be present for all CSCs, but for many CSCs, additional fields will be required.

  ** All text in square brackets [] must be re-populated accordingly **

  See https://developer.lsst.io/restructuredtext/style.html
  for a guide to reStructuredText writing.

  Use the following syntax for sections:

  Sections
  ========

  and

  Subsections
  -----------

  and

  Subsubsections
  ^^^^^^^^^^^^^^

  To add images, add the image file (png, svg or jpeg preferred) to the
  images/ directory. The reST syntax for adding the image is

  .. figure:: /images/filename.ext
   :name: fig-label

   Caption text.

  Feel free to delete this instructional comment.

.. Fill out data so contacts section below is auto-populated
.. add name and email between the *'s below e.g. *Marie Smith <msmith@lsst.org>*
.. |CSC_developer| replace::  *Replace-with-name-and-email*
.. |CSC_product_owner| replace:: *Replace-with-name-and-email*

.. _User_Guide:

#######################
GIS User Guide
#######################

.. Update links and labels below
.. image:: https://img.shields.io/badge/GitHub-ts_athexapod-green.svg
    :target: https://github.com/lsst-ts/ts_athexapod
.. image:: https://img.shields.io/badge/Jenkins-ts_athexapod-green.svg
    :target: https://tssw-ci.lsst.org/job/LSST_Telescope-and-Site/job/ts_athexapod/
.. image:: https://img.shields.io/badge/Jira-ts_athexapod-green.svg
    :target: https://jira.lsstcorp.org/issues/?jql=labels+%3D+ts_athexapod
.. image:: https://img.shields.io/badge/ts_xml-ATHexapod-green.svg
    :target: https://ts-xml.lsst.io/sal_interfaces/ATHexapod.html


The GIS outputs two events via SAL DDS.
The raw status contains the whole 29 words of the GIS into one bytearray.
The status event contains an index and a integer from the subsystem.
These events are only published when the previous status has changed.
In order to help figure out what each system is, an enumeration containing the names of the systems is provided in the ts_idl package.

GIS Interface
======================

The important part of the GIS interface is the status event where each individual subsystem change is published and therefore can be easily corresponded to the System enumeration located in the ts_idl package.

Example Use-Case
================

TBD.
