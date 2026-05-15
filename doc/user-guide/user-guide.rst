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

The GIS CSC publishes SAL events for the raw GIS register state, changed subsystem register values, and per-subsystem boolean fields.
The raw status event contains the decoded state of all 35 GIS Modbus holding registers as a space-separated string of bits.
The status event contains an index and an integer indicating the raw register value for the subsystem.
The subsystem status event is only published when the previous raw register value changes.
In order to help identify each subsystem, an ordered list of subsystem names is provided by ``lsst.ts.gis.subsystem_order``.

GIS Interface
======================

Since the GIS is an alarm system meant for indicating a change in the sanctity of the telescope operations, we publish events instead of telemetry.
The CSC reads the GIS Modbus holding registers and publishes the decoded state as SAL events.

The first event that we'll note is the ``GIS_logevent_rawStatus`` event.
This event publishes all decoded register bits as one string, with one 16-bit group per subsystem.
The intention is to provide users with an overall picture of the status of the GIS since a cause can trigger multiple effects.
This is probably most useful for user interfaces.

The second event is the ``GIS_logevent_systemStatus`` event which is more granular as it only contains a changed subsystem's index and its updated word value as it is read from the Modbus server.
This is meant to help a user looking at the EFD data since it provides a more specific insight into an individual subsystem.

Subsystem-specific events are also published, with each bit exposed as a boolean field where the XML defines a named field.
Reserved/free bit ranges are packed into tuple fields.

Bit Ordering
============

GIS register bits are decoded using the Pilz Modbus convention: bit 0 is the least-significant bit and bit 15 is the most-significant bit.
For example, a register value of ``1`` means bit 0 is true and all other bits are false.

.. code:: python

    register = 1
    bits = [(register >> bit) & 1 for bit in range(16)]
    print(bits)  # [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


There is one subsystem event for each non-reserved subsystem, allowing the user to see which GIS bits are currently triggered.

Monitoring Workflow
===================

For high-level monitoring, subscribe to ``GIS_logevent_rawStatus`` to see the full GIS state.
For EFD queries that need to identify changed Modbus words, use ``GIS_logevent_systemStatus`` and map the ``index`` field through ``lsst.ts.gis.subsystem_order``.
For user interfaces and alarms, prefer the subsystem-specific events because they expose named boolean fields instead of requiring consumers to decode register bits themselves.
