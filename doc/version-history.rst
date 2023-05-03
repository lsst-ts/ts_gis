.. _version_history:Version_History:

===============
Version History
===============

.. At the time of writing the Version history/release notes are not yet standardized amongst CSCs.
.. Until then, it is not expected that both a version history and a release_notes be maintained.
.. It is expected that each CSC link to whatever method of tracking is being used for that CSC until standardization occurs.
.. No new work should be required in order to complete this section.
.. Below is an example of a version history format.

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
