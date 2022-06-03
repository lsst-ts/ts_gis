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


.. image:: https://img.shields.io/badge/SAL-API-gray.svg
    :target: https://ts-xml.lsst.io/sal_interfaces/GIS.html
.. image:: https://img.shields.io/badge/GitHub-gray.svg
    :target: https://github.com/lsst-ts/ts_gis
.. image:: https://img.shields.io/badge/Jira-gray.svg
    :target: https://jira.lsstcorp.org/issues/?jql=labels+%3D+ts_gis
.. image:: https://img.shields.io/badge/Jenkins-gray.svg
    :target: https://tssw-ci.lsst.org/job/LSST_Telescope-and-Site/job/ts_gis/

The GIS outputs two events via SAL DDS.
The raw status event contains the whole 29 words of the GIS into one bytearray.
The status event contains an index and a integer indicating the status from the subsystem.
These events are only published when the previous status has changed.
In order to help figure out what each system is, an enumeration containing the names of the systems is provided in the ts_idl package.

GIS Interface
======================

Since the GIS is an alarm system meant for indicating a change in the sanctity of the telescope operations, we publish events instead of telemetry.
The CSC works by producing two events upon reading of a change in the GIS.

The first event that we'll note is the ``GIS_logevent_rawStatus`` event, this event produces a byte array of 29 values from each subsystem that's currently implemented in the firmware.
The intention is to provide users with a overall picture of the status of the GIS since a cause can trigger multiple effects.
This is probably most useful for user interfaces.

The second event is the ``GIS_logevent_systemStatus`` event which is more granular as it only contains a changed subsystem's index and its updated word value as its being read from the modbus server.
This is more meant to help with a user looking at the EFD data since it provides a more specific insight into an individual subsystem.

Both events will need to be manipulated in order to see which bits/flags were changed in each subsystem.

For example, we might get back a value of 232 from the subsystem.
In order to determine the flag/bit value, we need to convert this value to an array of bits.
First install a third party package bitarray which will make this process much easier.

.. prompt::

    conda install bitarray


.. code:: python

    from bitarray import bitarray
    import sys
    reply = 232 # this is the integer value that we received from the CSC
    byte_reply = reply.to_bytes(2, sys.byteorder) # We convert the int to a bytes object where we know that we have two bytes of data and we get the big/little value from the machine
    data_bits = bitarray() # Create an empty bitarray
    data_bits.frombytes(byte_reply) # Extend the bitarray with a bytes object
    print(data_bits.to01()) # 1110100000000000


Example Use-Case
================

TBD.
