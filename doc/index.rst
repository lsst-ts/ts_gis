#########################
GIS
#########################

.. image:: https://img.shields.io/badge/SAL-API-gray.svg
    :target: https://ts-xml.lsst.io/sal_interfaces/GIS.html
.. image:: https://img.shields.io/badge/GitHub-gray.svg
    :target: https://github.com/lsst-ts/ts_gis
.. image:: https://img.shields.io/badge/Jira-gray.svg
    :target: https://jira.lsstcorp.org/issues/?jql=labels+%3D+ts_gis
.. image:: https://img.shields.io/badge/Jenkins-gray.svg
    :target: https://tssw-ci.lsst.org/job/LSST_Telescope-and-Site/job/ts_gis/

.. _Overview:

Overview
========

The GIS CSC reads the Global Interlock System Modbus interface and publishes SAL events describing the state of telescope safety interlocks.
The GIS is a safety system that prevents or interrupts telescope operation when interlock conditions are violated.

As with all CSCs, information on the package, developers and product owners can be found in the `Master CSC Table <ts_xml:index:master-csc-table:GIS>`_.

.. note:: If you are interested in viewing other branches of this repository append a `/v` to the end of the url link. For example `https://ts_gis.lsst.io/v/`


.. _User_Documentation:

User Documentation
==================

User-level documentation is aimed at personnel monitoring GIS state through SAL events.

.. toctree::
    user-guide/user-guide
    :maxdepth: 2

.. _Configuration:

Configuring the GIS
=========================================
The GIS configuration schema and connection parameters are described at the following link.

.. toctree::
    configuration/configuration
    :maxdepth: 1


.. _Development_Documentation:

Development Documentation
=========================

Developer documentation covers the Modbus interface, simulator behavior, register-map audit tooling, and package APIs.

.. toctree::
    developer-guide/developer-guide
    :maxdepth: 1

.. _Version_History:

Version History
===============

.. At the time of writing the Version history/release notes are not yet standardized amongst CSCs.
.. Until then, it is not expected that both a version history and a release_notes be maintained.
.. It is expected that each CSC link to whatever method of tracking is being used for that CSC until standardization occurs.
.. No new work should be required in order to complete this section.

The version history of the GIS is found at the following link.

.. toctree::
    version-history
    :maxdepth: 1
