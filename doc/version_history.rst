v0.7.0 (2026-06-02)
===================

New Features
------------

- Added tooling to parse ``Send_TCS.txt`` PLC structured text into GIS Modbus register mappings for auditing. (`OSW-2263 <https://rubinobs.atlassian.net//browse/OSW-2263>`_)


Bug Fixes
---------

- Fixed GIS Modbus register decoding to use Pilz least-significant-bit first bit ordering. (`OSW-2263 <https://rubinobs.atlassian.net//browse/OSW-2263>`_)


Performance Enhancement
-----------------------

- Added missing fields and events. (`OSW-1845 <https://rubinobs.atlassian.net//browse/OSW-1845>`_)


Other Changes and Additions
---------------------------

- Updated conda recipe to use pymodbus 3.11.


v0.6.2 (2026-01-22)
===================

Other Changes and Additions
---------------------------

- Pinned paramiko to compatible version with sshtunnel. (`OSW-1208 <https://rubinobs.atlassian.net//browse/OSW-1208>`_)


v0.6.1 (2025-08-12)
===================

Performance Enhancement
-----------------------

- Added mypy type hints and switched to ruff from black, flake8 and isort. (`OSW-731 <https://rubinobs.atlassian.net//browse/OSW-731>`_)
