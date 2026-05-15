.. _Configuration_details:

#######################
GIS Configuration
#######################


The GIS CSC configuration defines how the CSC reaches the GIS Modbus server and how frequently it publishes telemetry events.
For real hardware, the CSC connects through an SSH tunnel to the configured Modbus endpoint.
In simulation mode, the CSC starts a local pymodbus simulator and rewrites the relevant connection values to point at the simulator.

The most important fields are:

1. ``modbus_host`` and ``modbus_port``: The remote GIS Modbus server endpoint.
2. ``bastion_host``, ``bastion_port``, ``ssh_username``, and ``pkey``: SSH tunnel settings for real hardware.
3. ``tunnel_host`` and ``tunnel_port``: Local tunnel endpoint used by the Modbus client.
4. ``telemetry_interval``: Time, in seconds, between telemetry loop updates.

The complete schema is shown below.

.. jsonschema:: lsst.ts.gis.CONFIG_SCHEMA
