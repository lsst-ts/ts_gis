.. _Developer_Guide:

###################
GIS Developer Guide
###################

The GIS communicates to the outside via a modbus server running off of the main GIS pilz CPU.
The software uses pymodbus as the modbus library.
The GIS publishes 29 words (2 bytes) for each subsystem, you can find the meanings of each value in the GIS to TCS document.

.. _Dependencies:

Dependencies
============

[This section should list dependencies in bullet form]

* `SAL <https://ts-sal.lsst.io>`_ - v5.x
* ts_salobj - v6.x
* ts_xml - v10
* ts_idl - >v3.1.3
* pymodbus - v2.5.2

.. Linking to the previous versions may also be worthwhile, depending on the CSC

.. _API:

GIS API
=============================

The content in this section is autogenerated from docstrings.

.. The code below should insert the docstrings from the code.

.. automodapi:: lsst.ts.gis
    :no-main-docstr:
    :no-inheritance-diagram:
    :inherited-members:


.. _Build:

Build and Test
==============

.. code::

    scons --clean
    scons

.. _Usage:

Usage
=====

.. code::

    run_gis_csc.py

.. _Simulator:

Simulator
=========

There is a hardware simulator, it can connected to via a switch and is found on the pilz GIS cpu at 192.168.180.1 on port 502.
You will need a copy of the PAS4000 software 1.18 running on Windows 10 in order to control the variables on the PILZ.

.. _Firmware:

Updating Firmware of the GIS
==================================================

This is not the responsiblity of the CSC developer.

.. _Documentation:

Building the Documentation
==========================

.. code::

    package-docs build


.. _Contributing:

Contributing
============

Code and documentation contributions utilize pull-requests on github.
Feature requests can be made by filing a Jira ticket with the `ts_gis` label.
In all cases, reaching out to the :ref:`contacts for this CSC <ts_xml:index:master-csc-table:GIS>` is recommended.

