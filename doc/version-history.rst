.. _version_history:Version_History:

===============
Version History
===============

.. At the time of writing the Version history/release notes are not yet standardized amongst CSCs.
.. Until then, it is not expected that both a version history and a release_notes be maintained.
.. It is expected that each CSC link to whatever method of tracking is being used for that CSC until standardization occurs.
.. No new work should be required in order to complete this section.
.. Below is an example of a version history format.

.. towncrier release notes start

ts_gis v0.6.0 (2024-09-23)
==========================

Features
--------

- Go to fault state if disconnected unexpectedly. (`DM-42817 <https://rubinobs.atlassian.net/DM-42817>`_)


Bugfixes
--------

- Update ts-conda-build to 0.4 and restrict to pymodbus 3.5 and aiohttp 3.8.5. (`DM-43486 <https://rubinobs.atlassian.net/DM-43486>`_)
- Pin pymmodbus and sshtunnel in conda recipe. (`DM-45977 <https://rubinobs.atlassian.net/DM-45977>`_)


Improved Documentation
----------------------

- Add towncrier. (`DM-42817 <https://rubinobs.atlassian.net/DM-42817>`_)


v0.5.1
======
* Fix subsystem event bug.
* Change generation of 1 and 0's string array.

0.5.0
=====

* Support new pymodbus simulator.
* Support pymodbus 3.5.
* Split subsystem registers into booleans for publishing new subsystem events.

v0.4.5
======
* Clean up code.

v0.4.4
======
* Enforce pymodbus greater than or equal to 3 for runtime.

v0.4.3
======
* Enforce pymodbus greater than 3 for conda recipe.

v0.4.2
======
* Pass logs to CSC logs for debugging.
* Start the tunnel even when using open_tunnel.
* Add debug log to check registers when changed received.
* Improve raw status bit flag representation.

v0.4.1
======
* Fix typo in sshtunnel parameter ssh_pkey from pkey to ssh_pkey.

v0.4.0
======
* Swap ts-salobj base case.
* Fix import path for pymodbus.
* Add mock_server and simulation mode.
* Switch to async modbus client.
* Add sshtunnel functionality.

v0.3.0
======
* Use pyproject.toml
* Write documentation

v0.2.0
======
* Update CSC to support salobj 7

v0.1.0
======
* Initial CSC
