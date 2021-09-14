__all__ = ["GISComponent"]

import itertools

from .commander import ModbusCommander


class GISComponent:
    """The controller for GIS.

    Parameters
    ----------
    csc

    Attributes
    ----------
    commander
    csc
    raw_status
    system_status
    """

    def __init__(self, csc) -> None:
        self.commander = None
        self.csc = csc
        self.raw_status = None
        self.system_status = []

    @property
    def connected(self):
        """Return if the component is connected or not.

        Returns
        -------
        `bool`
            A boolean which determines the connection status of the client.
        """
        if self.commander is not None:
            return self.commander.connected
        else:
            return False

    def connect(self):
        """Connect to the commander."""
        self.commander = ModbusCommander(self.config.host, self.config.port)
        self.commander.connect()

    def disconnect(self):
        """Disconnect from the commander."""
        if self.commander is not None:
            self.commander.disconnect()
            self.commander = None

    def update_status(self):
        """Update the status of the GIS."""
        reply = self.commander.read()
        raw_status = self.commander.get_raw_string(reply)
        if self.raw_status != raw_status:
            self.csc.evt_rawStatus.set_put(status=raw_status)
        self.raw_status = raw_status
        for index, (current_subsystem, old_subsystem) in enumerate(
            itertools.zip_longest(reply.registers, self.system_status, fillvalue=None)
        ):
            if current_subsystem != old_subsystem:
                self.csc.evt_systemStatus.set_put(index=index, status=current_subsystem)
        self.system_status = reply.registers

    def configure(self, config):
        """Configure the GIS."""
        self.config = config
